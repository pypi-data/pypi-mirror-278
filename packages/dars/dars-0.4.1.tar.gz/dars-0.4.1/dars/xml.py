'''Модуль для работы с XML данными'''

import io
import decimal
import xml.etree.ElementTree as ET
from collections import defaultdict


def element_to_dict(t: ET.Element, root_key: bool = True) -> dict:
    '''Преобразовать Element в словарь

    Args:
        t - элемент XML-дерева
        root_key - флаг включения в состав результирующего словаря
            корневого элемента

    @see https://stackoverflow.com/a/10076823/4498602
    '''
    d = {t.tag: {} if t.attrib else None}
    if (children := list(t)):
        dd = defaultdict(list)
        for dc in map(element_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    if root_key:
        return d
    return next(iter(d.values()))


class XmlObject:
    '''Обертка для стандартного класса Xml объекта'''
    def __init__(self, xml_string: str, root_tag=None):
        # --- удаляем пространства имен
        self.tree = ET.iterparse(io.StringIO(xml_string))
        for _, el in self.tree:
            if '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
            for at in list(el.attrib.keys()):
                if '}' in at:
                    newat = at.split('}', 1)[1]
                    el.attrib[newat] = el.attrib[at]
                    del el.attrib[at]
        # ---
        self.root = self.tree.root
        # --- измеяем корень документа при необходимости
        if root_tag:
            self.root = self.root.find(root_tag)
            if not self.root:
                raise ValueError(f'Не найден корневой тег {root_tag}')

    def tree_root_tag(self):
        '''Корневой тег исходного документа

        В отличии от root_tag, корневой тег исходного документа
        всегда указывает в начало документа
        '''
        return self.tree.root.tag

    def value(self, paths: list, converter=None, root: ET = None) -> str:
        '''Получить значение поля

        Возвращается первое ненулевое значение в списке paths
        '''
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            if (el := (root or self.root).find(path)) is None:
                continue
            val = el.text
            if converter:
                val = converter(val)
            return val

    def values(self, paths: list, root: ET = None) -> list:
        '''Получить список значений'''
        if not isinstance(paths, list):
            paths = [paths]
        for path in paths:
            els = (root or self.root).findall(path)
            if len(els) == 0:
                continue
            return els
        return []

    def value_of(self, element, paths, converter=None):
        '''Получить значение относительно заданного элемента дерева'''
        return self.value(paths, converter=converter, root=element)

    @property
    def root_tag(self):
        '''Получить наименование корневого тега (тип документа)'''
        return self.root.tag

    def find(self, path: str) -> ET:
        '''Найти элемент по заданному пути'''
        return self.root.find(path)

    def sum(self, paths, root: ET = None):
        '''Сумма значений в заданых путях'''
        value_sum = 0
        for value in self.values(paths, root=root):
            value_sum += decimal.Decimal(value.text)
        return value_sum

    def to_dict(self, paths: list = None,
                include_root_key: bool = False,
                root: ET = None
                ) -> dict:
        '''Преобразовать элемент по заданному пути в словарь'''
        if paths is None:
            paths = []
        elif not isinstance(paths, list):
            paths = [paths]
        if len(paths) == 0:
            paths = ['.']
        root = root or self.root
        for path in paths:
            element = root.find(path)
            if not element or len(element) == 0:
                continue
            element_dict = element_to_dict(element, include_root_key)
            return element_dict
        return {}
