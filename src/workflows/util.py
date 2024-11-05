from datetime import datetime

import rfc3339
import iso8601


def parse_rfc3339_datetime(value: str) -> datetime:
    date_object = iso8601.parse_date(value)
    rfc_date = rfc3339.format(date_object)
    return datetime.fromisoformat(rfc_date)
