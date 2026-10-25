#!/usr/bin/env bash
# AC-3: scan the repository's history for secrets with gitleaks.
#
# The pinned release binary is used rather than gitleaks-action so the job
# needs no marketplace action, no GITLEAKS_LICENSE and no write permissions.
# Bump GITLEAKS_VERSION and GITLEAKS_SHA256 together.
set -euo pipefail

GITLEAKS_VERSION=${GITLEAKS_VERSION:-8.30.1}
GITLEAKS_SHA256=${GITLEAKS_SHA256:-551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb}

tarball="gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz"
url="https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/${tarball}"

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

echo "::group::install gitleaks $GITLEAKS_VERSION"
curl --fail --silent --show-error --location --output "$workdir/$tarball" "$url"
echo "$GITLEAKS_SHA256  $workdir/$tarball" | sha256sum --check --strict
tar --extract --gzip --file "$workdir/$tarball" --directory "$workdir" gitleaks
echo "::endgroup::"

"$workdir/gitleaks" git --redact --no-banner "$(git rev-parse --show-toplevel)"
