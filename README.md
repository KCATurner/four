# Four
Utility for finding the first occurring n-length four-chains.

# For Users
## Install
```shell
pip install git+https://github.com/KCATurner/four.git
```

## CLI
```shell
four --help
```

# For Developers
## Setup
```shell
git clone https://github.com/KCATurner/four.git && cd four
pip install -r devreqs.txt
pip install -e .
```

## Static Analysis
```shell
flake8
```
Static analysis report located in [.flake8](.flake8)

## Testing & Coverage
```shell
pytest
```
JUnitXML unit test results: [.pytest/results.xml](.pytest/results.xml)

CoberturaXML coverage report: [.pytest/coverage.xml](.pytest/coverage.xml)

Static HTML coverage report: [.pytest/coverage-html](.pytest/coverage-html)

## Build Docs
```shell
sphinx-build -aETb html docs/source docs/build
```
Documentation located in [docs/build](docs/build)
