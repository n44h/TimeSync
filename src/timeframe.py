from typing import Tuple
from datetime import datetime, timedelta

# Input Datetime formats.
DATETIME_FORMAT = '%d-%m-%y %H:%M'


class TimeFrame:
    """
    TimeFrame class that encapsulates the UTC offset, start time and end time of a timeframe.
    """

    def __init__(self, utc_offset: str, start_time: datetime | str, end_time: datetime | str) -> None:
        """ Initialize a TimeFrame object with 3 mandatory parameters.

        Args:
            utc_offset (str): UTC offset of the time frame in format ±HH:MM.
            start_time (datetime | str): start time of the time frame.
            end_time (datetime | str): end time of the time frame.
        """

        # Splitting the UTC offset into hour and min.
        self.offset_hour = int(utc_offset[:3])
        self.offset_min = int(utc_offset[4:])

        # UTC Offset string.
        self.utc_offset = f"{'+' if self.offset_hour >= 0 else '-'}{abs(self.offset_hour):02}:{self.offset_min:02}"

        # Create datetime objects for start and end time.
        self.start_time = datetime.strptime(start_time, DATETIME_FORMAT) if type(start_time) is str else start_time
        self.end_time = datetime.strptime(end_time, DATETIME_FORMAT) if type(end_time) is str else end_time

        # Check if the end time is earlier than start time.
        if self.end_time < self.start_time:
            raise ValueError("Illegal TimeFrame attributes: end time cannot be earlier than start time.")

        # Create the time delta object. timedelta accepts negative values in parameters.
        delta = timedelta(hours=self.offset_hour, minutes=self.offset_min)

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
        """ Get the UTC+00:00 normalized start and end times of the TimeFrame.

        Returns:
              Tuple containing the normalized start and end times.
        """

        return self.norm_start_time, self.norm_end_time

    def get_utc_offset(self) -> str:
        """ Get the UTC offset of the TimeFrame.

        Returns:
              a string of the UTC offset in the format ±HH:MM.
        """

        return self.utc_offset

    def to_local_time(self, times: list | tuple) -> list:
        """ Convert UTC +00:00 time to the local timezone of the timeframe.

        Args:
            times: list of datetime objects in UTC +00:00 time that need to be converted to local time.

        Returns:
            list of localized times as strings.
        """

        # Create the time delta object. timedelta accepts negative values in parameters.
        delta = timedelta(hours=self.offset_hour, minutes=self.offset_min)

        # Calculate the localized time for each datetime object in "times" and convert them to strings.
        localized_times = [(time + delta).strftime(DATETIME_FORMAT) for time in times]

        return localized_times

    def get_attributes(self) -> tuple:
        """ Get the attributes of the timeframe.

        Returns:
            a tuple containing the UTC offset, start time, end time, normalized start time, and normalized end time.
        """

        # Convert the start/end times to strings.
        start_time = self.start_time.strftime(DATETIME_FORMAT)
        end_time = self.end_time.strftime(DATETIME_FORMAT)

        # Convert the normalized start/end times to strings.
        norm_start_time = self.norm_start_time.strftime(DATETIME_FORMAT)
        norm_end_time = self.norm_end_time.strftime(DATETIME_FORMAT)

        return self.utc_offset, start_time, end_time, norm_start_time, norm_end_time
