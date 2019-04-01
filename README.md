[![PyPI version](https://badge.fury.io/py/data-genie-mkeshav.svg)](https://badge.fury.io/py/data-genie-mkeshav)
[![CircleCI](https://circleci.com/gh/mkeshav/data-genie.svg?style=svg)](https://circleci.com/gh/mkeshav/data-genie)
[![Documentation Status](https://readthedocs.org/projects/data-genie/badge/?version=latest)](https://data-genie.readthedocs.io/en/latest/?badge=latest)


# Data Genie

Genie that can satisfy your data wish.
Supports generation of fixedwidth, csv and json content

# Install
python3 -m pip install data-genie-mkeshav

# Run tests
- All tests (`docker-compose run --rm test`)
- Single test in a file(`docker-compose run --rm test bash -c "python setup.py develop &&  pytest tests/test_fw.py -k 'test_float'"`)
- `docker inspect --format='{{.Id}} {{.Parent}}'     $(docker images --filter since=<image_id> --quiet)` to check dependent child images

- Detailed [Documentation](https://data-genie.readthedocs.io)

# Sonar Scan
Gitignored .env file contains the SONAR_QUBE_TOKEN variable

- `sonar-scanner -Dsonar.login=$SONAR_QUBE_TOKEN`