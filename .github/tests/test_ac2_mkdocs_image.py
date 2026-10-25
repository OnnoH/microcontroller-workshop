"""AC-2: a workflow builds Containers/Dockerfile.mkdocs on every push and pull
request."""

from __future__ import annotations

from pathlib import Path


def test_ac2_dockerfile_exists(root: Path) -> None:
    assert (root / "Containers" / "Dockerfile.mkdocs").is_file()


def test_ac2_job_builds_the_mkdocs_dockerfile(jobs: dict, job_text: dict) -> None:
    job = jobs["mkdocs-image"]
    assert "AC-2" in job["name"]

    text = job_text["mkdocs-image"]
    assert "docker build" in text
    assert "--file Containers/Dockerfile.mkdocs" in text


def test_ac2_job_runs_on_push_and_pull_request(workflow: dict, jobs: dict) -> None:
    assert set(workflow["on"]) == {"push", "pull_request"}
    assert "if" not in jobs["mkdocs-image"], "the job must not be conditional on the event"
