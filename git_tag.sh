#!/usr/bin/env bash

set -eu

ver=$(python setup.py --version)
echo "Tagging with version: $ver"
git tag -a v$ver -m "Version $ver Release"
echo "Pushing tags"
git push origin --tags
