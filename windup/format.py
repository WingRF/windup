from typing import Union
from collections import namedtuple
from datetime import datetime, date, time as dtime

from windup.rfc3339 import (
    str_usec_to_msec,
    utcnow_to_string as _u_utcnow_to_string,
    now_to_string as _u_now_to_string,
    to_string as _u_to_string
)

# date-time string format separator
sep = namedtuple('sep', ['T', 'space', 'underscore'])('T', ' ', '_')

# date-time string format option
fmt = namedtuple(
    'fmt',
    ['date', 'time', 'msec', 'usec', 'tz', 'utc_z']
)(1, 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 5)

default_fmt = fmt.date | fmt.time | fmt.usec | fmt.tz


def _to_string_fmt(dt_string: str, option: int, sep: str) -> str:
    """Format date-time string."""
    _dts, _no_date, _no_time = '', 0, 0

    if option & fmt.date != 0:
        _dts = dt_string[:10]
    else:
        _no_date = 1

    if option & fmt.time != 0:
        if _no_date:
            _dts += dt_string[11:19]
        else:
            _dts += sep + dt_string[11:19]
    else:
        _no_time = 1

    if option & fmt.usec != 0:
        if _no_time:
            _dts += dt_string[20:26]
        else:
            _dts += dt_string[19:26]
    elif option & fmt.msec != 0:
        if _no_time:
            _dts += str_usec_to_msec(dt_string[20:26])
        else:
            _dts += '.' + str_usec_to_msec(dt_string[20:26])

    if option & fmt.utc_z != 0:
        if dt_string[-6:] in ('+00:00', '-00:00'):
            _dts += 'Z'
        else:
            _dts += dt_string[-6:]
    elif option & fmt.tz != 0:
        _dts += dt_string[-6:]

    return _dts


def _dt_to_string(dt: datetime, option: int, sep: str) -> str:
    """Serialize datetime object to date-time string."""
    return _to_string_fmt(_u_to_string(dt), option=option, sep=sep)


def utcnow_to_string(option: int = default_fmt, sep: str = sep.T) -> str:
    """
    Serialize utcnow datetime object to date-time string.

    Args:
        option: date-time string format option.
                    fmt.date  - format date string
                    fmt.time  - format time string
                    fmt.msec  - format millisecond string
                    fmt.usec  - format microseconds string
                    fmt.tz    - format timezone string
                    fmt.utc_z - use 'Z' instead of '+00:00'
                                if the timezone is UTC.

        sep:    date-time string separator between date and time.
                    sep.T          - 'T'
                    sep.space      - ' '
                    sep.underscore - '_'

    Returns:
        date-time string

    Examples:
        >>> import windup
        >>> windup.utcnow_to_string()
        '2022-07-12T11:18:55.547682+00:00'
        >>> windup.utcnow_to_string(option=windup.fmt.date | windup.fmt.time | windup.fmt.msec)
        '2022-07-13T08:41:15.397'
        >>> windup.utcnow_to_string(option=windup.fmt.date | windup.fmt.time, sep=windup.sep.space)
        '2022-07-13 08:42:32'

    """
    return _to_string_fmt(_u_utcnow_to_string(), option=option, sep=sep)


def now_to_string(option: int = default_fmt, sep: str = sep.T) -> str:
    """
    Serialize now datetime object to date-time string.

    Args:
        option: date-time string format option.
                    fmt.date  - format date string
                    fmt.time  - format time string
                    fmt.msec  - format millisecond string
                    fmt.usec  - format microseconds string
                    fmt.tz    - format timezone string
                    fmt.utc_z - use 'Z' instead of '+00:00'
                                if the timezone is UTC.

        sep:    date-time string separator between date and time.
                    sep.T          - 'T'
                    sep.space      - ' '
                    sep.underscore - '_'

    Returns:
        date-time string

    Examples:
        >>> import windup
        >>> windup.now_to_string()
        '2022-07-12T11:18:55.547000+00:00'
        >>> windup.now_to_string(option=windup.fmt.date | windup.fmt.time | windup.fmt.msec)
        '2022-07-13T16:46:25.120'
        >>> windup.now_to_string(option=windup.fmt.date | windup.fmt.time, sep=windup.sep.space)
        '2022-07-13 16:47:03'

    """
    return _to_string_fmt(_u_now_to_string(), option=option, sep=sep)


def to_string(dt: Union[datetime, date, dtime],
              option: int = default_fmt,
              sep: str = sep.T) -> str:
    """
    Serialize datetime object to date-time string.

    Args:
        dt:     datetime object.
        option: date-time string format option.
                    fmt.date  - format date string
                    fmt.time  - format time string
                    fmt.msec  - format millisecond string
                    fmt.usec  - format microseconds string
                    fmt.tz    - format timezone string
                    fmt.utc_z - use 'Z' instead of '+00:00'
                                if the timezone is UTC.

        sep:    date-time string separator between date and time.
                    sep.T          - 'T'
                    sep.space      - ' '
                    sep.underscore - '_'

    Returns:
        date-time string

    Raises:
        TypeError

    Examples:
        >>> import windup
        >>> windup.to_string(windup.utcnow())
        '2022-07-12T11:18:55.547000+00:00'
        >>> windup.to_string(windup.utcnow(), option=windup.fmt.date | windup.fmt.time | windup.fmt.usec)
        '2022-07-13T08:48:43.524185'
        >>> windup.to_string(windup.utcnow(), option=windup.fmt.date | windup.fmt.time | windup.fmt.utc_z, sep=windup.sep.space)
        '2022-07-13 08:49:21Z'

    """
    _dt = None
    if isinstance(dt, datetime):
        _dt = dt
    elif isinstance(dt, date):
        _dt = datetime(dt.year, dt.month, dt.day)
        option = fmt.date
    elif isinstance(dt, dtime):
        _dt = datetime(
            1970, 1, 1,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            tzinfo=dt.tzinfo
        )
        if option & fmt.date != 0:
            option ^= fmt.date
    else:
        raise TypeError('Expected a datetime/date/time object.')

    return _dt_to_string(_dt, option=option, sep=sep)
