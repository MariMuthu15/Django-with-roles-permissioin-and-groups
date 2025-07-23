import json
import random
import string
from datetime import datetime, timezone
from secrets import randbelow
from typing import Any


def get_current_utc() -> datetime:
    """Returns the current UTC datetime as a timezone-aware object."""
    return datetime.now(timezone.utc)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Formats a datetime object to a string with the specified format."""
    return dt.strftime(format_str)


def days_to_minutes(day: int) -> int:
    return day * 24 * 60


def generate_random_characters(length: int = 8):
    """

    :param length: number of characters to be generated
    :return: random string contains Upper+Lowercase letters
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def string_to_boolean(value: any):
    return value.lower() in ("yes", "y", "true", "t", "1")


def return_list_to_dict(obj: any):
    """

    :param obj: Any Models Serializer.data
    :return: dict
    """
    ordered_dict_items = json.dumps(obj)
    return json.loads(ordered_dict_items)

def generate_otp(length=6):
    # Calculate the smallest number with the given length
    start = 10 ** (length - 1)

    # Calculate one above the largest number for the given length
    end = 10 ** length

    # Calculate the range (end - start)
    range_size = end - start

    # Generate a random number within the range and shift by the starting value
    otp = str(randbelow(range_size) + start)
    print(f'OTP Length: {otp}')
    return otp

def validate_payload(serializer_class: Any, data: Any) -> Any:
    """
    :param serializer_class: Serializer class
    :param data: data to validate
    """
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data