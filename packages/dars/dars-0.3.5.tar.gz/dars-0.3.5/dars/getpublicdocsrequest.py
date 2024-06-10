'''Работа с содержательной частью информационных пакетов запроса НСИ'''

import os
import uuid
import jinja2

from dars import datastructs as ds
from dars import (
        models,
        utils,
        xml,
        )


def render(model: models.GetPublicDocsRequestModel) -> str:
    '''Сгенерировать тело запроса публичных документов

    Аргументы:
        model - модель параметров команды
    '''
    if model.base == ds.Base.FZ223:
        raise NotImplementedError
    path = os.path.join(os.path.dirname(__file__), 'templates')
    env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=path))
    template = env.get_template('getpublicdocsrequest.xml.j2')
    template.globals['now'] = utils.isonow
    template.globals['uuid'] = uuid.uuid4
    return template.render(context=model)


def extract_archive_info(xmlstring: str,
                         base: ds.Base = ds.Base.FZ44
                         ) -> list[tuple]:
    '''Извлечь документы организаций

    Аргументы:
        xmlstring - xml-строка, содержащая пакет данных getPublicDocsRequest
    Результат:
        Список кортежей (код по СПЗ, ссылка для скачивания)
    '''
    if base == ds.Base.FZ223:
        raise NotImplementedError
    obj = xml.XmlObject(xmlstring, root_tag='Body/getPublicDocsResponse')
    info_path = 'dataInfo/orgzanizations44DocsInfo/orgzanization44DocsInfo'
    info = []
    for el in obj.values(info_path):
        regnum = obj.value_of(el, 'orgzanization44Info/regNum')
        urls = [url.text for url in obj.values('archiveUrl', root=el)]
        info.append((regnum, urls))
    return info
