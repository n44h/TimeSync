from datetime import datetime, timedelta


class Timezone:
    """
    Timezone class
    """

    def __init__(self, utc_offset: str):
        """ Initialize a Timezone object
        Args:
            utc_offset (str): Should be in format `+HHMM` in 24hr format. e.g. -0200, for UTC-2.
        """

        assert type(utc_offset) is str and len(utc_offset) == 5

        self.hour = int(utc_offset[:3])
        self.min = int(utc_offset[3:])


class TimeFrame:
    """
    TimeFrame class that encapsulates the UTC offset and the start/end times of a timeframe.
    """

    def __init__(self, utc_offset: str, start_time: datetime, end_time: datetime):
        """ Initialize a TimeFrame object with 3 mandatory parameters

        Args:
            utc_offset (int): UTC offset of the time frame in format +HHMM
            start_time (datetime): start time of the time frame
            end_time (datetime): end time of the time frame
        """

        # Create a Timezone object.
        self.timezone = Timezone(utc_offset)

        self.start_time = start_time
        self.end_time = end_time

        # Create the time delta object. timedelta accepts negative values in parameters.
        delta = timedelta(hours=self.timezone.hour, minutes=self.timezone.min)

        # Calculate the normalized times.
        self.norm_start_time = self.start_time + delta
        self.norm_end_time = self.end_time + delta
