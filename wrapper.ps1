<#
.SYNOPSIS
    ED Research Loop daemon. Runs the autonomous KB-builder loop.

    Each iteration shells out to `claude -p <ed-research-prompt.md>`, which acts as
    the loop orchestrator: it reads STATE.toml, researches ED sources, writes KB
    pages, indexes them, commits, and checkpoints STATE.toml. The wrapper handles
    looping, retry/backoff, logging, and the -MaxLoops bound.

.PARAMETER MaxLoops
    Stop after this many successful loops. 0 (default) = run until STATE.toml halt=true.
    Use a small value (e.g. 3) to prove the loop before going unbounded.

.PARAMETER SkipPermissions
    Pass --dangerously-skip-permissions to the nested claude so it can write files,
    run git, and WebFetch unattended. Required for true autonomous operation.

.NOTE
    KEEP THIS FILE PURE ASCII. A non-ASCII byte is read as cp1252 by Windows
    PowerShell 5.1 (no BOM) and corrupts parsing. See launch-copilot.ps1 history.
#>
param(
    [string]$PromptFile     = "ed-research-prompt.md",
    [string]$LogFile        = "journal\daemon.log",
    [int]   $MaxRetries     = 3,
    [int]   $BaseBackoffSec = 30,
    [int]   $MaxLoops       = 0,
    [switch]$SkipPermissions,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$RepoRoot = $PSScriptRoot   # wrapper.ps1 lives at repo root

# ---------------------------------------------------------------------------
# Usage. -Help / -help / --help / -h all bind to $Help; bare 'help' lands in $args.
# ---------------------------------------------------------------------------
function Show-Usage {
    Write-Output @"
ED Research Loop daemon - runs the autonomous KB-builder loop.

USAGE:
    .\wrapper.ps1 [-PromptFile <path>] [-LogFile <path>] [-MaxRetries <n>]
                  [-BaseBackoffSec <n>] [-MaxLoops <n>] [-SkipPermissions] [-Help]

PARAMETERS:
    -PromptFile <path>     Loop prompt fed to claude -p. Default: ed-research-prompt.md
    -LogFile <path>        Append log here. Default: journal\daemon.log
    -MaxRetries <n>        Attempts per loop before backoff/abort. Default: 3
    -BaseBackoffSec <n>    Base for exponential retry backoff (sec). Default: 30
    -MaxLoops <n>          Stop after n successful loops. 0 = run until halt=true. Default: 0
    -SkipPermissions       Pass --dangerously-skip-permissions to nested claude (unattended).
    -Help, -help, --help   Show this help and exit.

EXAMPLES:
    .\wrapper.ps1 -MaxLoops 3 -SkipPermissions   # prove the loop, bounded
    .\wrapper.ps1 -SkipPermissions               # run unbounded until halt=true
"@
}
# Bare 'help' binds positionally to $PromptFile (position 0), so check there too.
if ($Help -or ($args -contains 'help') -or ($PromptFile -eq 'help')) { Show-Usage; exit 0 }

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
$LogPath = Join-Path $RepoRoot $LogFile
$logDir  = Split-Path $LogPath -Parent
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force $logDir | Out-Null }

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $ts   = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
    $line = "$ts  [$Level]  $Message"
    $line | Tee-Object -FilePath $LogPath -Append
}

# ---------------------------------------------------------------------------
# STATE.toml read (via Python tomllib -> JSON -> PSCustomObject)
# ---------------------------------------------------------------------------
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

function Read-StateToml {
    $statePath = Join-Path $RepoRoot "STATE.toml"
    if (-not (Test-Path $statePath)) {
        Write-Log "STATE.toml not found - treating as fresh start." "WARN"
        return [pscustomobject]@{ loop_number = 0; last_completed_phase = "none"; halt = $false; mode = "search" }
    }
    $py = @"
import tomllib, json
with open(r'$statePath', 'rb') as f:
    print(json.dumps(tomllib.load(f)))
"@
    $json = & $VenvPython -c $py
    if ($LASTEXITCODE -ne 0) {
        Write-Log "STATE.toml parse error: $json" "ERROR"
        return $null
    }
    # Normalize missing keys to defaults. Under Set-StrictMode -Version Latest,
    # accessing an absent property (e.g. $s.halt on a hand-edited STATE.toml that
    # dropped the key) throws a TERMINATING error and crashes the daemon. Add the
    # three keys the main loop reads if they are missing.
    $s = ($json | ConvertFrom-Json)
    if ($null -eq $s.PSObject.Properties['halt'])        { $s | Add-Member -NotePropertyName halt        -NotePropertyValue $false  }
    if ($null -eq $s.PSObject.Properties['mode'])        { $s | Add-Member -NotePropertyName mode        -NotePropertyValue 'search' }
    if ($null -eq $s.PSObject.Properties['loop_number']) { $s | Add-Member -NotePropertyName loop_number -NotePropertyValue 0       }
    return $s
}

# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------
if (-not (Test-Path (Join-Path $RepoRoot $PromptFile))) {
    Write-Log "Prompt file not found: $PromptFile" "ERROR"; exit 1
}
if (-not (Test-Path $VenvPython)) {
    Write-Log "venv python not found at .venv\Scripts\python.exe" "ERROR"; exit 1
}
$claude = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claude) { Write-Log "claude CLI not on PATH." "ERROR"; exit 1 }

$boundDesc = if ($MaxLoops -gt 0) { "bounded: $MaxLoops loop(s)" } else { "unbounded (until halt=true)" }
Write-Log "=== ED Research Daemon starting. PID=$PID. $boundDesc ==="

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
$loopsDone = 0
while ($true) {
    if ($MaxLoops -gt 0 -and $loopsDone -ge $MaxLoops) {
        Write-Log "=== Reached MaxLoops=$MaxLoops. Stopping cleanly. ==="
        exit 0
    }

    $state = Read-StateToml
    if ($null -eq $state) { Write-Log "State unreadable - aborting." "ERROR"; exit 1 }
    if ($state.halt -eq $true) { Write-Log "Halt flag set in STATE.toml - exiting." ; exit 0 }

    $loopStart   = Get-Date
    $attempt     = 0
    $loopSuccess = $false
    $beforeLoop  = [int]$state.loop_number
    Write-Log "=== Loop $($state.loop_number) start (mode=$($state.mode), phase=$($state.last_completed_phase)) ==="

    while (-not $loopSuccess -and $attempt -lt $MaxRetries) {
        $attempt++
        Write-Log "Invoking claude (attempt $attempt/$MaxRetries)..."

        # Read prompt fresh each attempt (allows hot-editing the prompt).
        $prompt = Get-Content (Join-Path $RepoRoot $PromptFile) -Raw -Encoding UTF8

        # Build claude args. Pipe the prompt via stdin to dodge the ~32KB
        # command-line length limit on Windows.
        $claudeArgs = @("-p")
        if ($SkipPermissions) { $claudeArgs = @("--dangerously-skip-permissions") + $claudeArgs }

        $prompt | & claude @claudeArgs 2>&1 | Tee-Object -FilePath $LogPath -Append
        $exitCode = $LASTEXITCODE   # capture IMMEDIATELY - next line may clobber it

        # Exit 0 alone is NOT proof of work: a headless claude can exit 0 after merely
        # chatting. Require STATE.toml loop_number to actually ADVANCE (the orchestrator
        # increments it only at COMMIT). That is the honest completion signal.
        $advanced = $false
        if ($exitCode -eq 0) {
            $after = Read-StateToml
            if ($null -ne $after -and ([int]$after.loop_number) -gt $beforeLoop) { $advanced = $true }
        }

        if ($advanced) {
            $loopSuccess = $true
            Write-Log "=== Loop succeeded: loop_number $beforeLoop -> $($after.loop_number). Duration: $((Get-Date) - $loopStart) ==="
        } else {
            if ($exitCode -eq 0) {
                Write-Log "claude exited 0 but loop_number did NOT advance (still $beforeLoop) - orchestrator did not complete a loop." "WARN"
            } else {
                Write-Log "claude exited $exitCode." "WARN"
            }
            $backoff = [int]([math]::Pow(2, $attempt) * $BaseBackoffSec)
            if ($attempt -lt $MaxRetries) {
                Write-Log "Backing off ${backoff}s (attempt $attempt/$MaxRetries)." "WARN"
                for ($i = $backoff; $i -gt 0; $i -= 10) {
                    Write-Log "  ... retrying in ${i}s"
                    Start-Sleep -Seconds ([math]::Min(10, $i))
                }
            }
        }
    }

    if ($loopSuccess) {
        $loopsDone++
        Write-Log "Loops completed this session: $loopsDone"
    } else {
        if ($MaxLoops -gt 0) {
            Write-Log "All $MaxRetries retries failed in bounded mode - aborting." "ERROR"; exit 1
        }
        Write-Log "All $MaxRetries retries failed. Sleeping 5 min before next attempt." "ERROR"
        for ($i = 300; $i -gt 0; $i -= 15) {
            Write-Log "  ... next attempt in ${i}s"
            Start-Sleep -Seconds 15
        }
    }
}
