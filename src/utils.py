import os
import re
from datetime import datetime, timedelta
from typing import Tuple


VALID_UTC_OFFSETS = ["-1200", "-1100", "-1000", "-0930", "-0900", "-0800", "-0700", "-0600", "-0500", "-0400",
                     "-0330", "-0300", "-0200", "-0100", "+0000", "-0000", "+0100", "+0200", "+0300", "+0330",
                     "+0400", "+0430", "+0500", "+0530", "+0545", "+0600", "+0630", "+0700", "+0800", "+0845",
                     "+0900", "+0930", "+1000", "+1030", "+1100", "+1200", "+1245", "+1300", "+1400"]

# Input Datetime formats.
IN_DATETIME_FORMAT = '%d-%m-%y %H%M'


def clear_screen() -> None:
    """ Utility function to clear the Terminal. """
    os.system('cls' if os.name == 'nt' else 'clear')


def validate_datetime(in_datetime: str) -> bool:
    """ Validate a datetime string's format.

    Args:
        in_datetime (str): the datetime string input.

    Returns:
        True if the input matches the DD-MM-YY HHMM format.
    """

    # Regex for datetime format.
    datetime_re = re.compile(r"^[0-3]\d-[0-1]\d-\d{2} [0-2]\d[0-5]\d$")

    # Match in_datetime argument with datetime regex.
    return bool(datetime_re.match(in_datetime))


def validate_offset(in_offset: str) -> Tuple[bool, str]:
    """ Validate a UTC offset string.

    Args:
        in_offset (str): the UTC offset string input.

    Returns:
        a tuple (flag, error_message). flag is True if the input matches the ±HHMM format.
    """

    # Flag is True if the utc_offset is valid.
    flag = True
    # Error message to print to the terminal.
    error_message = ""

    # Regex expression for UTC offset.
    offset_re = re.compile(r"^[+,-]\d{4}$")

    # Match in_datetime argument with datetime regex.
    if not offset_re.match(in_offset):
        flag = False
        error_message = "add: Incorrect format of UTC offset. Expected format: ±HHMM."

    elif in_offset in VALID_UTC_OFFSETS:
        flag = False
        error_message = "add: Invalid UTC offset. Provide a valid UTC offset."

    # Return the flag and message.
    return flag, error_message


class Timezone:
    """
    Timezone class.
    """

    def __init__(self, utc_offset: str) -> None:
        """ Initialize a Timezone object.

        Args:
            utc_offset (str): Should be in format `±HHMM` in 24hr format. e.g. -0200, for UTC-2.
        """

        assert type(utc_offset) is str and len(utc_offset) == 5

        self.hour = int(utc_offset[:3])
        self.min = int(utc_offset[3:])

    def __str__(self):
        """ String representation of Timezone object.

        Returns:
              a string of the UTC offset in the format ±HHMM.
        """

        sign = "+" if self.hour >= 0 else "-"
        return f"{sign}{self.hour}{self.min}"


class TimeFrame:
    """
    TimeFrame class that encapsulates the UTC offset, start time and end time of a timeframe.
    """

    def __init__(self, utc_offset: str, start_time: str, end_time: str) -> None:
        """ Initialize a TimeFrame object with 3 mandatory parameters.

        Args:
            utc_offset (int): UTC offset of the time frame in format ±HHMM.
            start_time (datetime): start time of the time frame.
            end_time (datetime): end time of the time frame.
        """

        # Create a Timezone object.
        self.timezone = Timezone(utc_offset)

        # Create datetime objects for start and end time.
        self.start_time = datetime.strptime(start_time, IN_DATETIME_FORMAT)
        self.end_time = datetime.strptime(end_time, IN_DATETIME_FORMAT)

        # Create the time delta object. timedelta accepts negative values in parameters.
        delta = timedelta(hours=self.timezone.hour, minutes=self.timezone.min)

        # Calculate the normalized times.
        self.norm_start_time = self.start_time - delta
        self.norm_end_time = self.end_time - delta

    def get_times(self) -> Tuple[datetime, datetime]:
        """ Get the start and end times of the TimeFrame.

        Returns:
              Tuple of containing the start and end times.
        """

        return self.start_time, self.end_time

    def get_norm_times(self) -> Tuple[datetime, datetime]:
        """ Get the UTC+00 normalized start and end times of the TimeFrame.

        Returns:
              Tuple of containing the normalized start and end times.
        """

        return self.norm_start_time, self.norm_end_time

    def get_utc_offset(self) -> str:
        """ Get the UTC offset of the TimeFrame.

        Returns:
              a string of the UTC offset in the format ±HHMM.
        """

        return str(self.timezone)
