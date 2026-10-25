"""AC-4: a dependency-audit job inventories the PlatformIO libraries per box."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest


def make_box(root: Path, name: str, body: str) -> None:
    box = root / "Boxes" / name
    box.mkdir(parents=True)
    (box / "platformio.ini").write_text(textwrap.dedent(body).lstrip(), encoding="utf-8")


@pytest.fixture
def fixture_repo(tmp_path: Path) -> Path:
    make_box(
        tmp_path,
        "Box A - No Libraries",
        """
        ; a comment the parser has to tolerate
        [env:nanoatmega328]
        platform = atmelavr
        board = nanoatmega328
        framework = arduino
        """,
    )
    make_box(
        tmp_path,
        "Box B - Two Libraries",
        """
        [env:esp12e]
        platform = espressif8266
        board = esp12e
        framework = arduino
        lib_deps =
          adafruit/DHT sensor library@^1.4.6
          fastled/FastLED@^3.10.3
        """,
    )
    return tmp_path


def test_ac4_job_runs_the_inventory_script(jobs: dict, job_text: dict) -> None:
    job = jobs["dependency-audit"]
    assert "AC-4" in job["name"]
    assert ".github/scripts/pio_deps_inventory.py" in job_text["dependency-audit"]
    assert "GITHUB_STEP_SUMMARY" in job_text["dependency-audit"]


def test_ac4_job_runs_on_push_and_pull_request(workflow: dict, jobs: dict) -> None:
    assert set(workflow["on"]) == {"push", "pull_request"}
    assert "if" not in jobs["dependency-audit"], "the job must not be conditional on the event"


def test_ac4_inventory_lists_every_declared_library_per_box(
    inventory, fixture_repo: Path, monkeypatch
) -> None:
    monkeypatch.setattr(inventory, "latest_version", lambda owner, library: "9.9.9")

    rows = inventory.collect(fixture_repo)

    assert [(row["box"], row["library"], row["pinned"]) for row in rows] == [
        ("Box A - No Libraries", "-", "-"),
        ("Box B - Two Libraries", "adafruit/DHT sensor library", "^1.4.6"),
        ("Box B - Two Libraries", "fastled/FastLED", "^3.10.3"),
    ]
    assert {row["latest"] for row in rows} == {"-", "9.9.9"}


def test_ac4_inventory_fails_when_a_declared_library_is_not_in_the_registry(
    inventory, fixture_repo: Path, monkeypatch
) -> None:
    def missing(owner: str, library: str) -> str:
        raise inventory.LibraryNotFound(f"{owner}/{library}")

    monkeypatch.setattr(inventory, "latest_version", missing)

    with pytest.raises(SystemExit) as raised:
        inventory.collect(fixture_repo)
    assert raised.value.code == 1


def test_ac4_inventory_does_not_look_up_a_specification_it_cannot_parse(
    inventory, tmp_path: Path, monkeypatch
) -> None:
    make_box(
        tmp_path,
        "Box C - Git Dependency",
        """
        [env:uno]
        platform = atmelavr
        board = uno
        lib_deps =
          https://github.com/example/library.git
          BareLibraryName
        """,
    )
    monkeypatch.setattr(
        inventory,
        "latest_version",
        lambda owner, library: pytest.fail(f"must not query the registry for {owner}/{library}"),
    )

    rows = inventory.collect(tmp_path)
    assert [row["latest"] for row in rows] == [inventory.NOT_CHECKED, inventory.NOT_CHECKED]


def test_ac4_inventory_covers_every_box_in_this_repository(inventory, root: Path) -> None:
    boxes = {box.name for box in inventory.boxes(root)}
    expected = {path.parent.name for path in root.glob("Boxes/*/platformio.ini")}
    assert boxes == expected and boxes


def test_ac4_inventory_renders_a_row_per_library(inventory, fixture_repo: Path, monkeypatch) -> None:
    monkeypatch.setattr(inventory, "latest_version", lambda owner, library: "9.9.9")

    table = inventory.render(inventory.collect(fixture_repo))

    assert "AC-4" in table
    assert "| Box | Env | Platform | Library | Pinned | Latest in registry |" in table
    assert "adafruit/DHT sensor library" in table
    assert "2 boxes, 2 distinct libraries declared." in table


def test_ac4_split_spec(inventory) -> None:
    assert inventory.split_spec("adafruit/DHT sensor library@^1.4.6") == (
        "adafruit",
        "DHT sensor library",
        "^1.4.6",
    )
    assert inventory.split_spec("fastled/FastLED") == ("fastled", "FastLED", "")
    assert inventory.split_spec("BareName") == ("", "BareName", "")
    assert inventory.split_spec("https://github.com/a/b.git") == (
        "",
        "https://github.com/a/b.git",
        "",
    )
