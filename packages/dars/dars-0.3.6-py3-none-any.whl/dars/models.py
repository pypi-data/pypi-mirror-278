from datetime import date
import pydantic

from dars import datastructs as ds
from dars import (
        config,
        defaults,
        )


class AppModel(pydantic.BaseModel):
    settings: config.Settings | None = None


class GetNsiRequestModel(AppModel):
    '''Параметры запроса справочника'''
    nsiCode: str
    nsiKind: ds.NsiKind = ds.NsiKind.ALL
    isHidden: bool | None = False
    base: ds.Base = ds.Base.FZ44
    prefix: str = ''


class GetPublicDocsRequestModel(AppModel):
    '''Параметры запроса публичных документов'''
    subsystemtype: str
    regnums: list[str]
    monthinfo: date | None = None
    exactdate: date | None = None
    todayinfo: str | None = pydantic.Field(default=None, pattern=r'^\d+-\d+$')
    offsettimezone: str = defaults.TZ
    base: ds.Base = ds.Base.FZ44
    prefix: str = ''

    @pydantic.computed_field
    def fromhour(self) -> int:
        if self.todayinfo:
            return int(self.todayinfo.split('-')[0])

    @pydantic.computed_field
    def tohour(self) -> int:
        if self.todayinfo:
            return int(self.todayinfo.split('-')[1])
