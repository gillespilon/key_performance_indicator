#! /usr/bin/env python3

from datetime import date, datetime, timezone, timedelta
from pathlib import Path

import kpis


def test_commit_datetimes_since():
    assert kpis.commit_datetimes_since(
            Path('/home/gilles/documents/websites/support.gillespilon.ca/fil/psa_analysis'),
            date(2019, 5, 5),
            date(2019, 5, 11)) == [
        datetime(2019, 5, 11, 7,  9,  51, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 11, 7,  6,  51, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 11, 6,  7,  57, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 11, 6,  3,  47, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 10, 6,  40, 24, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 10, 6,  25, 22, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 10, 6,  6,   7, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 10, 6,  1,  54, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 10, 5,  49, 11, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 10, 5,  25,  5, 0, timezone(offset=timedelta(hours=-5))),
        datetime(2019, 5, 6,  19, 9,  12, 0, timezone(offset=timedelta(hours=-5))),
    ]


if __name__ == '__main__':
    test_commit_datetimes_since()
