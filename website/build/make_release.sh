#!/usr/bin/env bash
# Build the site and package a versioned, drag-and-drop zip.
# Usage: bash make_release.sh v1.0
set -euo pipefail
VERSION="${1:?usage: make_release.sh vX.Y}"
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
cd "$HERE"
MMAG_VERSION="$VERSION" python3 build.py
mkdir -p "$REPO/releases"
ZIP="$REPO/releases/mmag-website-$VERSION.zip"
rm -f "$ZIP"
cd "$HERE/../dist"
# index.html sits at the zip root so hosts can serve it directly
zip -qr -X "$ZIP" . -x '.*'
echo "release: $ZIP ($(du -h "$ZIP" | cut -f1))"
unzip -l "$ZIP" | tail -1
