# Building from source

## Build

- `docker-compose build test`

## Run tests

- All tests (`docker-compose run --rm test`)
- Single test in a file(`docker-compose run --rm test bash -c "python setup.py develop &&  pytest tests/test_fw.py -k 'test_float'"`)
- `docker inspect --format='{{.Id}} {{.Parent}}'     $(docker images --filter since=<image_id> --quiet)` to check dependent child images
- If yo are inside the container just run `python setup.py develop &&  pytest`

## Release

After cloning deploy pre-push hook by copying `pre-push` script to `.git/hooks/pre-push`

- Increment version in init.py
- `./tag-master`
- `git push origin master`

Unblock the step in circleci

If you have updated the documentation, login to readthedocs and build latest

## Circle CI

Builds happen on circle ci with github integration

Following environment variables need to be set on circle

- `PYPI_API_TOKEN` (Pypi project token to allow publishing)

- `CODACY_PROJECT_TOKEN` (Only during builds) 
