#!/usr/bin/env bash
# Usage: ./reindex.sh [docs|docs_evil]
set -euo pipefail
TARGET="${1:-docs}"
python indexer.py "$TARGET"
