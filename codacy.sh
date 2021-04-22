#!/usr/bin/env bash

set -eu

echo "Generate coverage and test report"
python3 setup.py develop && pytest --cov=genie_pkg --cov-report=xml

bash <(curl -Ls https://coverage.codacy.com/get.sh) report -r coverage.xml \
    --project-token "$CODACY_PROJECT_TOKEN" \
    --organization-provider gh \
    --username mkeshav \
    --commit-uuid "$CIRCLE_WORKFLOW_ID" \
    --project-name data-genie