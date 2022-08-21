import os
import re
from typing import Tuple


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

    # Basic validations.
    # time_str should not contain more than 1 colon character.
    if time_str.count(":") > 1:
        raise ValueError("time string cannot contain more than one \":\" character.")

    # Besides one colon ":" character, time_str should only contain digits.
    elif time_str.replace(":", "").isdigit() is False:
        raise ValueError("time strings can only contain digits and \":\" characters.")

    # Get the time string length.
    length = len(time_str)

    # Check 1
    #
    # Time string is empty or only contains a colon.
    #
    if time_str in ["", ":"]:
        return "00:00"

    # Check 2
    #
    # String contains only a single digit.
    #
    # Possible inputs:  4 -> 04:00
    #
    elif length == 1:
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
        error_message = "Incorrect format of UTC offset. Expected format: ±HHMM."

    elif input_offset not in VALID_UTC_OFFSETS:
        flag = False
        error_message = "Invalid UTC offset. Provide a valid UTC offset."

    # Return the flag and message.
    return flag, error_message


def construct_timeframe_table(timeframes: dict) -> str:
    """ Constructs a table containing the timeframe IDs, UTC offsets, start/end times and normalized start/end times
    of the timeframes.

    Used in the 'list' action in TimeSync.

    Args:
        timeframes (dict): timeframes to include in the table.

    Returns:
        a table containing details about each timeframe as a multiline string.

    """
    # Headers strings for each column.
    column_headers = ["Timeframe ID", "UTC Offset", "Start Time", "End time",
                      "Normalized Start Time", "Normalized End Time"]

    # Determining the width of the Timeframe ID column.
    # The width is the length of the longest timeframe_id or the length of the column header, whichever is longer.
    timeframe_id_col_width = max(len(max(timeframes.keys(), key=len)), len(column_headers[0]))

    column_widths = [timeframe_id_col_width, 10, 14, 14, 21, 19]

    # delete timeframe_id_col_width.
    del timeframe_id_col_width

    # # Appending the column widths for the remaining columns 1 to (N-1), where N is the number of columns.
    # # Add 2 to the column width to account for 1 leading and 1 trailing space.
    # column_widths = column_widths + [len(header) for header in column_headers[1:]]

    # Horizontal length of the output string.
    # horizontal length = sum column widths  +
    #                     1 leading and 1 trailing spaces in each column (= number_of_columns x 2) +
    #                     number of column dividers "|" (= number_of_columns + 1)
    horizontal_len = sum(column_widths) + len(column_widths)*2 + (len(column_widths) + 1)

    # Adding the starting horizontal line.
    output_string = ("-" * horizontal_len) + "\n"

    # Adding the column headers' row.
    for index, header in enumerate(column_headers):
        output_string += f"| {header:{column_widths[index]}} "
    output_string += "|\n"

    # Adding the horizontal divider after the column headers.
    # output_string += f"|{('-' * (horizontal_len - 2))}|\n"

    for width in column_widths:
        output_string += f"|{('-' * (width+2))}"
    output_string += "|\n"

    # Adding the timeframe ids and the respective timeframe information.
    for timeframe_id, timeframe in timeframes.items():
        # Getting the initial and normalized start and end times.
        utc_offset = timeframe.get_utc_offset()
        times = timeframe.get_times_str()
        norm_times = timeframe.get_norm_times_str()

        # Appending the timeframe_id.
        output_string += f"| {timeframe_id:{column_widths[0]}} "

        # Appending the UTC offset.
        output_string += f"| {utc_offset:{column_widths[1]}} "

        # Appending the start and end times.
        output_string += f"| {times[0]:{column_widths[2]}} | {times[1]:{column_widths[3]}} "

        # Appending the normalized start and end times. Adding the newline character at the end.
        output_string += f"| {norm_times[0]:{column_widths[4]}} | {norm_times[1]:{column_widths[5]}} |\n"

    # Add the ending line.
    output_string += ("-" * horizontal_len) + "\n"

    # Return the constructed string.
    return output_string
