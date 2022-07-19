import sys
import argparse
from datetime import datetime, timedelta
from timeframe import TimeFrame


"""
NOTE: We need to assign the datetime objects a date as we are create 'aware' datetime objects.
      Hence, regardless of the actual dates of the constraints, we use the current date in the system.
"""

# Datetime formats.
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M'
DATETIME_FORMAT = f'{DATE_FORMAT} {TIME_FORMAT}'

VALID_COMMANDS = ["add", "ls", "remove", "visualize", "find"]

VALID_UTC_OFFSETS = ["-1200", "-1100", "-1000", "-0930", "-0900", "-0800", "-0700", "-0600", "-0500", "-0400",
                     "-0330", "-0300", "-0200", "-0100", "+0000", "-0000", "+0100", "+0200", "+0300", "+0330",
                     "+0400", "+0430", "+0500", "+0530", "+0545", "+0600", "+0630", "+0700", "+0800", "+0845",
                     "+0900", "+0930", "+1000", "+1030", "+1100", "+1200", "+1245", "+1300", "+1400"
                     ]

timeframes = {}


def add_timeframe(timeframe_id: str, utc_offset: str, start_time: str, end_time: str) -> None:
    """ Add a new timeframe to Cordi

    Args:
        timeframe_id (str): Unique ID to reference the timeframe
        utc_offset (str): UTC offset of the timeframe
        start_time (str): start time of the timeframe
        end_time (str): end time of the timeframe
    """

    # If timeframe_id is None, provide default id (i.e. the timeframe's index).
    if timeframe_id is None:
        timeframe_id = f"Timeframe {len(timeframes)-1}"

    # Ensure that the same timeframe_id does not exist.
    if timeframe_id in timeframes.keys:
        print(f"\nA timeframe with ID \"{timeframe_id}\" already exists."
              f"\nDo you wish to overwrite the existing timeframe \"{timeframe_id}\"?")

    # Create a new TimeFrame object.
    new_timeframe = TimeFrame(timeframe_id, utc_offset, start_time, end_time)

    # Add the new timeframe to the "timeframes" dictionary.
    timeframes[timeframe_id] = new_timeframe



def clear_timeframes() -> None:
    global constraint_count,start_times,end_times
    start_times.clear()
    end_times.clear()
    constraint_count = 0

def run():
    global start_times,end_times

    op_start_time = start_times[0]
    op_end_time = end_times[0]

    # Finding the latest start time.
    for this_start_time in start_times:
        if this_start_time > op_start_time:
            op_start_time = this_start_time
    
    # Finding the earliest end time.
    for this_end_time in end_times:
        if this_end_time < op_end_time:
            op_end_time = this_end_time    
    
    # Printing the result
    if op_start_time < op_end_time:
        common_time_frame = f'from {op_start_time.strftime("%H:%M")} to {op_end_time.strftime("%H:%M")}'
        delta = op_end_time - op_start_time
        difference = divmod(delta.days*1440 + (delta.seconds)/60, 60)
        duration = f'{int(difference[0])} hours and {int(difference[1])} minutes'
        print(f'\nThere is a common time frame {common_time_frame} ({duration})\n')
    else:
        print("\nNo common time frame for the set constraints.\n")

def vis():
    """
    NOTE: The reference datetime object must start 12 hours previous to GMT+0 to account for countries uptil GMT-12.
          The reference datetime must also increment until 12 hours after GMT+0 to account for countries uptil GMT+12.
    """
    # Getting the starting date.
    reference_datetime_start_date = (datetime.now() - timedelta(hours = 24)).strftime(DATE_FORMAT)
    # Keeps count of how many times the reference datetime object is incremented.
    increment_counter = 0

    # Printing reference hours.
    print('12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 00 01 02 03 04 05 06 07 08 09 10 11')
    
    for n in range(len(start_times)):
        
        # Creating a reference datetime which the other datetime objects will be measured against.
        reference_datetime = datetime.strptime(f'{reference_datetime_start_date} 12:00:00', DATETIME_FORMAT)
        increment_counter = 0
        output = ''
        while reference_datetime < start_times[n]:
            output += '|' + (' ' if increment_counter%2==1 else '')
            # Incrementing by 30 mins.
            reference_datetime += timedelta(minutes = 30)
            increment_counter+=1
        while reference_datetime < end_times[n]:
            output += '#' + (' ' if increment_counter%2==1 else '')
            # Incrementing by 30 mins.
            reference_datetime += timedelta(minutes = 30)
            increment_counter+=1
        while increment_counter < 96:
            output += '|' + (' ' if increment_counter%2==1 else '')
            # Incrementing by 30 mins.
            reference_datetime += timedelta(minutes = 30)
            increment_counter+=1
        
        print(f'{output}\n')




if __name__ == "__main__":
    # Create argparse instance.
    parser = argparse.ArgumentParser(prog="Meridian",
                                     description="Find a common timeframe within different timeframes across timezones"
                                     )

    # Add arguments.
    parser.add_argument("command",
                        help="The action to perform",
                        type=str,
                        choices=VALID_COMMANDS)

    parser.add_argument("-o", "--utc-offset",
                        help="UTC offset of the timeframe",
                        type=str,
                        choices=VALID_UTC_OFFSETS)

    parser.add_argument("-s", "--start-time",
                        help="Start time of the timeframe; Format: DD-MM-YY HHMM",
                        nargs=2,
                        type=str)

    parser.add_argument("-e", "--end-time",
                        help="End time of the timeframe; Format: DD-MM-YY HHMM",
                        nargs=2,
                        type=str)

    parser.add_argument("-n", "--timeframe-id",
                        help="Optionally assign an id to the timeframe",
                        type=str)

    # Parse the arguments
    args = parser.parse_args()

    if args.command == "add":
        add_timeframe(utc_offset=args.utc_offset,
                      start_time_str=)
