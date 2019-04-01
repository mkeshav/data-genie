[![PyPI version](https://badge.fury.io/py/data-genie-mkeshav.svg)](https://badge.fury.io/py/data-genie-mkeshav)
[![CircleCI](https://circleci.com/gh/mkeshav/data-genie/tree/master.svg?style=svg&circle-token=ec2327c448c58747d5ded5b95cab2f2371b9a095)](https://circleci.com/gh/mkeshav/data-genie/tree/master)
[![Documentation Status](https://readthedocs.org/projects/data-genie/badge/?version=latest)](https://data-genie.readthedocs.io/en/latest/?badge=latest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mkeshav_data-genie&metric=alert_status)](https://sonarcloud.io/dashboard?id=mkeshav_data-genie)

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
Gitignored .env file contains the SONAR_CLOUD_TOKEN variable (locally)

- `docker-compose run --rm test ./scan`