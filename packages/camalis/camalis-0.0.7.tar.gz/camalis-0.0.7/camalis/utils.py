from datetime import datetime, timezone


def datetime_to_iso_string(input_date: datetime) -> str:
    """
    Convert a datetime object to string date
    :param input_date: datetime object
    :return: 2011-12-03T10:15:30Z or ex: 2011-12-03T10:15:30-03:00 if timezone is -03:00
    """
    return input_date.isoformat().replace('+00:00', 'Z')


def iso_string_to_datetime(input_date: str) -> datetime:
    """
    Convert a string date to datetime object
    :param input_date: 2011-12-03T10:15:30Z or 2011-12-03T10:15:30+00:00
    :return: datetime object with timezone UTC
    """
    if 'Z' in input_date:
        input_date = input_date.replace('Z', '+00:00')
    date_to_result = datetime.fromisoformat(input_date)
    return date_to_result.astimezone(timezone.utc)
