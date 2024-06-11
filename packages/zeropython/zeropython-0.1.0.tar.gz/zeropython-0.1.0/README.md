# ZeroPython

## Setup

### Install

```bash
pip install zeropython
```

## Dev

This configuration include everything needed to develop and test and check quality of the project.

### Setup

```bash
pip install -e .[ALL]
pre-commit install
pre-commit autoupdate
```

### Run quality checks manually

If you want to run pre-commit checks manually, you can run:

```bash
pre-commit run --all-files
```

## Tests

### Setup

> ⚠️ You can pass this step if you have installed the dev environment `[DEV]`.

Setup your environment for tests:

```bash
pip install -e .[TEST]
```

### Run tests

```bash
pytest -v --strict-markers
```

## Share package

### Setup

Make sure you have installed build requirements:

```bash
python -m pip install --upgrade pip
pip install -r build_requirements.txt
```

### Build package

To release a new version of the package, you can run:

```bash
python -m build
```

Find package in `dist/` folder.
