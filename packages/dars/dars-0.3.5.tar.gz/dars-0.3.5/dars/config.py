'''Глобальная конфигурация

Реализация взята здесь - https://docs.pydantic.dev/latest/concepts/pydantic_settings/#other-settings-source  # noqa
'''

import os

import toml
from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

CONFIG_FILENAME = 'config.toml'


class S3Params(BaseModel):
    '''Секция конфигурации хранилища S3'''
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket: str
    region: str = 'ru-1'


class Settings(BaseSettings):
    '''Корневой класс конфигурации'''
    # --- отправитель запроса
    #     включается в состав XML, который отправляется в СОИ
    sender: str
    # --- адрес для запросов
    #     по-умолчанию - тестовый сервис
    url: str = 'https://int44.zakupki.gov.ru/eis-integration/services/getDocsMis2'  # noqa
    # --- директория для загрузки файлов из СОИ
    download_dir: str = '/tmp/dars/downloads'
    # --- Режим передачи информации
    mode: str = 'PROD'
    # --- секция конфигурации S3
    s3: S3Params | None = None


def load(config_file: str) -> BaseSettings:
    '''Создаем модель конфигурации из заданного файла'''
    class SettingsInitToml(Settings):
        '''Конифгурация из toml-файла

        Подразумевается использование в CLI
        '''
        model_config = SettingsConfigDict(toml_file=config_file)

        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
        ) -> tuple[PydanticBaseSettingsSource, ...]:
            return (TomlConfigSettingsSource(settings_cls),)

    return SettingsInitToml()


def store(config_file: str, model: BaseModel):
    '''Сохранить конфигурацию в файл'''
    abs_path = os.path.abspath(config_file)
    config_dir = os.path.dirname(abs_path)
    os.makedirs(config_dir, exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as file:
        file.write(toml.dumps(model.model_dump()))
