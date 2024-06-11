''' Хранилище в S3 '''

import re
import os
import threading
import time
import boto3
import botocore


from dars import config


class S3Repo:
    def __init__(self, params: config.S3Params):
        self.client = boto3.client('s3',
                                   endpoint_url=params.endpoint_url,
                                   aws_access_key_id=params.access_key,
                                   aws_secret_access_key=params.secret_key,
                                   region_name=params.region)
        self.bucket = params.bucket
        self.lock = threading.Lock()

    def ls(self,
           prefix: str = '',
           limit: int = 1000,
           pattern: str = '',
           start_after: str = '') -> list[str]:
        '''Список файлов с заданным префиксом

        Attributes:
            prefix: фильтр списка по префиксу файла
            limit: максимальное количество файлов в списке
            start_after: выдавать файлы после заданного
        '''
        with self.lock:
            resp = self.client.list_objects_v2(Bucket=self.bucket,
                                               Prefix=prefix,
                                               StartAfter=start_after,
                                               MaxKeys=limit)
            keys = []
            regex = re.compile(pattern)
            for item in resp.get('Contents', []):
                key = item.get('Key')
                # --- test key with regex pattern
                if pattern:
                    if not regex.search(key):
                        continue
                # ---
                keys.append(key)
            return keys

    def lsgen(self, *args, **kargs):
        '''Генератор пачек файлов заданного размера'''
        last_key = ''
        while keys := self.ls(*args, **kargs, start_after=last_key):
            last_key = keys[-1]
            yield keys

    def rm(self, keys: list):
        objects = [{'Key': key} for key in keys]
        return self.client.delete_objects(Bucket=self.bucket,
                                          Delete={'Objects': objects,
                                                  'Quiet': True})

    def put_file(self, file: str, prefix: str = '', max_retries: int = 2):
        '''Загрузить файл в хранилище

        Args:
            file - путь к файлу в файловой системе
            prefix - префикс ключа файла в S3
            max_retries - количество попыток загрузки в S3
        '''
        with self.lock:
            for _ in range(max_retries):
                try:
                    self.client.upload_file(
                            file,
                            self.bucket,
                            os.path.join(
                                prefix.lstrip('/'),
                                os.path.basename(file)
                                ),
                            )
                    return
                except Exception as e:
                    last_exception = e
                    time.sleep(1)
            raise last_exception

    def locked(self) -> bool:
        '''Репозиторий заблокирован задачей'''
        return self.lock.locked()

    def exists(self, file: str, prefix: str = '') -> bool:
        '''Файл существует -> true, файл не существует -> false'''
        key = os.path.join(
                prefix.lstrip('/'),
                os.path.basename(file)
                )
        try:
            self.client.head_object(
                    Bucket=self.bucket,
                    Key=key
                    )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise e
        return True
