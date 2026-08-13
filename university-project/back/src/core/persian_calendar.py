"""Small, dependency-free Jalali calendar helpers for API date ranges."""

from datetime import datetime


def _div(value: int, divisor: int) -> int:
    # The original jalaali-js algorithm truncates toward zero.
    return int(value / divisor)


def _jalali_calculation(jalali_year: int) -> tuple[int, int]:
    breaks = [
        -61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210,
        1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178,
    ]
    gregorian_year = jalali_year + 621
    leap_j = -14
    previous_break = breaks[0]
    jump = 0

    for current_break in breaks[1:]:
        jump = current_break - previous_break
        if jalali_year < current_break:
            break
        leap_j += _div(jump, 33) * 8 + _div(jump % 33, 4)
        previous_break = current_break

    offset = jalali_year - previous_break
    leap_j += _div(offset, 33) * 8 + _div((offset % 33) + 3, 4)
    if jump % 33 == 4 and jump - offset == 4:
        leap_j += 1

    leap_g = (
        _div(gregorian_year, 4)
        - _div((_div(gregorian_year, 100) + 1) * 3, 4)
        - 150
    )
    march = 20 + leap_j - leap_g
    return gregorian_year, march


def _gregorian_to_day_number(year: int, month: int, day: int) -> int:
    result = (
        _div((year + _div(month - 8, 6) + 100100) * 1461, 4)
        + _div(153 * ((month + 9) % 12) + 2, 5)
        + day
        - 34840408
    )
    return result - _div(_div(year + 100100 + _div(month - 8, 6), 100) * 3, 4) + 752


def _day_number_to_gregorian(day_number: int) -> tuple[int, int, int]:
    value = 4 * day_number + 139361631
    value += _div(_div(4 * day_number + 183187720, 146097) * 3, 4) * 4 - 3908
    index = _div(value % 1461, 4) * 5 + 308
    day = _div(index % 153, 5) + 1
    month = (_div(index, 153) % 12) + 1
    year = _div(value, 1461) - 100100 + _div(8 - month, 6)
    return year, month, day


def jalali_to_gregorian(jalali_year: int, jalali_month: int, jalali_day: int) -> datetime:
    """Convert a Jalali date to a naive Gregorian datetime at midnight."""
    jalali_year = int(jalali_year)
    jalali_month = int(jalali_month)
    jalali_day = int(jalali_day)
    gregorian_year, march = _jalali_calculation(jalali_year)
    first_day = _gregorian_to_day_number(gregorian_year, 3, march)
    day_number = (
        first_day
        + (jalali_month - 1) * 31
        - _div(jalali_month, 7) * (jalali_month - 7)
        + jalali_day
        - 1
    )
    year, month, day = _day_number_to_gregorian(day_number)
    return datetime(year, month, day)


def jalali_month_range(jalali_year: int, jalali_month: int) -> tuple[datetime, datetime]:
    """Return the inclusive-start/exclusive-end Gregorian range of a Jalali month."""
    jalali_year = int(jalali_year)
    jalali_month = int(jalali_month)
    if not 1 <= jalali_month <= 12:
        raise ValueError("ماه شمسی باید بین ۱ و ۱۲ باشد.")

    start = jalali_to_gregorian(jalali_year, jalali_month, 1)
    if jalali_month == 12:
        end = jalali_to_gregorian(jalali_year + 1, 1, 1)
    else:
        end = jalali_to_gregorian(jalali_year, jalali_month + 1, 1)
    return start, end


def jalali_season_range(jalali_year: int, season: str) -> tuple[datetime, datetime]:
    """Return the Gregorian range for a Persian season in a Jalali year."""
    season_months = {
        "Spring": 1,
        "Summer": 4,
        "Fall": 7,
        "Winter": 10,
    }
    normalized = str(season).strip().capitalize()
    if normalized not in season_months:
        raise ValueError("فصل نامعتبر است.")

    start_month = season_months[normalized]
    start = jalali_to_gregorian(jalali_year, start_month, 1)
    if normalized == "Winter":
        end = jalali_to_gregorian(jalali_year + 1, 1, 1)
    else:
        end = jalali_to_gregorian(jalali_year, start_month + 3, 1)
    return start, end
