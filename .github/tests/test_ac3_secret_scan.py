"""AC-3: a secret-scan job (gitleaks) runs on every push and pull request."""

from __future__ import annotations

import re
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "gitleaks.sh"


def test_ac3_job_runs_the_gitleaks_script(jobs: dict, job_text: dict) -> None:
    job = jobs["secret-scan"]
    assert "AC-3" in job["name"]
    assert ".github/scripts/gitleaks.sh" in job_text["secret-scan"]


def test_ac3_job_checks_out_the_full_history(jobs: dict) -> None:
    """`gitleaks git` can only scan the commits it was given."""
    checkout = next(
        step for step in jobs["secret-scan"]["steps"] if str(step.get("uses", "")).startswith("actions/checkout")
    )
    assert checkout["with"]["fetch-depth"] == 0


def test_ac3_job_runs_on_push_and_pull_request(workflow: dict, jobs: dict) -> None:
    assert set(workflow["on"]) == {"push", "pull_request"}
    assert "if" not in jobs["secret-scan"], "the job must not be conditional on the event"


def test_ac3_script_pins_a_version_and_its_checksum() -> None:
    text = SCRIPT.read_text(encoding="utf-8")
    version = re.search(r"GITLEAKS_VERSION=\$\{GITLEAKS_VERSION:-([\d.]+)\}", text)
    checksum = re.search(r"GITLEAKS_SHA256=\$\{GITLEAKS_SHA256:-([0-9a-f]{64})\}", text)
    assert version, "the gitleaks version must be pinned"
    assert checksum, "the downloaded gitleaks tarball must be checksum-verified"
    assert "sha256sum --check --strict" in text
