import os
import sys
from contextlib import contextmanager
from pathlib import Path

import click
from django.core.management import execute_from_command_line

import hamilton


@contextmanager
def extend_sys_path(path):
    original_sys_path = sys.path[:]
    try:
        sys.path.insert(0, path)
        yield
    finally:
        sys.path = original_sys_path


# Usage

# Perform operations that require importing modules from the specified path


def cli():
    pass


@contextmanager
def set_env_variables(vars: dict):
    original_values = {}
    try:
        # Set new values and store original values
        for key, value in vars.items():
            original_values[key] = os.getenv(key)
            os.environ[key] = value
        yield
    finally:
        # Restore original values or delete if they were not set originally
        for key in vars:
            if original_values[key] is None:
                del os.environ[key]
            else:
                os.environ[key] = original_values[key]


@click.command()
@click.option("--port", default=8241, help="Port to run the server on.")
@click.option(
    "--base-dir",
    default=os.path.join(Path.home(), ".hamilton", "db"),
    help="Base directory for the server -- stores data"
)
@click.option(
    "--no-migration",
    is_flag=True,
    help="Do not run migrations."
)
def run(
    port: int,
    base_dir: str,
    no_migration: bool
):
    env = {
        "DJANGO_SETTINGS_MODULE": "hamilton.server.server.settings_mini",
        "HAMILTON_BASE_DIR": base_dir
    }
    with set_env_variables(env):
        with extend_sys_path(os.path.join(*hamilton.__path__, "server")):
            if not no_migration:
                execute_from_command_line([
                    'manage.py',
                    'migrate',
                    '--settings=server.settings_mini']
                )
            execute_from_command_line([
                'manage.py',
                'runserver',
                '--settings=server.settings_mini',
                f'0.0.0.0:{port}']
            )
