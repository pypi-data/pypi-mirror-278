'''Входная точка бизнес-логии модуля'''

import os
import logging
import requests

from dars import (
        config,
        errors,
        getnsirequest,
        getpublicdocsrequest,
        models,
        s3_repo,
        utils,
        )

logger = logging.getLogger('dars')

TRIM_REQUEST_LOG = 1024
TRIM_RESPONSE_LOG = 1024


class Client:
    '''Клинетский класс для доступа к бизнес-логике'''

    def __init__(self, settings: config.Settings):
        self.settings = settings
        self.repo = s3_repo.S3Repo(self.settings.s3)

    def getNsiRequest(self, **kwargs):
        '''Загрузить справочники НСИ'''
        self.params = models.GetNsiRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getnsirequest.render(self.params)
        response_text = self._make_request(body)
        for (_, url) in getnsirequest.extract_archive_info(response_text):
            self._process_response_link(url)

    def getPublicDocsRequest(self, **kwargs):
        '''Загрузить публичные документы'''
        self.params = models.GetPublicDocsRequestModel(**kwargs)
        self.params.settings = self.settings
        body = getpublicdocsrequest.render(self.params)
        response_text = self._make_request(body)
        for (_, urls) in getpublicdocsrequest.extract_archive_info(
                response_text
                ):
            for url in urls:
                self._process_response_link(url)

    def _process_response_link(self, url: str):
        '''Обработать ссылку из СОИ

        Ссылка, полученная из СОИ, указывает на архив документов.
        Му получаем имя файла, проверяем наличие файла в ФС и S3,
        загружаем файл в S3
        '''
        filename = self._get_remote_filename(url)
        # --- проверяем существование файла в S3
        if self.repo.exists(filename, prefix=self.params.prefix):
            logger.debug(
                    'Файл уже существует: %s',
                    os.path.join(self.params.prefix, filename)
                    )
            return
        # --- проверяем существование файла в файловой системе
        download_dir = self.settings.download_dir
        file_path = os.path.join(download_dir, filename)
        if os.path.exists(file_path):
            logger.debug('Файл уже существует в ФС: %s', file_path)
        else:
            # --- загружаем файл из СОИ в ФС
            self._download_file(url, file_path)

        size = utils.humanize_size(os.path.getsize(file_path))
        logger.info('%10s %s/%s', size, self.params.prefix, filename)
        # --- выгружаем файл из ФС в S3
        self.repo.put_file(file_path, prefix=self.params.prefix)

    def _make_request(self, body: str) -> str:
        '''Выполнить запрос к СОИ

        Args:
            body - тело запроса
        Returns:
            Текст ответа
        '''
        logger.debug('Выполнение запроса на %s', self.settings.url)
        logger.debug(utils.truncate_string(body, TRIM_REQUEST_LOG))
        response = requests.post(self.settings.url, data=body, timeout=300)
        logger.debug('HTTP код ответа: %s', response.status_code)
        logger.debug(utils.truncate_string(response.text, TRIM_RESPONSE_LOG))
        # logger.debug('Размер ответа: %d', len(response.text))
        if response.status_code != 200:
            raise errors.EisClientError(
                    'СОИ вернул неожиданный статус ответа '
                    f'{response.status_code}'
                    )
        return response.text

    def _download_file(self, url: str, file_path: str) -> str:
        '''Скачать файл

        Args:
            url - ссылка для скачивания
            file_path - полный путь к файлу
        Return:
            Полный путь файла в файловой системе
        raises:
            EisClientUnexpectedStatus - СОИ вернул не 200
        '''
        download_dir = os.path.dirname(file_path)
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        # ---
        response = requests.get(url, timeout=300)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            # size = utils.humanize_size(os.path.getsize(file_path))
            # logger.info('%10s %s', size, file_path)
            return file_path
        raise errors.EisClientUnexpectedStatus(response.status_code)

    def _get_remote_filename(self, url: str) -> str:
        '''Получить имя файла без скачивания'''
        response = requests.head(url, timeout=300)
        content_disposition = response.headers.get('content-disposition')
        filename = content_disposition.split('=')[1][1:-1]
        return filename
