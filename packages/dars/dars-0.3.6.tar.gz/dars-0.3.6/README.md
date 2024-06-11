# Сервис отдачи информации и документов

Сервис отдачи информации и документов ЕИС (сокр. СОИ) - это сервис для доступа к документам, размещенным на официальном сайте ЕИС.

> С 01.07.2024 выгрузка документов ЕИС на FTP сервер будет прекращена и доступ будет осуществляться только через COИ.

В ЕИС опубликована [инструкция](https://zakupki.gov.ru/epz/main/public/download/downloadDocument.html?id=40288) по работе с данным сервисом.

Настоящий проект представляет собой клиентский модуль на языке Python для взаимодействия с СОИ.

## Быстрый старт

Установка

```bash
pip install dars
```

Использование CLI

```bash
dars config edit
# --- загрузить НСИ
dars getnsirequest --base=fz44  --nsicode=nsiOrganization --nsikind=all

# --- загрузить документы из заданной подсистемы
#     monthinfo, exectdate и todayinfo - взаимоисключающие опции команды
#     organizations и regnum - взаимоисключающие опции команды
dars getpublicdocsrequest \
  --base=fz44 \
  --subsystemtype=PRIZ \
  --monthinfo=2024-04 \      # запрос на заданный месяц
  --exactdate=2024-04-30 \   # запрос на заданный день
  --todayinfo=0-12 \         # запрос на заданный час
  --offsettimezone=UTC+03:00 \
  --organizations=/path/to/file/with/regNum.csv \
  --regnum=regnum1 \
  --regnum=regnum2 \
  --regnum=regnum3
```

Использование модуля

```python
import dars

s3 = {
    "access_key": "key",
    "secret_key": "secret",
    "endpoint_url": "http://localhost:9002",
    "bucket": "drs",
    "region": "ru-1"
}
client = dars.client(sender='myapp', s3=s3)

keys = client.getNsiRequest(
                base='fz44',
                nsicode='nsiOrganization',
                nsikind='all',
		prefix='/fz44/nsi/nsiOrganization'
                )
```

## Особенности реализации

### Ошибка в getPublicDocsResponse

В файле схемы *GetDocsWS/GetDocsMIS/GetDocsMIS-ws-api.xsd* имеется схема *getPublicDocsResponse*,
которая описывает ответ от СОИ с публичными документами: закупки, контракты и т.п.

До версии 14.1.7 интеграция 1 в схеме *getPublicDocsResponse* имеется ошибка:
*dataInfo/orgzanizations44DocsInfo* вместо *dataInfo/organizations44DocsInfo*. Аналогично для 223.
