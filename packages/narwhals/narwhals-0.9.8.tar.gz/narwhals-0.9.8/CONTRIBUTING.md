# Contributing

Thank you for your interest in contributing to Narwhals! Any kind of improvement is welcome!

## Setting up your environment

Here's how you can set up your local development environment to contribute:

1. Make sure you have Python3.9+ installed
2. Create a new virtual environment with `python3.11 -m venv .venv` (or whichever version of Python3.9+ you prefer)
3. Activate it: `. .venv/bin/activate`
4. Install Narwhals: `pip install -e .`
5. Install test requirements: `pip install -r requirements-dev.txt`
6. Install docs requirements: `pip install -r docs/requirements-docs.txt`

You should also install pre-commit:
```
pip install pre-commit
pre-commit install
```
This will automatically format and lint your code before each commit, and it will block the commit if any issues are found.

## Running tests

To run tests, run `pytest`. To check coverage: `pytest --cov=narwhals`.
To run tests on the docset-module, use `pytest narwhals --doctest-modules`.

## Building docs

To build the docs, run `mkdocs serve`, and then open the link provided in a browser.
The docs should refresh when you make changes. If they don't, press `ctrl+C`, and then
do `mkdocs build` and then `mkdocs serve`.

## How it works

If Narwhals looks like underwater unicorn magic to you, then please read
[how it works](https://narwhals-dev.github.io/narwhals/roadmap/).

## Happy contributing!

Please remember to abide by the code of conduct, else you'll be conducted away from this project.
