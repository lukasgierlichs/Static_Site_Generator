#!/usr/bin/env bash
# Build the site for production by passing the repository name as basepath
set -euo pipefail

REPO_NAME="Static_Site_Generator"
python3 src/main.py "/${REPO_NAME}/"

echo "Build complete: basepath=/${REPO_NAME}/"
