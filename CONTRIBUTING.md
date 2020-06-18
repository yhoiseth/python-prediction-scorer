# Contributing

## Create virtual environment

`python3 -m venv venv`

## Activate virtual environment

`source venv/bin/activate.fish`

## Install dependencies

`pip-sync`

## Set up pre-commit hooks

`pre-commit install`

## Check pre-commit hooks

`pre-commit run --all-files`

## Prepare for tests

`pip install -e .`

## Run tests

`pytest`

## Update dependencies

`./update-dependencies.sh`

## Issue checklist

Copy and paste into GitHub:

- [ ] Documentation
- [ ] Tests
- [ ] Implementation
- [ ] Changelog
- [ ] Release

## Create release

### Update version number

Edit in [`setup.py`](setup.py).

### Update Changelog

[CHANGELOG.md](CHANGELOG.md)

### Create distribution

`python setup.py sdist`

### Publish

`twine upload dist/*`

### Commit

`git commit -am 'Release v[version number]`

### Create tag

`git tag -a v[version number] -m "v[version number]"`

### Push

`git push origin v[version number]`

### Create GitHub release

1. [Create new release](https://github.com/yhoiseth/python-prediction-scorer/releases/new)
2. Use the tag — e.g. `v1.0.0` as the release title.
3. Copy-paste the changelog entry into the description.
