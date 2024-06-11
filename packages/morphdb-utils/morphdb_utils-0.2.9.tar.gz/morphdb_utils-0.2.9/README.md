# Morphdb Utils

Morph enables everyone to process data with SQL and Python using AI assist and auto-scale database powered by PostgreSQL.

## How to Contribute

### Setting up the development environment

This project uses [pre-commit](https://pre-commit.com/) to enforce code quality and consistency. To install the pre-commit hooks, run the following command:

```shell
pre-commit install
```

## How to Publish

This project uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To publish a new version of the package, run the following command:

First, update the version in `pyproject.toml` file.

```shell
poetry version patch
git commit -am "Bump version"
git push origin develop
```

```shell
git checkout develop
poetry publish --build
```
