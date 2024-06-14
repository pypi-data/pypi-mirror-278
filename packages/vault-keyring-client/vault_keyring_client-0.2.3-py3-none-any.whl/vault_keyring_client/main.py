import getpass
import sys

import keyring
import typer
from ansible.config.manager import ConfigManager, get_ini_config_value

app = typer.Typer()

KEYNAME_UNKNOWN_RC = 2


def get_config_values():
    """Get default values from Ansible configuration."""
    username = getpass.getuser()
    keyname = "ansible"
    config = ConfigManager()
    if config._config_file:
        username = (
            get_ini_config_value(
                config._parsers[config._config_file],
                dict(section="vault", key="username"),
            )
            or username
        )
        keyname = (
            get_ini_config_value(
                config._parsers[config._config_file],
                dict(section="vault", key="keyname"),
            )
            or keyname
        )
    return username, keyname


@app.command()
def main(
    vault_id: str = typer.Option(
        None, "--vault-id", help="Name of the vault secret to get from keyring"
    ),
    username: str = typer.Option(None, "--username", help="The username whose keyring is queried"),
    set_password: bool = typer.Option(
        False, "--set", help="Set the password instead of getting it"
    ),
):
    """Get or set a password in the keyring."""

    default_username, default_keyname = get_config_values()
    username = username or default_username
    keyname = vault_id or default_keyname

    if set_password:
        typer.echo(f'Storing password in "{username}" user keyring using key name: {keyname}')
        password = getpass.getpass()
        confirm = getpass.getpass("Confirm password: ")
        if password == confirm:
            keyring.set_password(keyname, username, password)
            typer.echo(f"Password for {username} in {keyname} set successfully.")
        else:
            sys.stderr.write("Passwords do not match.\n")
    else:
        password = keyring.get_password(keyname, username)
        if password:
            typer.echo(password)
        else:
            typer.echo("No password found.")
            sys.exit(KEYNAME_UNKNOWN_RC)


if __name__ == "__main__":
    app()
