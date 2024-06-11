import logging
import os
import shutil
import subprocess
import typer

from dars import (
        __app_name__,
        config
        )

app = typer.Typer()

logger = logging.getLogger('dars')

CONFIG_DIR = typer.get_app_dir(__app_name__)

CONFIG_PATH = os.path.join(
        CONFIG_DIR,
        config.CONFIG_FILENAME
        )


@app.command()
def edit():
    '''Редактировать параметры программы'''
    if not os.path.exists(CONFIG_PATH):
        source_config_path = os.path.join(
                os.path.dirname(__file__),
                'files/config.toml'
                )
        os.makedirs(CONFIG_DIR, exist_ok=True)
        shutil.copy(source_config_path, CONFIG_PATH)
    # ---
    editor = os.environ.get('EDITOR', 'nano')
    subprocess.call([editor, CONFIG_PATH])


@app.command()
def show():
    '''Отобразить параметры программы'''
    if not os.path.exists(CONFIG_PATH):
        typer.echo(
                'Файл конфиуграции не найден. '
                'Выполните команду dars config edit'
                )
        raise typer.Exit(1)
    # ---
    with open(CONFIG_PATH, 'r') as file:
        typer.echo(file.read())
