"""Tests for copilot.vision_ingest."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from copilot.models import ProfileFact

# ---------------------------------------------------------------------------
# Unit tests — mock ollama_client.vision
# ---------------------------------------------------------------------------

MOCK_VISION_RESPONSE = json.dumps({
    "ranks": {
        "combat": "Expert",
        "trade": "Elite V",
        "explore": "Elite",
        "soldier": "Defenceless",
        "exobiologist": "Directionless",
        "cqc": "Helpless"
    },
    "balance_cr": 3200000000,
    "assets": {
        "carriers": 2,
        "ships_estimate": "many"
    }
})


class TestIngestScreenshotUnit:
    def test_returns_list_of_profile_facts(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        assert isinstance(facts, list)
        assert all(isinstance(f, ProfileFact) for f in facts)

    def test_origin_is_screenshot(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        assert all(f.origin == "screenshot" for f in facts)

    def test_verified_is_false(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        assert all(f.verified is False for f in facts)

    def test_rank_facts_extracted(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        combat = [f for f in facts if f.key == "rank.combat"]
        assert len(combat) == 1
        assert combat[0].value == "Expert"

    def test_balance_extracted_when_present(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = MOCK_VISION_RESPONSE
            facts = ingest_screenshot(str(fake_img))
        balance = [f for f in facts if f.key == "balance_cr"]
        assert len(balance) == 1
        assert balance[0].value == "3200000000"

    def test_malformed_vision_response_returns_empty(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.return_value = "not valid JSON at all {{{"
            facts = ingest_screenshot(str(fake_img))
        assert facts == []

    def test_vision_unavailable_returns_empty(self, tmp_path):
        from copilot.vision_ingest import ingest_screenshot
        from copilot.ollama_client import OllamaUnavailable
        fake_img = tmp_path / "rank.png"
        fake_img.write_bytes(b"\x89PNG\r\n")
        with patch("copilot.vision_ingest.ollama_client") as mock_client:
            mock_client.vision.side_effect = OllamaUnavailable("Ollama unreachable")
            mock_client.OllamaUnavailable = OllamaUnavailable
            facts = ingest_screenshot(str(fake_img))
        assert facts == []


# ---------------------------------------------------------------------------
# Integration test — real Ollama call (skip unless --integration flag)
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_ingest_real_screenshot():
    """Requires Ollama + qwen3-vl:8b running and the rank screenshot present."""
    from copilot.vision_ingest import ingest_screenshot
    img = Path(r"C:\Users\Quadstronaut\.claude\image-cache\45518cb0-435b-47c5-9711-56ce5054f178\1.png")
    if not img.exists():
        pytest.skip(f"Rank screenshot not found at {img} — drop a screenshot and rerun.")
    facts = ingest_screenshot(str(img))
    assert len(facts) > 0
    rank_keys = [f.key for f in facts if f.key.startswith("rank.")]
    assert len(rank_keys) >= 1, "Expected at least one rank fact from the screenshot"
