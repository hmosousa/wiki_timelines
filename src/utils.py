import calendar
import re
from datetime import datetime

import requests
from pytz import UTC


def get_html(url: str) -> str | None:
    if url is None:
        return None

    response = requests.get(url)
    if response.ok:
        return response.text


def extract_date(iso_format: str, start: bool = False, end: bool = False):
    pattern = re.compile(r"[-+]?(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z")
    match = pattern.match(iso_format)

    if match:
        year = int(match.group(1))

        month = int(match.group(2))
        if month == 0:
            if start:
                month = 1
            elif end:
                month = 12

        day = int(match.group(3))
        if day == 0:
            if start:
                day = 1
            elif end:
                day = calendar.monthrange(year, month)[1]

        hour = int(match.group(4))
        if hour == 0 and end:
            hour = 23

        minute = int(match.group(5))
        if minute == 0 and end:
            minute = 59

        seconds = int(match.group(6))
        if seconds == 0 and end:
            seconds = 59

        date = datetime(year, month, day, hour, minute, seconds, tzinfo=UTC)
        return date
    else:
        raise Exception(f"Can not parse date {iso_format}.")
