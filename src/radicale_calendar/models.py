from __future__ import annotations

from typing import Literal
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EmptyInput(InputModel):
    pass


class ConfigureInput(InputModel):
    url: str = Field(min_length=1)
    username: str = Field(min_length=1)
    verify_ssl: bool = True
    allow_insecure_http: bool = False

    @model_validator(mode="after")
    def secure_url(self) -> ConfigureInput:
        parsed = urlparse(self.url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("url must be an absolute http or https URL")
        if parsed.username or parsed.password:
            raise ValueError("url must not contain credentials")
        if parsed.scheme == "http" and not self.allow_insecure_http:
            raise ValueError("plain HTTP requires allow_insecure_http=true")
        return self


class RangeInput(InputModel):
    calendar: str = Field(min_length=1)
    start: str = Field(min_length=1)
    end: str = Field(min_length=1)
    timezone: str = Field(min_length=1)


class Recurrence(InputModel):
    frequency: Literal["daily", "weekly", "monthly", "yearly"]
    interval: int = Field(default=1, ge=1, le=999)
    count: int | None = Field(default=None, ge=1)
    until: str | None = None
    by_weekday: list[Literal["MO", "TU", "WE", "TH", "FR", "SA", "SU"]] | None = None

    @model_validator(mode="after")
    def one_ending(self) -> Recurrence:
        if self.count is not None and self.until is not None:
            raise ValueError("recurrence may contain count or until, not both")
        if self.by_weekday and self.frequency != "weekly":
            raise ValueError("by_weekday is supported only for weekly recurrence")
        return self


class EventInput(InputModel):
    uid: str | None = Field(default=None, min_length=1)
    title: str = Field(min_length=1)
    start: str = Field(min_length=1)
    end: str = Field(min_length=1)
    timezone: str = Field(min_length=1)
    all_day: bool = False
    description: str | None = None
    location: str | None = None
    recurrence: Recurrence | None = None


class EventPatch(InputModel):
    title: str | None = Field(default=None, min_length=1)
    start: str | None = Field(default=None, min_length=1)
    end: str | None = Field(default=None, min_length=1)
    timezone: str | None = Field(default=None, min_length=1)
    all_day: bool | None = None
    description: str | None = None
    location: str | None = None
    recurrence: Recurrence | None = None

    @model_validator(mode="after")
    def nonempty(self) -> EventPatch:
        if not self.model_fields_set:
            raise ValueError("event patch must contain at least one field")
        return self


class CreateInput(InputModel):
    calendar: str = Field(min_length=1)
    event: EventInput


class UpdateInput(InputModel):
    calendar: str = Field(min_length=1)
    uid: str = Field(min_length=1)
    etag: str = Field(min_length=1)
    event: EventPatch
    recurrence_scope: str = "series"


class DeleteInput(InputModel):
    calendar: str = Field(min_length=1)
    uid: str = Field(min_length=1)
    etag: str = Field(min_length=1)
    confirm: bool = False
    recurrence_scope: str = "series"
