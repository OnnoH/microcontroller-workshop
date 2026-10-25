"""Shared fixtures for the ONN-6 acceptance tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
SCRIPTS = ROOT / ".github" / "scripts"


@pytest.fixture(scope="session")
def root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def workflow() -> dict:
    """ci.yml, parsed.

    `on:` is quoted so PyYAML does not fold it to the boolean True, which is
    what the YAML 1.1 spec it implements would otherwise do.
    """
    text = WORKFLOW.read_text(encoding="utf-8")
    parsed = yaml.safe_load(text)
    if True in parsed:
        parsed["on"] = parsed.pop(True)
    return parsed


@pytest.fixture(scope="session")
def jobs(workflow: dict) -> dict:
    return workflow["jobs"]


@pytest.fixture(scope="session")
def job_text(workflow: dict) -> dict[str, str]:
    """Every job's definition re-rendered as YAML, for substring assertions."""
    return {name: yaml.safe_dump(body) for name, body in workflow["jobs"].items()}


@pytest.fixture(scope="session")
def inventory():
    """The AC-4 inventory script, imported as a module."""
    spec = importlib.util.spec_from_file_location(
        "pio_deps_inventory", SCRIPTS / "pio_deps_inventory.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
