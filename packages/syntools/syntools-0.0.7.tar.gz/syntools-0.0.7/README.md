# Synapse Power Tools

Utilities for using [Synapse](https://www.synapse.org/).

## Dependencies

- [Python3.10+](https://www.python.org/)
- A [Synapse](https://www.synapse.org/) account with a username/password. Authentication through a 3rd party (.e.g.,
  Google) will not work, you must have a Synapse user/pass for
  the [API to authenticate](http://docs.synapse.org/python/#connecting-to-synapse).

## Install

```bash
pip install syntools
```

## Configuration

### Environment Variables

No configuration is necessary if using environment variables or the default synapse config file.
For user/pass, set:

```shell
SYNAPSE_USERNAME=
SYNAPSE_PASSWORD=
```

For auth token, set:

```shell
SYNAPSE_AUTH_TOKEN=
```

For Synapse Config file, have a valid config file in:
`~/.synapseConfig`
Or, have the environment variable set:
`SYNAPSE_CONFIG_FILE=`

### Command Line Arguments

```text
options:
  -u USERNAME, --username USERNAME
                        Synapse username.
  -p PASSWORD, --password PASSWORD
                        Synapse password.
  --auth-token AUTH_TOKEN
                        Synapse auth token.
  --synapse-config SYNAPSE_CONFIG
                        Path to Synapse configuration file.
```

## Usage

```text
usage: syntools [-h] [--version] {download,find-id,copy,move,list} ...

Synapse Power Tools

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Commands:
  {download,find-id,copy,move,list}
    download            Download folders and files from Synapse.
    find-id             Find a Synapse ID by a Synapse path (e.g., MyProject/Folder/file.txt).
    copy                Copy Synapse entities from one container to another.
    move                Move Synapse entities from one container to another.
    list                List Synapse entities in one or more containers.

```

## Development Setup

```bash
pipenv --python 3.10
pipenv shell
make pip_install
make build
make install_local
```

See [Makefile](Makefile) for all commands.

### Testing

- Create and activate a virtual environment:
- Rename [.env-template](.env-template) to [.env](.env) and set each of the variables.
- Run the tests: `make test`
