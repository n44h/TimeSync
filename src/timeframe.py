import re
from datetime import datetime, timedelta


# Input Datetime formats.
IN_DATETIME_FORMAT = '%d-%m-%y-%H%M'

# Output Datetime formats.
OUT_DATE_FORMAT = '%d-%m-%y'
OUT_TIME_FORMAT = '%H:%M'
OUT_DATETIME_FORMAT = f'{OUT_DATE_FORMAT} {OUT_TIME_FORMAT}'


class Timezone:
    """
    Timezone class
    """

    def __init__(self, utc_offset: str):
        """ Initialize a Timezone object

        Args:
            utc_offset (str): Should be in format `+HHMM` in 24hr format. e.g. -0200, for UTC-2
        """

        assert type(utc_offset) is str and len(utc_offset) == 5

        self.hour = int(utc_offset[:3])
        self.min = int(utc_offset[3:])


class TimeFrame:
    """
    TimeFrame class that encapsulates the UTC offset, start time and end time of a timeframe
    """

    def __init__(self, utc_offset: str, start_time: str, end_time: str):
        """ Initialize a TimeFrame object with 3 mandatory parameters

        Args:
            utc_offset (int): UTC offset of the time frame in format +HHMM
            start_time (datetime): start time of the time frame
            end_time (datetime): end time of the time frame
        """

        # Create a Timezone object.
        self.timezone = Timezone(utc_offset)

        # Create a regex expression for the datetime format.
        date_format = re.compile(r"[0-3]\d-[0-1]\d-\d{2}-[0-2]\d[0-5]\d")

        # Check that the input strings has the right format.
        if not date_format.match(start_time):
            raise ValueError("\nInvalid start time input. Incorrect format."
                             "\nExpected format: DD-MM-YY-HHMM")

        if not date_format.match(end_time):
            raise ValueError("\nInvalid end time input. Incorrect format."
                             "\nExpected format: DD-MM-YY-HHMM")

        # Create datetime objects for start and end time.
        self.start_time = datetime.strptime(start_time, IN_DATETIME_FORMAT)
        self.end_time = datetime.strptime(end_time, IN_DATETIME_FORMAT)

        # Create the time delta object. timedelta accepts negative values in parameters.
        delta = timedelta(hours=self.timezone.hour, minutes=self.timezone.min)

        # Calculate the normalized times.
        self.norm_start_time = self.start_time + delta
        self.norm_end_time = self.end_time + delta
