'''Работа с содержательной частью информационных пакетов запроса НСИ'''

import os
import uuid
import jinja2

from dars import datastructs as ds
from dars import (
        models,
        utils,
        xml
        )


def render(model: models.GetNsiRequestModel) -> str:
    '''Сгенерировать тело запроса справочника НСИ

    Аргументы:
        model - модель параметров команды
    '''
    if model.base == ds.Base.FZ223:
        raise NotImplementedError
    path = os.path.join(os.path.dirname(__file__), 'templates')
    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=path))
    template = env.get_template('getnsirequest.xml.j2')
    template.globals['now'] = utils.isonow
    template.globals['uuid'] = uuid.uuid4
    return template.render(context=model)


def extract_archive_info(xmlstring: str) -> list[tuple]:
    '''Извлечь информацию об архивах из ответа

    Аргументы:
        xmlstring - xml-строка, содержащая пакет данных getNsiResponse
    Результат:
        Список кортежей (наименование архива, ссылка для скачивания)
    '''
    obj = xml.XmlObject(xmlstring, root_tag='Body/getNsiResponse')
    info = []
    for el in obj.values('dataInfo/nsiArchiveInfo'):
        name = obj.value_of(el, 'archiveName')
        url = obj.value_of(el, 'archiveUrl')
        info.append((name, url))
    return info
