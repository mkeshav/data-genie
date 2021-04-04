# Building from source

## Build
- `docker-compose build test`


## Run tests
- All tests (`docker-compose run --rm test`)
- Single test in a file(`docker-compose run --rm test bash -c "python setup.py develop &&  pytest tests/test_fw.py -k 'test_float'"`)
- `docker inspect --format='{{.Id}} {{.Parent}}'     $(docker images --filter since=<image_id> --quiet)` to check dependent child images


## Sonar Scan
Gitignored .env file contains the SONAR_CLOUD_TOKEN variable (locally)

- `docker-compose run --rm test ./scan`

## Release
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
