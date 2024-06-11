from datetime import datetime
import csv
import os
import pathlib
from typing import Annotated

import typer
import pydantic

from dars import datastructs as ds
from dars import config as config_module
from dars import (
        __app_name__,
        __version__,
        cli_config,
        defaults,
        getnsirequest,
        getpublicdocsrequest,
        models,
        main as main_module,
        )

app = typer.Typer()
app.add_typer(
        cli_config.app,
        name='config',
        help='Управление конфигурацией'
        )


CONFIG_PATH = os.path.join(
        typer.get_app_dir(__app_name__),
        config_module.CONFIG_FILENAME
        )


@app.command()
def getPublicDocsRequest(
        subsystemtype: Annotated[
            ds.SubsystemType,
            typer.Option(help='Тип подсистемы для отбора документов')
            ],
        regnum:  Annotated[
            list[str],
            typer.Option(
                help='Организации для отбора документов (код по СПЗ)',
                )
            ] = [],
        organizations: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к csv-файлу c кодами организаций (код по СПЗ)')
            ] = None,
        monthinfo: Annotated[
            datetime,
            typer.Option(
                help='Задать год и месяц отбора документов',
                formats=["%Y-%m"]
                )
            ] = None,
        exactdate: Annotated[
            datetime,
            typer.Option(
                help='Задать дату отбора документов',
                formats=["%Y-%m-%d"]
                )
            ] = None,
        todayinfo: Annotated[
            str,
            typer.Option(help='Задать период в течении суток. Пример: 0-6')
            ] = defaults.TODAY_INFO,
        offsettimezone: Annotated[
            str,
            typer.Option(help='Смещение часового пояса')
            ] = defaults.TZ,
        base: Annotated[
            ds.Base,
            typer.Option(help='Закон (основание)')
            ] = defaults.BASE,
        prefix: Annotated[
            str,
            typer.Option(help='Префикс файла в S3')
            ] = '',
        dry_run: Annotated[
            bool,
            typer.Option(
                help='Вывести XML запроса к СОИ и не выполнять запрос'
                )
            ] = False,
        config: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к файлу конфигурации')
            ] = CONFIG_PATH,
        ):
    '''Получить публичные документы: планы-графики, закупки, контракты'''
    try:
        settings = config_module.load(config)
    except pydantic.ValidationError as e:
        typer.echo('Ошибка конфигурации. Выполните dars config edit')
        raise typer.Exit(1) from e
    # --- реестровые номера организаций
    if organizations:
        with open(organizations, encoding='utf-8', newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            regnums = list(reader)
            regnums = [item[0] for item in regnums]
    else:
        regnums = regnum
    # ---
    params = models.GetPublicDocsRequestModel(
            subsystemtype=subsystemtype,
            regnums=regnums,
            monthinfo=monthinfo,
            exactdate=exactdate,
            todayinfo=todayinfo,
            offsettimezone=offsettimezone,
            base=base,
            prefix=prefix,
            )
    # ---
    if dry_run:
        params.settings = settings
        typer.echo(getpublicdocsrequest.render(params))
        raise typer.Exit(0)
    # ---
    client = main_module.Client(settings)
    client.getPublicDocsRequest(**params.dict())


@app.command()
def getNsiRequest(
        nsiCode: Annotated[
            str,
            typer.Option(
                help='Код справочника. Примеры: '
                'nsiAllList - справочник справочников, '
                'nsiOrganization - справочник организаций')
            ],
        nsiKind: Annotated[
            ds.NsiKind,
            typer.Option(
                help='Вид выгрузки: all - полная, inc - инкрементальнаяx')
            ] = defaults.NSI_KIND,
        hidden: Annotated[
            bool,
            typer.Option(
                help='Признак непубличности справочника'
                )
            ] = defaults.IS_HIDDEN,
        base: Annotated[
            ds.Base,
            typer.Option(help='Закон (основание)')
            ] = defaults.BASE,
        prefix: Annotated[
            str,
            typer.Option(help='Префикс файла в S3')
            ] = '',
        dry_run: Annotated[
            bool,
            typer.Option(
                help='Вывести XML запроса к СОИ и не выполнять запрос'
                )
            ] = False,
        config: Annotated[
            pathlib.Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                help='Путь к файлу конфигурации')
            ] = CONFIG_PATH,
        ):
    '''Получить справочник'''
    try:
        settings = config_module.load(config)
    except pydantic.ValidationError as e:
        typer.echo('Ошибка конфигурации. Выполните dars config edit')
        raise typer.Exit(1) from e
    # ---
    params = models.GetNsiRequestModel(
            nsiCode=nsiCode,
            nsiKind=nsiKind,
            isHidden=hidden,
            base=base,
            prefix=prefix,
            )
    # ---
    if dry_run:
        params.settings = settings
        typer.echo(getnsirequest.render(params))
        raise typer.Exit(0)
    # ---
    client = main_module.Client(settings)
    client.getNsiRequest(**params.dict())


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} {__version__}')
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        '--version',
        '-v',
        help='Отобразить версию программы и выйти.',
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    # pylint: disable=unused-argument,missing-function-docstring
    return
