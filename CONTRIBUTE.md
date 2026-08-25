# Building from source

## Build

- `docker-compose build test`

## Run tests

- All tests (`docker-compose run --rm test`)
- Single test in a file(`docker-compose run --rm test bash -c "python setup.py develop &&  pytest tests/test_fw.py -k 'test_float'"`)
- `docker inspect --format='{{.Id}} {{.Parent}}'     $(docker images --filter since=<image_id> --quiet)` to check dependent child images
- If you are inside the container just run `python setup.py develop &&  pytest`

## Release

After cloning deploy pre-push hook by copying `pre-push` script to `.git/hooks/pre-push`

- Increment version in init.py
- `./tag-master`
- `git push origin master`

Approve the `pypi` environment deployment in GitHub Actions

If you have updated the documentation, login to readthedocs and build latest

## GitHub Actions

Builds happen on GitHub Actions (`.github/workflows/ci.yml`)

Following secrets need to be set on the repo

- `PYPI_API_TOKEN` (Pypi project token to allow publishing)

- `CODACY_PROJECT_TOKEN` (Only during builds)
