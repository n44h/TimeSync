'''
Wrote this to find a common free time for people living in different time zones.
This script is used to find a common time frame from several time frame inputs.

The period of time each person is free is called a "time frame".
Time frames are in 24hr format and have a "starting" and "ending" time.

For example: 13:00 to 18:00. 13:00 is the starting time and 18:00 is 
the ending time for this time frame.

Each time frame is accompanied by a timezone.
Timezones are communicated with reference to GMT/UTC.

Each timezone and time frame pair is called a "limit".


--------------------------------------------------------------------------

-> Adding a Limit:
The command to add a new limit is: 

>> add {city},{country} {startTime} {endTime} <<

{city} and {country} are used to find the UTC offset, taking into account Daylight Saving Time as well.
e.g.:
- Vancouver,Canada
- London,UK
- Seattle,USA

{startTime} and {endTime} are in 24 hr format without the colon.
e.g.:
- 9am     = 0900
- 6:30pm  = 1830
- 12am    = 0000  

Here is an example command to add a limit:

>> add +4 1430 1700 <<

--------------------------------------------------------------------------

-> Clearing all the Limits:
The command to clear all the limits that have been entered:

>> clear limits <<

--------------------------------------------------------------------------

-> Print all the Limits:
Command to list all the limits that have been entered:

>> print limits <<

--------------------------------------------------------------------------

-> Removing a specific Limit:
To remove a specific limit, you need to know the index of the limit.
The index can be found by just printing the limits. INDICES START FROM 0.

Command to remove a limit:

>> remove {index} <<

e.g.: 
- To remove the 3rd limit: >> remove 2 <<

--------------------------------------------------------------------------

-> Finding the common time frame:
Command to find a common time frame:

>> run << 

--------------------------------------------------------------------------

-> Visualize the time frames:
Command to visualize the time frames accurate to 30 mins.

>> vis <<

--------------------------------------------------------------------------

-> Terminate the script:
Command:

>> quit <<

--------------------------------------------------------------------------
'''

import re
import sys
from datetime import datetime, timedelta
import time
import requests
import json

# Datetime format.
dt_format = '%d/%m/%y %H:%M:%S'
date_today = datetime.now().strftime('%d/%m/%y')

# Stores the startTimes of each limit in GMT/UTC time.
startTimes = []

# Stores the endTimes of each limit in GMt/UTC time.
endTimes = []

# Variable to keep count of the number of limits.
limit_count = 0

def convertToUTC(BASE_LOCATION, BASE_DATETIME): 
    API_KEY = "GIEB53MNXY0K" # API key for timezoneDB.
    TARGET_TIMEZONE = "UTC"
    BASE_UNIX_TIMESTAMP = str(datetime.timestamp(BASE_DATETIME)*1000)

    # Sending API request
    try:
        response = requests.get(f"https://api.timezonedb.com/v2.1/convert-time-zone?key={API_KEY}&format=json&from={BASE_LOCATION}&to={TARGET_TIMEZONE}&time={BASE_UNIX_TIMESTAMP}")
    except Exception as e:
        print(e)

    # Checking status code.
    if response.status_code <= 299:
        print(f"API Time Request completed with status code: {response.status_code}.\n")
    else:
        print(f"API Time Request failed with status code: {response.status_code}.\n")
        
    # converting the json to readable dictionary and then getting the value of 'toTimestamp'
    UTC_timestamp = int(response.json()['toTimestamp'])
    print(UTC_timestamp)
    # converting unix timestamp to date object and returning
    return datetime.fromtimestamp(UTC_timestamp)


def add(input):
    global limit_count,startTimes,endTimes

    # Extracting the timezone from the string.
    location = (re.findall('\w+,\w+', input))[0].upper()

    # Extracting the StartTime and endTime into a list.
    time_stamps = re.findall('\d\d\d\d', input)

    # Adding the colon in the time strings. 0900 -> 09:00
    start_datetime_object = datetime.strptime(f'{date_today} {time_stamps[0][:2]}:{time_stamps[0][2:]}:00', dt_format)
    end_datetime_object = datetime.strptime(f'{date_today} {time_stamps[1][:2]}:{time_stamps[1][2:]}:00', dt_format)

    print(start_datetime_object.strftime('%d/%m/%y %H:%M:%S'))
    print(end_datetime_object.strftime('%d/%m/%y %H:%M:%S'))

    # Adding the startTime as a datetime object.
    startTimes.append(convertToUTC(location, start_datetime_object))

    # Wait for a little over 1 second because the API has a restriction of 1 API call per second.
    time.sleep(1.2)

    # Checking if endTime is less than startTime (this means that the endTime is in the next day).
    if start_datetime_object < end_datetime_object :
        endTimes.append(convertToUTC(location, end_datetime_object))
    else:
        endTimes.append(convertToUTC(location, end_datetime_object + timedelta(days=1)))
   
    # Incrementing limit_count.
    limit_count += 1

def clear():
    global limit_count,startTimes,endTimes

    startTimes.clear()
    endTimes.clear()
    limit_count = 0

def run():
    global startTimes,endTimes

    print(startTimes[0].strftime(dt_format))
    print(endTimes[0].strftime(dt_format))

    op_startTime = startTimes[0]
    op_endTime = endTimes[0]

    # Finding the latest start time.
    for item in startTimes:
        if op_startTime > item:
            op_startTime = item

    # Finding the earliest end time.
    for item in endTimes:
        if op_endTime < item:
            op_endTime = item    

    # Printing the result
    if op_startTime < op_endTime:
        common_time_frame = f'from {op_startTime.strftime("%H:%M")} to {op_endTime.strftime("%H:%M")}'
        delta = op_endTime - op_startTime
        duration = f'{delta.hours}:{delta.minutes}'
        print(f'\nCommon time frame {common_time_frame} ({duration})\n')
    else:
        print("\nNo common time frame for the set limits.\n")

def vis():
    # Keeps count of how many times the reference datetime object is incremented.
    increment_counter = 0

    for n in range(len(startTimes)):
        # Creating a reference datetime which the other datetime objects will be measured against.
        reference_datetime = startTimes[0]
        reference_datetime  
        output = ''
        while reference_datetime < startTimes[n]:
            output += '|'
            # Incrementing by 30 mins.
            reference_datetime += timedelta(minutes = 30)
            increment_counter+=1
        while reference_datetime < endTimes[n]:
            output += ' '
            # Incrementing by 30 mins.
            reference_datetime += timedelta(minutes = 30)
            increment_counter+=1
        while increment_counter < 49:
            output += '|'
            # Incrementing by 30 mins.
            reference_datetime += timedelta(minutes = 30)
            increment_counter+=1
        
        print(f'{output}\n')



while True:
    user_command = input("command: ")

    if "add" in user_command:
        if re.search('add\s\w+,\w+\s([0,1]\d[0-5]\d|[2][0-3][0-5]\d)\s([0,1]\d[0-5]\d|[2][0-3][0-5]\d)', user_command) != None:
            add(user_command)
        else:
            print('\nInvalid command.\n')

    elif user_command == 'clear limits':
        clear()

    elif user_command == 'vis':
        vis()
    
    elif user_command == 'run':
        run()
    
    elif user_command == 'quit':
        sys.exit()

    else:
        print('\nInvalid command.\n')
