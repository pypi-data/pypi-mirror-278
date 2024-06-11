"""Module providing date and time related functions."""

from datetime import UTC, date, datetime, timedelta, timezone
import re


DateLike = date | datetime | str

_DATETIME_REGEX = re.compile(
    r"^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})([T ](?P<hour>\d{2}):(?P<minute>\d{2})(:(?P<second>\d{2}))?)?$"
)


def today_start(tz: timezone = UTC) -> datetime:
    """Get datetime representing today's beginning of day. The default timezone is UTC."""
    t = datetime.now(tz=tz)
    return datetime(t.year, t.month, t.day, 0, 0, 0, tzinfo=tz)


def today_start_end(tz: timezone = UTC) -> tuple[datetime, datetime]:
    """Get two datetime instances representing today's beginning and end of day. The default timezone is UTC."""
    start = today_start(tz)
    end = start + timedelta(days=1)
    return start, end


def yesterday_start(tz: timezone = UTC) -> datetime:
    """Get datetime representing yesterday's beginning of day. The default timezone is UTC."""
    return today_start(tz) - timedelta(days=1)


def yesterday_start_end(tz: timezone = UTC) -> tuple[datetime, datetime]:
    """Get two datetime instances representing yesterday's beginning and end of day. The default timezone is UTC."""
    start = yesterday_start(tz)
    end = start + timedelta(days=1)
    return start, end


def norm_date(v: DateLike) -> date:
    """
    Accept date-like object (date | datetime | str) and if necessary convert it datetime.date.

    :param v: when str than only this format is supported ''
    :raises ValueError: when string could not be parsed
    """
    if isinstance(v, date):
        return v
    if isinstance(v, datetime):
        return v.date()
    dt = parse_date_str(v)
    return dt.date()


def norm_datetime(v: DateLike, tz: timezone = UTC) -> datetime:
    """
    Accept date-like object (date | datetime | str) and if necessary convert it datetime.datetime.

    :param v: when str than only this format is supported ''
    :param tz: timezone to set the datetime to
    :raises ValueError: when string could not be parsed
    """
    if isinstance(v, datetime):
        return v.astimezone(tz)
    if isinstance(v, date):
        return datetime(v.year, v.month, v.day, 0, 0, 0, tzinfo=tz)
    dt = parse_date_str(v)
    return dt.astimezone(tz)


def parse_date_str(s: str) -> datetime:
    """
    Parse string to get datetime.datetime instance.

    :raises ValueError: when string could not be parsed
    """
    m = _DATETIME_REGEX.match(s)
    if not m:
        raise ValueError(f"Invalid datetime string: '{s}'; the format is not supported.")
    year = int(m.group("year"))
    month = int(m.group("month"))
    day = int(m.group("day"))
    hour_str = m.group("hour")
    if not hour_str:
        return datetime(year, month, day, 0, 0, 0)
    hour = int(hour_str)
    minute = int(m.group("minute"))
    second_str = m.group("second")
    if not second_str:
        return datetime(year, month, day, hour, minute, 0)
    second = int(second_str)
    return datetime(year, month, day, hour, minute, second)
