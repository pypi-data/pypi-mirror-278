# Vault Keyring Client

This project provides an installable version of the original community script `vault-keyring-client.py` for Ansible, allowing you to manage vault passwords using your OS's native keyring application.

## Description

The `vault-keyring-client` is a CLI tool to store and retrieve Ansible vault passwords in the keyring. This version is implemented using `typer` for a modern CLI interface, making it easy to use and extend.

## Installation

To install the `vault-keyring-client`, you can use [Poetry](https://python-poetry.org/):

```sh
poetry add git+https://git@github.com/jakob1379/vault-keyring-client.git#main
```

## Usage

```console
$ vault-keyring-client [OPTIONS]
```

**Options**:

* `--vault-id TEXT`: Name of the vault secret to get from keyring
* `--username TEXT`: The username whose keyring is queried
* `--set`: Set the password instead of getting it
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

## Original Script

This project is based on the original `vault-keyring-client.py` script contributed by Matt Martz and Justin Mayer. The original script can be found in the Ansible Community's contrib-scripts repository:

[Original vault-keyring-client.py script](https://github.com/ansible-community/contrib-scripts/blob/main/vault/vault-keyring-client.py)

## License

This project is licensed under the GNU General Public License v3.0 or later. See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) file for details.
