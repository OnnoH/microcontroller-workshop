#!/usr/bin/env bash
# AC-1: print the Boxes/* directories that carry a platformio.ini, as a JSON
# array, for use as a GitHub Actions matrix. Box names contain spaces, so the
# list has to travel as JSON rather than as a whitespace-separated string.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

find Boxes -mindepth 2 -maxdepth 2 -name platformio.ini -printf '%h\n' |
  sort |
  python3 -c 'import json, sys; print(json.dumps([line.rstrip("\n") for line in sys.stdin]))'
