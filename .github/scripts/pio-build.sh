#!/usr/bin/env bash
# AC-1: resolve and build one Boxes/* PlatformIO project.
#
# The workshop boxes ship a platformio.ini as the participant's starting point;
# the sketch itself is what the participant writes, so most boxes carry no
# sources in this repository. `pio run` on such a project exits 1 with
# "Error: Nothing to build". So this script checks two things:
#
#   1. `pio pkg install` must succeed. This is where a broken box is actually
#      caught: an unknown board, a platform that no longer resolves, or a
#      lib_deps pin that has disappeared from the PlatformIO registry.
#   2. `pio run` must succeed whenever the box has sources under src/. It is
#      allowed to stop at PlatformIO's "Nothing to build" only while the box
#      has none - the moment a sketch is committed, a broken build fails here.
set -euo pipefail

box="${1:?usage: pio-build.sh <box directory>}"

if [[ ! -f "$box/platformio.ini" ]]; then
  echo "::error::$box has no platformio.ini"
  exit 1
fi

cd "$box"

echo "::group::pio pkg install - $box"
pio pkg install
echo "::endgroup::"

shopt -s nullglob globstar
sources=(src/**/*.c src/**/*.cc src/**/*.cpp src/**/*.cxx src/**/*.ino src/**/*.S src/**/*.s)
shopt -u nullglob globstar

log=$(mktemp)
trap 'rm -f "$log"' EXIT

echo "::group::pio run - $box"
if pio run 2>&1 | tee "$log"; then
  echo "::endgroup::"
  echo "$box: built ${#sources[@]} source file(s)"
  exit 0
fi
echo "::endgroup::"

if (( ${#sources[@]} == 0 )) && grep -qF 'Error: Nothing to build' "$log"; then
  echo "::notice title=$box::platformio.ini resolves; no sketch committed yet, so there is nothing to build"
  exit 0
fi

echo "::error title=$box::pio run failed"
exit 1
