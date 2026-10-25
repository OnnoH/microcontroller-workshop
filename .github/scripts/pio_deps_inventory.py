#!/usr/bin/env python3
"""AC-4: inventory the PlatformIO libraries declared per box.

PlatformIO has no first-party vulnerability database, so this is an inventory,
not a CVE gate: it renders what every box pins next to the newest version in
the PlatformIO registry, so pins that have drifted behind are visible in the
job summary. It fails only on a declaration that cannot be true - a
`lib_deps` entry whose library does not exist in the registry at all.

Usage: pio_deps_inventory.py [--root DIR] [--output FILE] [--offline]
"""

from __future__ import annotations

import argparse
import configparser
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REGISTRY = "https://api.registry.platformio.org/v3/packages"
TIMEOUT = 30

UNKNOWN = "unknown"
NOT_CHECKED = "not checked"


class LibraryNotFound(Exception):
    """A lib_deps entry names an owner/library the registry does not know."""


def repo_root(start: Path | None = None) -> Path:
    here = (start or Path(__file__).resolve()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "Boxes").is_dir():
            return candidate
    raise SystemExit("could not locate the repository root (no Boxes/ directory found)")


def boxes(root: Path) -> list[Path]:
    """Every Boxes/* directory that carries a platformio.ini, sorted by name."""
    return sorted(
        (path.parent for path in root.glob("Boxes/*/platformio.ini")),
        key=lambda path: path.name,
    )


def parse_ini(path: Path) -> list[dict[str, object]]:
    """The [env:*] sections of one platformio.ini."""
    parser = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
    parser.read(path, encoding="utf-8")

    envs = []
    for section in parser.sections():
        if not section.startswith("env:"):
            continue
        envs.append(
            {
                "env": section[len("env:") :],
                "platform": parser.get(section, "platform", fallback=""),
                "board": parser.get(section, "board", fallback=""),
                "framework": parser.get(section, "framework", fallback=""),
                "lib_deps": [
                    line.strip()
                    for line in parser.get(section, "lib_deps", fallback="").splitlines()
                    if line.strip()
                ],
            }
        )
    return envs


def split_spec(dep: str) -> tuple[str, str, str]:
    """Split `owner/library@^1.2.3` into owner, library and version spec.

    Owner and library come back empty for anything that is not in that form
    (a bare library name, a git URL, a local path) - those are reported but
    not looked up.
    """
    name, _, version = dep.partition("@")
    name, version = name.strip(), version.strip()
    if name.count("/") != 1 or "://" in dep:
        return "", dep, version
    owner, _, library = name.partition("/")
    return owner.strip(), library.strip(), version


def latest_version(owner: str, library: str) -> str:
    """The newest version of a library in the PlatformIO registry."""
    url = f"{REGISTRY}/{urllib.parse.quote(owner)}/library/{urllib.parse.quote(library)}"
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == 404:
            raise LibraryNotFound(f"{owner}/{library}") from error
        raise
    return payload.get("version", {}).get("name", UNKNOWN)


def collect(root: Path, offline: bool = False) -> list[dict[str, str]]:
    """One row per declared library, plus a row per box that declares none."""
    rows: list[dict[str, str]] = []
    missing: list[str] = []

    for box in boxes(root):
        for env in parse_ini(box / "platformio.ini"):
            if not env["lib_deps"]:
                rows.append(
                    {
                        "box": box.name,
                        "env": str(env["env"]),
                        "platform": str(env["platform"]),
                        "library": "-",
                        "pinned": "-",
                        "latest": "-",
                    }
                )
                continue

            for dep in env["lib_deps"]:
                owner, library, pinned = split_spec(dep)
                if offline or not owner:
                    latest = NOT_CHECKED
                else:
                    try:
                        latest = latest_version(owner, library)
                    except LibraryNotFound:
                        latest = "**NOT IN REGISTRY**"
                        missing.append(f"{box.name}: {dep}")
                rows.append(
                    {
                        "box": box.name,
                        "env": str(env["env"]),
                        "platform": str(env["platform"]),
                        "library": f"{owner}/{library}" if owner else library,
                        "pinned": pinned or "(unpinned)",
                        "latest": latest,
                    }
                )

    if missing:
        for entry in missing:
            print(f"::error title=AC-4::library not found in the PlatformIO registry - {entry}", file=sys.stderr)
        raise SystemExit(1)

    return rows


def render(rows: list[dict[str, str]]) -> str:
    libraries = {row["library"] for row in rows if row["library"] != "-"}
    lines = [
        "## AC-4 · PlatformIO library inventory",
        "",
        f"{len({row['box'] for row in rows})} boxes, "
        f"{len(libraries)} distinct libraries declared.",
        "",
        "| Box | Env | Platform | Library | Pinned | Latest in registry |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    lines += [
        "| {box} | `{env}` | `{platform}` | {library} | `{pinned}` | `{latest}` |".format(**row)
        for row in rows
    ]
    lines += [
        "",
        "PlatformIO publishes no vulnerability feed for its registry, so this "
        "table is an inventory rather than a gate: the job fails only when a "
        "declared library is absent from the registry.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    arguments = argparse.ArgumentParser(description=__doc__)
    arguments.add_argument("--root", type=Path, default=None, help="repository root")
    arguments.add_argument("--output", type=Path, default=None, help="write the table here as well as to stdout")
    arguments.add_argument("--offline", action="store_true", help="skip the registry lookups")
    options = arguments.parse_args(argv)

    table = render(collect(repo_root(options.root), offline=options.offline))
    print(table)
    if options.output:
        options.output.write_text(table, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
