# copilot/paths.py
"""Repo-root anchor and configuration loader.

All path helpers resolve relative to repo_root() so the project is relocatable
as long as config.toml stays at the repo root.
"""

import tomllib
from pathlib import Path


def repo_root() -> Path:
    """Return the absolute path to the repo root (directory containing config.toml).

    Resolves by walking up from this file's location until config.toml is found,
    which makes the project relocatable and safe inside sub-packages.
    """
    here = Path(__file__).resolve().parent  # copilot/
    root = here.parent                      # EliteDangerousKB/
    config_candidate = root / "config.toml"
    if not config_candidate.exists():
        raise FileNotFoundError(
            f"config.toml not found at expected repo root {root}. "
            "Ensure paths.py lives in copilot/ directly under the repo root."
        )
    return root


def load_config() -> dict:
    """Parse and return config.toml as a nested dict (tomllib; Python 3.11+)."""
    config_path = repo_root() / "config.toml"
    with open(config_path, "rb") as fh:
        return tomllib.load(fh)


def kb_dir() -> Path:
    """Return the kb/ directory as configured in config.toml [paths].kb."""
    cfg = load_config()
    return repo_root() / cfg["paths"]["kb"]


def embeddings_dir() -> Path:
    """Return the embeddings/ directory as configured in config.toml [paths].embeddings."""
    cfg = load_config()
    return repo_root() / cfg["paths"]["embeddings"]


def indexes_dir() -> Path:
    """Return the indexes/ directory as configured in config.toml [paths].indexes."""
    cfg = load_config()
    return repo_root() / cfg["paths"]["indexes"]
