import typing as t
from pydantic import BaseModel, HttpUrl, field_validator, IPvAnyAddress, Field
from datetime import datetime


class Event(BaseModel):
    name: str = Field(max_length=32)
    siteId: str = Field(max_length=16)
    sourceIp: IPvAnyAddress
    time: str

    @field_validator('time')
    @classmethod
    def validate_time(cls, time: str):
        datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        return time

    @property
    def py_time(self):
        return datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%SZ")


class PageViewEvent(Event):
    name: t.Literal['PageView']
    pageUrl: HttpUrl
    referrer: str = ""
    prevUrl: str = ""
