from fastapi import HTTPException
from datetime import datetime, timezone

def check_date_time_validity(datetime_object):
    """
    Ensures that the datetime object is in UTC and that the date is not before the founding of the Wolt company.

    Args:
        datetime_object (datetime): The datetime object to validate.

    Raises:
        HTTPException: If validation fails.
    """
    UTC = timezone.utc
    tz = datetime_object.tzinfo
    if tz is None or tz != UTC:
        raise HTTPException(status_code=400, detail="Timezone must be specified and in UTC")

    if datetime_object.date() < datetime.date(datetime(2014, 10, 6)):
        raise HTTPException(status_code=400, detail="The Wolt company was not founded before 6 October 2014")
