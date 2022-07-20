import sys
from datetime import datetime
from typing import Tuple
from utils import clear_screen, validate_datetime, validate_offset
from utils import TimeFrame


# Datetime format.
DATETIME_FORMAT = "%d-%m-%y %H:%M"

# Dict to store the timeframes.
TIMEFRAMES = {}


def add_timeframe(timeframe_id: str, utc_offset: str, start_time: str, end_time: str) -> None:
    """ Add a new timeframe to Meridian.

    Args:
        timeframe_id (str): Unique ID to reference the timeframe.
        utc_offset (str): UTC offset of the timeframe.
        start_time (str): start time of the timeframe.
        end_time (str): end time of the timeframe.
    """

    # If timeframe_id is None, provide default id (i.e. the timeframe's index).
    if timeframe_id is None:
        timeframe_id = f"Timeframe {len(TIMEFRAMES) - 1}"

    # Ensure that the same timeframe_id does not already exist in TIMEFRAMES.
    if timeframe_id in TIMEFRAMES.keys:
        print(f"\nA timeframe with ID \"{timeframe_id}\" already exists.")

        # Prompt the user whether they wish to overwrite the existing timeframe entry.
        response = input(f"\nDo you wish to overwrite the existing timeframe \"{timeframe_id}\"? [N/y]: ")
        if response.lower() not in ["y", "yes"]:
            print("\nAction aborted. Timeframe entry was not overwritten.")
            # End function execution.
            return

    # Create a new TimeFrame object.
    new_timeframe = TimeFrame(utc_offset, start_time, end_time)

    # Add the new timeframe to the "timeframes" dictionary.
    TIMEFRAMES[timeframe_id] = new_timeframe


def find_shared_timeframe() -> Tuple[datetime, datetime] | None:
    """ Finds the longest shared timeframe within the provided timeframes.

    Returns:
        The shared timeframe among the provided timeframes. Returns None if a shared timeframe does not exist.
    """

    # Create a list containing the values of the TIMEFRAMES dictionary.
    timeframes = list(TIMEFRAMES.values())

    # Initialize (latest_start_time, earliest_end_time) to the normalized (start, end) times of the 0th timeframe.
    latest_start_time, earliest_end_time = timeframes[0].get_norm_times()

    # Looping through every timeframe to find the latest normalized start time and earliest normalized end time.
    for timeframe in timeframes[1:]:
        # Get the normalized start and end times for the TimeFrame object.
        norm_start, norm_end = timeframe.get_norm_times()

        # Assign the current timeframe's normalized start time to latest_start_time if it is later.
        if norm_start > latest_start_time:
            latest_start_time = norm_start

        # Assign the current timeframe's normalized end time to earliest_end_time if it is earlier.
        if norm_end < earliest_end_time:
            earliest_end_time = norm_end

    # If the latest start time is greater than the earliest end time, a shared timeframe does not exist.
    if latest_start_time > earliest_end_time:
        return None

    # Else, return the start and end times as a tuple.
    else:
        return latest_start_time, earliest_end_time


def print_help() -> None:
    """ Prints the help description. """

    # Print help string.
    print(
        """
        Core Commands:
            [1] add <timeframe-id> <utc-offset> <start-time> <end-time>
            [2] find
            [3] remove <timeframe-id>
            [4] reset
            [5] ls
            [6] vis
        
        Helper Commands:
            [7] clear
            [8] help
            [9] exit
        """)


def main():
    # Clear the terminal.
    clear_screen()

    # Print the title.
    print("\nMeridian - Find a shared timeframe among several timeframes across different timezones")

    # Print help.
    print_help()

    while True:
        # Prompt the user for command.
        command = input(">> ")

        # If command is empty, continue.
        if command == "":
            continue

        # Split the command string into a list. Whitespace is the delimiter character.
        command = command.split()
        # The first string is the action to perform.
        action = command[0]

        """ Analyzing Command """

        # ADD
        if action == "add":
            # Number of arguments.
            if len(command) < 5:
                print(f"\nadd: Expected 4 arguments but found {len(command) - 1}."
                      f"\n     Required arguments: timeframe-id, utc-offset, start-time, end-time")
                continue

            # Validate utc-offset format.
            flag, error_message = validate_offset(command[2])
            if flag is False:
                print(f"\n{error_message}\n")
                continue

            # Validate start-time format.
            if not validate_datetime(command[3]):
                print("\nadd: Incorrect format of start-time argument. Expected format: DD-MM-YY HHMM.\n")
                continue

            # Validate end-time format.
            if not validate_datetime(command[4]):
                print("\nadd: Incorrect format of end-time argument. Expected format: DD-MM-YY HHMM.\n")
                continue

            # Add the timeframe if it passes all the validation checks.
            add_timeframe(timeframe_id=command[1],
                          utc_offset=command[2],
                          start_time=command[3],
                          end_time=command[4])
        # ---------- #

        # FIND
        elif action == "find":
            # Ensure there are more than 1 timeframes provided.
            if len(TIMEFRAMES) <= 1:
                print(f"\nfind:{len(TIMEFRAMES)} timeframe(s) provided."
                      "\n      Provide at least 2 timeframes to find a shared timeframe.")
                continue

            # Find the shared timeframe.
            shared_timeframe = find_shared_timeframe()

            # If None, shared time frame does not exist.
            if shared_timeframe is not None:
                # Convert the datetime objects to Strings.
                start_datetime, end_datetime = shared_timeframe
                start_datetime = datetime.strftime(start_datetime, DATETIME_FORMAT)
                end_datetime = datetime.strftime(end_datetime, DATETIME_FORMAT)

                # Print output.
                print(f"\nShared timeframe from {start_datetime} UTC+00 to {end_datetime} UTC+00.")

            else:
                print("\nThere is no shared timeframe within the provided timeframes.")
        # ---------- #

        # REMOVE
        elif action == "remove":
            # Number of arguments.
            if len(command) < 2:
                print(f"\nremove: Expected 1 argument \"timeframe-id\" but found 0 arguments.")
                continue

            # Check if timeframe-id exists.
            if command[1] not in TIMEFRAMES.keys:
                print(f"\nremove: Timeframe with the ID \"{command[1]}\" does not exist.")
                continue

            # Remove the timeframe if all validation checks are passed.
            TIMEFRAMES.pop(command[1])
        # ---------- #

        # RESET
        elif action == "reset":
            # Prompt the user for confirmation.
            print("\nAre you sure you want to reset this session? This will clear all stored timeframes. [N/y]")
            response = input(">> ")

            if response.lower() in ["y", "yes"]:
                # Clearing all values in TIMEFRAMES.
                TIMEFRAMES.clear()
        # ---------- #

        # LIST
        elif action == "ls":
            pass
        # ---------- #

        # VISUALIZE
        elif action == "vis":
            pass
        # ---------- #

        # CLEAR
        elif action == "clear":
            clear_screen()
        # ---------- #

        # HELP
        elif action == "help":
            # Print help.
            print_help()
        # ---------- #

        # EXIT
        elif action == "exit":
            # Prompt the user for confirmation.
            print("\nAre you sure you want to exit Meridian? [N/y]")
            response = input(">> ")

            if response.lower() in ["y", "yes"]:
                break
        # ---------- #

        # INVALID COMMAND
        else:
            print("Invalid command.")

    # Exit the program.
    sys.exit(0)


if __name__ == "__main__":
    # Invoke main().
    main()
