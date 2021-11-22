## Requirements

Install Poetry in your user page, then log out and login again.

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