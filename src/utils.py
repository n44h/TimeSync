import os
import re
from typing import Tuple
from datetime import datetime, timedelta


VALID_UTC_OFFSETS = ["-12:00", "-11:00", "-10:00", "-09:30", "-09:00", "-08:00", "-07:00", "-06:00", "-05:00", "-04:00",
                     "-03:30", "-03:00", "-02:00", "-01:00", "-00:00", "+00:00", "+01:00", "+02:00", "+03:00", "+03:30",
                     "+04:00", "+04:30", "+05:00", "+05:30", "+05:45", "+06:00", "+06:30", "+07:00", "+08:00", "+08:45",
                     "+09:00", "+09:30", "+10:00", "+10:30", "+11:00", "+12:00", "+12:45", "+13:00", "+14:00"]


def clear_screen() -> None:
    """ Utility function to clear the Terminal. """
    os.system('cls' if os.name == 'nt' else 'clear')


def format_time(time_str: str) -> str:
    """ Rectifies incorrectly formatted start/end time strings.

    Args:
        time_str: the time string to format.

    Returns:
        the time string with the correct format.

    """

    """ 
    NOTE: Correct time string format: HH:MM 
    """

    """ Validation 1 """
    # time_str should not contain more than 1 colon character.
    if time_str.count(":") > 1:
        raise ValueError("time string cannot contain more than one \":\" character.")

    # Check 1
    #
    # Time string is empty or only contains a colon.
    #
    if time_str in {"", ":"}:
        return "00:00"

    """ Validation 2 """
    # Besides one colon ":" character, time_str should only contain digits.
    if time_str.replace(":", "").isdigit() is False:
        raise ValueError("time strings can only contain digits and \":\" characters.")

    # Get the time string length.
    length = len(time_str)

    # Check 2
    #
    # String contains only a single digit.
    #
    # Possible inputs:  4 -> 04:00
    #
    if length == 1:
        return f"0{time_str}:00"

    # Check 3
    #
    # Contains 2 digits, assume the 2 digits refer to hour.
    #
    # Possible inputs:  12 -> 12:00
    #                   04 -> 04:00
    #
    elif length == 2:
        return f"{time_str}:00"

    # Check 4
    #
    # Contains 3 digits.
    #
    # Assume first digit belongs to hour and last 2 digits belong to minutes.
    #
    # Possible inputs:  425 -> 04:25
    #
    elif length == 3 and ":" not in time_str:
        return f"0{time_str[0]}:{time_str[1:]}"

    # Check 5
    #
    # Contains 2 digits and a colon.
    #
    # Possible inputs:  :30 -> 00:30
    #                   4:5 -> 04:05
    #                   12: -> 12:00
    #
    elif length == 3 and ":" in time_str:
        # Get the index of the colon character.
        colon_index = time_str.index(":")

        # For type: ":30" -> "00:30"
        if colon_index == 0:
            return f"00{time_str}"

        # For type: "4:5" -> "04:05"
        elif colon_index == 1:
            return f"0{time_str[0:2]}0{time_str[-1]}"

        # For type: "12:" -> "12:00"
        else:
            return f"{time_str}00"

    # Check 6
    #
    # Contains 4 digits.
    #
    # First 2 digits belong to hour and last 2 digits belong to minutes.
    #
    # Possible inputs:  1125 -> 11:25
    #
    elif length == 4 and ":" not in time_str:
        return f"{time_str[0:2]}:{time_str[2:]}"

    # Check 7
    #
    # Contains 3 digits and a colon.
    #
    # Possible inputs:  1:30 -> 01:30
    #                   14:5 -> 14:05
    #                   :125 -> raise ValueError
    #                   125: -> raise ValueError
    #
    elif length == 4 and ":" in time_str:
        # Get the index of the colon character.
        colon_index = time_str.index(":")

        # For type: "1:30" -> "01:30"
        if colon_index == 1:
            return f"0{time_str}"

        # For type: "14:5" -> "14:05"
        elif colon_index == 2:
            return f"{time_str[0:3]}0{time_str[-1]}"

        # For type where colon is in index 0 or 3.
        else:
            raise ValueError("invalid time string format.")

    # Check 8
    #
    # Contains 5 digits.
    #
    # Possible inputs:  15:00 -> valid input
    #                   other -> raise ValueError
    #
    elif length == 5:
        if time_str.index(":") == 2:
            return time_str
        else:
            raise ValueError("invalid time format.")

    # length > 5, raise ValueError.
    else:
        raise ValueError("invalid time format.")


def format_utc_offset(utc_offset_str: str) -> str:
    """ Rectifies incorrectly formatted UTC offset strings.

    Args:
        utc_offset_str: utc offset string to format.

    Returns:
        the UTC offset string with the correct format.

    """

    """ 
    NOTE: Correct UTC offset string format: ±HH:MM
    """

    # If the utc_offset_str contains a sign.
    if utc_offset_str[0] in ["+", "-"]:
        sign = utc_offset_str[0]
        time_str = format_time(utc_offset_str[1:])

    # If sign is missing, assign sign as "+".
    else:
        sign = "+"
        time_str = format_time(utc_offset_str)

    return f"{sign}{time_str}"


def format_date(date_str: str) -> str:
    """ Rectifies incorrectly formatted date strings.

    Args:
        date_str: date string to format.

    Returns:
        the date string with the correct format.
    """

    # If a "*" is inputted, return the current system date.
    if date_str == "*":
        # Get current date.
        dt = datetime.today()

        return dt.strftime("%d-%m-%y")

    # If a "*" is followed by one or more "+", add as many days to today's date as there are "+" signs.
    # e.g. if today is 12-08-22, the input "*+++" would have the output "15-08-22".
    elif set(date_str) == {"*", "+"} or {"+"} == set(date_str):
        # How many days to add.
        iterations = date_str.count("+")

        # Get current date.
        dt = datetime.today()

        # Create timedelta object for 1 day.
        delta = timedelta(days=1)

        # Add the specified number of days.
        for i in range(iterations):
            dt += delta

        return dt.strftime("%d-%m-%y")

    else:
        return date_str


def is_valid_datetime(in_datetime: str) -> bool:
    """ Checks if a datetime string has the format DD-MM-YYYY HH:MM.

    Args:
        in_datetime (str): the datetime string input.

    Returns:
        True if the input matches the DD-MM-YY HH:MM format.
    """

    # Regex for datetime format.
    datetime_re = re.compile(r"^[0-3]\d-[0-1]\d-\d{2} [0-2]\d:[0-5]\d$")

    # Match in_datetime argument with datetime regex.
    return bool(datetime_re.match(in_datetime))


def is_valid_offset(input_offset: str) -> Tuple[bool, str]:
    """ Validate a UTC offset string.

    Args:
        input_offset (str): the UTC offset string input.

    Returns:
        a tuple (flag, error_message). flag is True if the input matches the ±HH:MM format.
    """

    # Flag is True if the input_offset is valid.
    flag = True
    # Error message to print to the terminal.
    error_message = ""

    # Regex expression for UTC offset.
    offset_re = re.compile(r"^[+,-]\d{2}:\d{2}$")

    # Match input_offset argument with offset regex.
    if not offset_re.match(input_offset):
        flag = False
        error_message = "Incorrect format of UTC offset. Expected format: ±HH:MM."

    elif input_offset not in VALID_UTC_OFFSETS:
        flag = False
        error_message = "Invalid UTC offset. Provide a valid UTC offset."

    # Return the flag and message.
    return flag, error_message


def get_duration_string(minutes: int) -> str:
    """ Builds a string of format "DD days HH hours MM minutes" from inputted minutes.

    Args:
        minutes (int): input in minutes.

    Returns:
        a string in the format "DD days HH hours MM minutes".
    """

    # Create duration string with number of days.
    duration_str = f"{minutes // (24 * 60)} day{'s' if minutes >= 24 * 60 * 2 else ''} " if minutes >= 24 * 60 else ""

    # Get remainder minutes that do not make a full day.
    minutes %= (24 * 60)

    # Create duration string with number of hours.
    duration_str += f"{minutes // 60} hour{'s' if minutes >= 60 * 2 else ''} " if minutes >= 60 else ""

    # Get remainder minutes that do not make a full hour.
    minutes %= 60

    # Add number of minutes to duration string.
    duration_str += f"{minutes} minute{'s' if minutes % 60 >= 2 else ''}" if minutes >= 1 else ""

    return duration_str


def generate_timeframe_table(timeframes: dict) -> str:
    """ Generate a table containing the timeframe IDs, UTC offsets, start/end times and normalized start/end times
    of the timeframes.

    Used in the 'list' action in TimeSync.

    Args:
        timeframes (dict): timeframes to include in the table.

    Returns:
        a table containing details about each timeframe as a multiline string.
    """

    # Column headers for the table. Added 2 extra spaces at the end of "Normalized End Time" for symmetry in the table.
    column_headers = [
        "Timeframe ID", "UTC Offset", "Start Time", "End Time", "Normalized Start Time", "Normalized End Time  "
    ]

    # Create a new Table object.
    table = Table(column_headers)

    # Adding the rows.
    for timeframe_id, timeframe in timeframes.items():
        # Getting the attributes of the timeframe as a tuple.
        attributes = timeframe.get_attributes()

        # Adding the timeframe row to the table.
        table.add_row([timeframe_id, *attributes])

    return str(table)


def generate_localized_times_table(timeframes: dict, common_timeframe: Tuple[datetime, datetime] = None) -> str:
    """ Generate a table containing the localized times of the common timeframe for each timeframe.

    Args:
        timeframes (dict): timeframes to include in the table.
        common_timeframe (tuple): the common timeframe of the timeframes.

    Returns:
        a table of the localized times as a multiline string
    """

    # Column headers for the table.
    column_headers = ["Timeframe ID", "UTC Offset", "Start Time", "End Time"]

    # Create a new Table object.
    table = Table(column_headers)

    # Adding the rows.
    for timeframe_id, timeframe in timeframes.items():
        # Getting the UTC offset of the timeframe.
        utc_offset = timeframe.get_utc_offset()

        # Getting the localized start and end times.
        localized_times = timeframe.to_local_time(common_timeframe)

        # Adding the timeframe row to the table.
        table.add_row([timeframe_id, utc_offset, *localized_times])

    return str(table)


def generate_visualization_table(timeframes: dict, weight: int, earliest_start_time: datetime) -> str:
    # Column headers for the table.
    column_headers = ["Timeframe ID", "Representation"]

    # Create a new Table object.
    table = Table(column_headers)

    # Create timedelta object.
    delta = timedelta(minutes=weight)

    # Adding the rows.
    for timeframe_id, timeframe in timeframes.items():
        # Reference datetime is used to keep track of the
        reference_datetime = earliest_start_time

        # Get the normalized start/end times for the timeframe.
        start_time, end_time = timeframe.get_norm_times()

        # Visualization string.
        vis_string = ""

        while reference_datetime < end_time:
            # Add a "|" if the reference_datetime is within the timeframe. Else, print a whitespace.
            vis_string += "|" if start_time <= reference_datetime else " "

            # Update the reference_datetime.
            reference_datetime += delta

        # Adding the timeframe id and vis string to the table.
        table.add_row([timeframe_id, vis_string])

    return str(table)


class Table:
    """
    Class to create tables as multiline strings.
    """

    def __init__(self, column_headers: list | tuple) -> None:
        """
        Args:
            column_headers: column headers of the table.
        """

        # The table column headers.
        self.column_headers = column_headers

        # 2D list used to store values of the table. First row contains column headers.
        self.table = [column_headers]

        self.num_cols = len(column_headers)

    def add_row(self, row_values: list | tuple) -> None:
        """ Add a new row to the table.

        Args:
            row_values: list containing the values for each column of the row.
        """

        # Number of values in the row_values list must match the number of columns.
        if len(row_values) != self.num_cols:
            raise ValueError(f"Incorrect number of row values. Expected {self.num_cols} but got {len(row_values)}")

        # Append the new row to the table.
        self.table.append(row_values)

    def __str__(self):
        # List to store the widths of the longest value in each column.
        column_widths = []

        # Finding the length of the longest value for each column.
        for col in range(self.num_cols):
            # Finding the length of the longest value in current column.
            longest_width = len(max([row[col] for row in self.table], key=len))

            # Add the current column width to the list.
            column_widths.append(longest_width)

        # Horizontal length of the output string.
        # horizontal length = sum column widths  +
        #                     1 leading and 1 trailing spaces in each column (= number_of_columns x 2) +
        #                     number of column dividers "|" (= number_of_columns + 1)
        horizontal_len = sum(column_widths) + len(column_widths) * 2 + (len(column_widths) + 1)

        # Adding the starting horizontal line.
        output_string = ("-" * horizontal_len) + "\n"

        # Adding the column headers' row.
        for index, header in enumerate(self.column_headers):
            output_string += f"| {header:{column_widths[index]}} "
        output_string += "|\n"

        # Adding divider after column headers.
        for width in column_widths:
            # Add 2 to the width to account for 1 leading whitespace and 1 trailing whitespace.
            output_string += f"|{('-' * (width + 2))}"
        output_string += "|\n"

        # Traversing rows, excluding the headers row.
        for row in self.table[1:]:
            # Adding the values from each column of a row.
            for index, element in enumerate(row):
                output_string += f"| {element:{column_widths[index]}} "

            # Add row-end vertical divider and new line character.
            output_string += "|\n"

        # Add the ending line.
        output_string += ("-" * horizontal_len) + "\n"

        # Return the constructed string.
        return output_string

    def __repr__(self):
        self.__str__()
