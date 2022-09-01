# TimeSync

TimeSync is a tool to find the longest common timeframe out of the inputted timeframes in different timezones. Refer to the [Commands section](#commands) to see how to use TimeSync.

### How TimeSync works:

The start and end times of each timeframe are normalized to UTC +00:00 time.

The latest normalized start time is taken as the start time of the common timeframe.  
Similarly, the earliest normalized end time is taken as the end time of the common timeframe.

A timeframe is one continuous period of time and cannot include breaks or intervals.


## Formats
The formatting rules are very relaxed for time and UTC offset inputs.
If there is an intuitive way
to represent the input, TimeSync will internally format it to the proper format.  

#### Time Inputs

| Time Input | How it will be formatted |
|------------|--------------------------|
| :          | 00:00                    |
| 0          | 00:00                    |
| 4          | 04:00                    |
| 04         | 04:00                    |
| 15         | 15:00                    |
| 425        | 04:25                    |
| 4:5        | 04:05                    |
| :35        | 00:35                    |
| 15:        | 15:00                    |
| 6:45       | 06:45                    |
| 13:5       | 13:05                    |
| 0420       | 04:20                    |

#### UTC Offset Inputs
The above-mentioned formats are accepted for UTC offset inputs as well.  
Additionally, inputs without a sign will be assumed to be a positive UTC offset.

## Commands

### Add a Timeframe

Command skeleton to add a timeframe:

```shell
>> add <timeframe-id> <utc-offset> <start-point> <end-point>
```

#### Start point and end point are on the same day.  

Adding a timeframe from 10:25 to 15:30 UTC +06:00 on 12-08-22.  
Let's call the timeframe _foo_.

```shell
>> add foo +06 12-08-22 1025 1530
```

#### Start point and end point are on different days.  

Adding a timeframe from 10:25 UTC +06:00 on 12-08-22 to 15:30 UTC +06:00 on 13-08-22.  
Let's call this one _bar_.

```shell
>> add bar +06 12-08-22 1025 13-08-22 1530
```

___

### List Timeframes

Command to list the stored timeframes: `ls`, `list`

```shell
>> ls
```

Will print a table as shown below:

```shell
-------------------------------------------------------------------------------------------------------------
| Timeframe ID | UTC Offset | Start Time     | End Time       | Normalized Start Time | Normalized End Time |
|--------------|------------|----------------|----------------|-----------------------|---------------------|
| foo          | +04:00     | 12-08-22 09:00 | 12-08-22 20:00 | 12-08-22 05:00        | 12-08-22 16:00      |
| bar          | -01:00     | 12-08-22 12:00 | 12-08-22 18:30 | 12-08-22 13:00        | 12-08-22 19:30      |
| bang         | -05:00     | 12-08-22 08:20 | 12-08-22 17:45 | 12-08-22 13:20        | 12-08-22 22:45      |
-------------------------------------------------------------------------------------------------------------
```

___

### Find a common Timeframe

Find the longest common timeframe among the stored timeframes.  
Ensure at least 2 timeframes have been added before performing this action.

Command to find common timeframe: `run`, `find`, `sync`

```shell
>> run
```

If a common timeframe exists, its start/end times and duration are printed.  
Additionally, a table of localized times for each timeframe is displayed as shown below.  

```shell
Common timeframe found.

Start Time : 12-08-22 13:20 UTC
End Time   : 12-08-22 16:00 UTC
Duration   : 2 hours 40 minutes

---------------------------------------------------------------
| Timeframe ID | UTC Offset | Start Time     | End Time       |
|--------------|------------|----------------|----------------|
| foo          | +04:00     | 12-08-22 17:20 | 12-08-22 20:00 |
| bar          | -01:00     | 12-08-22 12:20 | 12-08-22 15:00 |
| bang         | -05:00     | 12-08-22 08:20 | 12-08-22 11:00 |
---------------------------------------------------------------
```

___

### Remove a Timeframe

Command skeleton to remove a timeframe:

```shell
>> remove <timeframe-id>
```

Removing the timeframe _foo_.

```shell
>> remove foo
```

___

### Remove all Timeframes

To remove all the stored timeframes.

```shell
>> reset
```

___
