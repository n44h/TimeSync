import os
import re
from typing import Tuple


VALID_UTC_OFFSETS = ["-1200", "-1100", "-1000", "-0930", "-0900", "-0800", "-0700", "-0600", "-0500", "-0400",
                     "-0330", "-0300", "-0200", "-0100", "-0000", "+0000", "+0100", "+0200", "+0300", "+0330",
                     "+0400", "+0430", "+0500", "+0530", "+0545", "+0600", "+0630", "+0700", "+0800", "+0845",
                     "+0900", "+0930", "+1000", "+1030", "+1100", "+1200", "+1245", "+1300", "+1400"]


def clear_screen() -> None:
    """ Utility function to clear the Terminal. """
    os.system('cls' if os.name == 'nt' else 'clear')


def is_valid_datetime(in_datetime: str) -> bool:
    """ Checks if a datetime string has the format DD-MM-YYYY HHMM.

    Args:
        in_datetime (str): the datetime string input.

    Returns:
        True if the input matches the DD-MM-YY HHMM format.
    """

    # Regex for datetime format.
    datetime_re = re.compile(r"^[0-3]\d-[0-1]\d-\d{2} [0-2]\d[0-5]\d$")

    # Match in_datetime argument with datetime regex.
    return bool(datetime_re.match(in_datetime))


def is_valid_offset(input_offset: str) -> Tuple[bool, str]:
    """ Validate a UTC offset string.

    Args:
        input_offset (str): the UTC offset string input.

    Returns:
        a tuple (flag, error_message). flag is True if the input matches the ±HHMM format.
    """

    # Flag is True if the input_offset is valid.
    flag = True
    # Error message to print to the terminal.
    error_message = ""

    # Regex expression for UTC offset.
    offset_re = re.compile(r"^[+,-]\d{4}$")

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
