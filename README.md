[![CircleCI branch](https://img.shields.io/circleci/project/github/mkeshav/data-genie/master.svg)](https://circleci.com/gh/mkeshav/data-genie/tree/master)
[![PyPI version](https://badge.fury.io/py/data-genie-mkeshav.svg)](https://badge.fury.io/py/data-genie-mkeshav)
[![Documentation Status](https://readthedocs.org/projects/data-genie/badge/?version=latest)](https://data-genie.readthedocs.io/en/latest/?badge=latest)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mkeshav_data-genie&metric=alert_status)](https://sonarcloud.io/dashboard?id=mkeshav_data-genie)

# Data Genie

Genie that can satisfy your data wish.

- Supports generation of fixedwidth, csv and json content
- Allows data quality checks to be first class

# Install
python3 -m pip install data-genie

# Run tests
- All tests (`docker-compose run --rm test`)
- Single test in a file(`docker-compose run --rm test bash -c "python setup.py develop &&  pytest tests/test_fw.py -k 'test_float'"`)
- `docker inspect --format='{{.Id}} {{.Parent}}'     $(docker images --filter since=<image_id> --quiet)` to check dependent child images

- Detailed [Documentation](https://data-genie.readthedocs.io)

# Sonar Scan
Gitignored .env file contains the SONAR_CLOUD_TOKEN variable (locally)

- `docker-compose run --rm test ./scan`

# Release
increment version in init.py

- `./tag-master`
- `git push origin master`

Unblock the step in circleci

If you have updated the documentation, login to readthedocs and build latest

# Circle CI

Builds happen on circle ci with github integration

Following environment variables need to be set on circle

- `SONAR_CLOUD_TOKEN`
- `PYPI_API_TOKEN` (Pypi project token to allow publishing)


