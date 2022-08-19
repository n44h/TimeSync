# TimeSync

Tool to find a common timeframe within several timeframes across different timezones.  

### How TimeSync works:

The start and end points of each timeframe are normalized to UTC +00:00 time.

Then, the latest normalized start point is taken as the start point of the shared timeframe.
Similarly, the earliest normalized end point is taken as the end point of the shared timeframe.

A timeframe is one continuous period of time and cannot include breaks or intervals.



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
>> add foo +0600 12-08-22 1025 1530
```

#### Start point and end point are on different days.  

Adding a timeframe from 10:25 UTC +06:00 on 12-08-22 to 15:30 UTC +06:00 on 13-08-22.  
Let's call this one _bar_.

```shell
>> add bar +0600 12-08-22 1025 13-08-22 1530
```

___

### Find a shared Timeframe

Find the longest shared timeframe among the stored timeframes.  
Ensure at least 2 timeframes have been added before performing this action.

```shell
>> run
```

___

### List all Timeframes

To list all the stored Timeframes.

```shell
>> ls
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