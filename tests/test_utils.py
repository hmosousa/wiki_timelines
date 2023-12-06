from datetime import datetime

from src.utils import extract_date


def test_extract_date():
    date = "+1848-08-22T00:00:00Z"
    extracted = extract_date(date)
    assert extracted == datetime(1848, 8, 22)


def test_extract_date_start():
    date = "+1848-00-00T00:00:00Z"
    extracted = extract_date(date, start=True)
    assert extracted == datetime(1848, 1, 1)


def test_extract_date_end():
    date = "+1848-00-00T00:00:00Z"
    extracted = extract_date(date, end=True)
    assert extracted == datetime(1848, 12, 31, 23, 59, 59)
