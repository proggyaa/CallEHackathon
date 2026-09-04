"""Utility helper for loading mock CALL-E agent responses."""

import json
from pathlib import Path


def load_mock_call_response() -> dict:
    """Loads mock JSON call response from tests directory."""
    mock_file = (
        Path(__file__).parent.parent / "tests" / "mock_response.json"
    )
    if not mock_file.exists():
        raise FileNotFoundError(f"Mock data file not found at: {mock_file}")

    with open(mock_file, "r", encoding="utf-8") as f:
        return json.load(f)