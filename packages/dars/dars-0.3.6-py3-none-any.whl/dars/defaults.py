'''Значения по умолчанию'''
from datetime import datetime

from dars import datastructs as ds

BASE = ds.Base.FZ44

NSI_KIND = ds.NsiKind.ALL

IS_HIDDEN = False

TODAY_INFO = f'0-{datetime.now().hour}'

TZ = '+3'
