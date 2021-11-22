## Requirements

Install [Poetry](https://python-poetry.org/docs/) in your user folder:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Then log out and log in again.

```bash
git clone git@github.com:antonellopellecchia/gem-testbeam-scripts.git
cd gem-testbeam-scripts
source env.sh
poetry install
```

## Usage

Activate the environment:

```bash
source env.sh
poetry shell
```

Command help:

```bash
$ python3 runs.py -h
usage: runs.py [-h] {list,search,log} ...

positional arguments:
  {list,search,log}  Explore command
    list             List all runs
    search           Search for run
    log              Print run log

optional arguments:
  -h, --help         show this help message and exit
```