"""AC-1: a workflow runs `pio run` for each Boxes/*/platformio.ini project on
every push and pull request."""

from __future__ import annotations

import json
import os
import stat
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pio-build.sh"
LIST_BOXES = Path(__file__).resolve().parents[1] / "scripts" / "list-boxes.sh"

NOTHING_TO_BUILD = (
    "Error: Nothing to build. Please put your source code files to the 'src' folder"
)


def write_stub_pio(directory: Path, *, pkg_install_exit: int, run_exit: int, run_output: str) -> None:
    """A fake `pio` that records nothing and answers as the test dictates."""
    stub = directory / "pio"
    stub.write_text(
        "#!/usr/bin/env bash\n"
        'case "$1" in\n'
        f"  pkg) exit {pkg_install_exit} ;;\n"
        f'  run) printf "%s\\n" {json.dumps(run_output)}; exit {run_exit} ;;\n'
        "  *) echo \"unexpected: $*\" >&2; exit 2 ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    stub.chmod(stub.stat().st_mode | stat.S_IEXEC)


def run_build(box: Path, stub_dir: Path) -> subprocess.CompletedProcess:
    environment = dict(os.environ, PATH=f"{stub_dir}:{os.environ['PATH']}")
    return subprocess.run(
        [str(SCRIPT), str(box)],
        capture_output=True,
        text=True,
        env=environment,
        check=False,
    )


@pytest.fixture
def box(tmp_path: Path) -> Path:
    box = tmp_path / "Box Z - Test Board"
    box.mkdir()
    (box / "platformio.ini").write_text(
        "[env:testboard]\nplatform = atmelavr\nboard = uno\nframework = arduino\n",
        encoding="utf-8",
    )
    return box


@pytest.fixture
def stub_dir(tmp_path: Path) -> Path:
    stub_dir = tmp_path / "bin"
    stub_dir.mkdir()
    return stub_dir


def test_ac1_every_box_with_a_platformio_ini_is_discovered(root: Path) -> None:
    expected = sorted(
        (path.parent.relative_to(root).as_posix() for path in root.glob("Boxes/*/platformio.ini")),
        key=lambda path: path.rsplit("/", 1)[-1],
    )
    assert expected, "no Boxes/*/platformio.ini projects found"

    discovered = json.loads(
        subprocess.run(
            [str(LIST_BOXES)], cwd=root, capture_output=True, text=True, check=True
        ).stdout
    )
    assert discovered == expected


def test_ac1_build_job_runs_pio_over_the_discovered_boxes(jobs: dict, job_text: dict) -> None:
    build = jobs["pio-build"]
    assert build["needs"] == "discover-boxes"
    assert build["strategy"]["matrix"]["box"] == "${{ fromJSON(needs.discover-boxes.outputs.boxes) }}"
    assert build["strategy"]["fail-fast"] is False
    assert "AC-1" in build["name"]
    assert ".github/scripts/pio-build.sh" in job_text["pio-build"]
    assert ".github/scripts/list-boxes.sh" in job_text["discover-boxes"]


def test_ac1_runs_on_push_and_pull_request(workflow: dict) -> None:
    assert set(workflow["on"]) == {"push", "pull_request"}


def test_ac1_build_fails_when_the_project_config_does_not_resolve(box: Path, stub_dir: Path) -> None:
    write_stub_pio(stub_dir, pkg_install_exit=1, run_exit=0, run_output="unreachable")
    result = run_build(box, stub_dir)
    assert result.returncode == 1


def test_ac1_build_fails_when_a_box_with_sources_does_not_compile(box: Path, stub_dir: Path) -> None:
    (box / "src").mkdir()
    (box / "src" / "main.cpp").write_text("void setup() {}\n", encoding="utf-8")
    write_stub_pio(stub_dir, pkg_install_exit=0, run_exit=1, run_output="error: 'oops' was not declared")

    result = run_build(box, stub_dir)
    assert result.returncode == 1
    assert "::error" in result.stdout


def test_ac1_build_passes_when_a_box_with_sources_compiles(box: Path, stub_dir: Path) -> None:
    (box / "src").mkdir()
    (box / "src" / "main.cpp").write_text("void setup() {}\n", encoding="utf-8")
    write_stub_pio(stub_dir, pkg_install_exit=0, run_exit=0, run_output="SUCCESS")

    assert run_build(box, stub_dir).returncode == 0


def test_ac1_build_passes_a_box_that_has_no_sketch_yet(box: Path, stub_dir: Path) -> None:
    """A box ships a platformio.ini for the participant to write a sketch into.

    PlatformIO exits 1 on such a project, so AC-1 would otherwise be red on
    every box in this repository; the config must still resolve.
    """
    write_stub_pio(stub_dir, pkg_install_exit=0, run_exit=1, run_output=NOTHING_TO_BUILD)

    result = run_build(box, stub_dir)
    assert result.returncode == 0
    assert "::notice" in result.stdout


def test_ac1_build_fails_when_a_box_without_sources_fails_for_another_reason(
    box: Path, stub_dir: Path
) -> None:
    write_stub_pio(stub_dir, pkg_install_exit=0, run_exit=1, run_output="Error: Unknown board ID 'uno'")
    assert run_build(box, stub_dir).returncode == 1


def test_ac1_build_fails_on_a_directory_without_a_platformio_ini(tmp_path: Path, stub_dir: Path) -> None:
    empty = tmp_path / "Box Y - No Config"
    empty.mkdir()
    assert run_build(empty, stub_dir).returncode == 1
