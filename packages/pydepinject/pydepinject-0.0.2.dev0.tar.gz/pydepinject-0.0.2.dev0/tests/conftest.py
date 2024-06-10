from __future__ import annotations

import pathlib

import pytest

PROJECT_DIR = pathlib.Path(__file__).parent.parent


@pytest.fixture(autouse=True)
def check_test_leftovers():
    """Checks if the test left any files in the project directory."""
    items_before = list(PROJECT_DIR.iterdir())
    yield
    items_after = list(PROJECT_DIR.iterdir())
    new_items = set(items_after) - set(items_before)
    new_items = {item for item in new_items if not item.name.startswith(".coverage")}
    if new_items:
        pytest.fail(f"New items in the project directory: {new_items}")
