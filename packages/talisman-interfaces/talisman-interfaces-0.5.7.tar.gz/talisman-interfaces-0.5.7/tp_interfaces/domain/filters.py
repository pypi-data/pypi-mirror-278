from functools import singledispatch

from tdm.abstract.datamodel import AbstractValue
from tdm.datamodel.values import DateTimeValue, DoubleValue, GeoPointValue, IntValue, StringValue, TimestampValue


@singledispatch
def get_filters(value: AbstractValue) -> dict:
    raise NotImplementedError


@get_filters.register
def _string_filter(value: StringValue) -> dict:
    return {"stringFilter": {"str": value.value.replace('"', '?')}}  # see TKL-987


def _int_timestamp_filter(value: IntValue | TimestampValue) -> dict:
    return {"intFilter": {"start": value.value, "end": value.value}}


@get_filters.register
def _int_filter(value: IntValue) -> dict:
    return _int_timestamp_filter(value)


@get_filters.register
def _timestamp_filter(value: TimestampValue) -> dict:
    return _int_timestamp_filter(value)


@get_filters.register
def _double_filter(value: DoubleValue) -> dict:
    return {"doubleFilter": {"start": value.value, "end": value.value}}


@get_filters.register
def _date_time_filter(value: DateTimeValue) -> dict:
    date_filter = {"date": value.date.__dict__}
    if value.time:
        date_filter["time"] = value.time.__dict__

    return {"dateTimeFilter": {"start": date_filter, "end": date_filter}}


@get_filters.register
def _geo_filter(value: GeoPointValue) -> dict:
    geo_filter = {"radius": 0.0001}
    if value.point:
        geo_filter["point"] = value.point.__dict__
    if value.name:
        geo_filter["name"] = value.name

    return {"geoFilter": geo_filter}
