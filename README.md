# Cross Timezone Coordinator
Python script to find a common time frame within several time frame constraints with different timezones.

A period of time is called a "time frame".
Time frames have a "starting" and "ending" time which are in 24hr format.
Each time frame is accompanied by a timezone.
Timezones are communicated with reference to its offset from GMT/UTC time.

A timezone, time frame pair is called a "constraint".

## Commands

### Add Constraint:
Add a new constraint.

`add {utc_offset} {startTime} {endTime}`

`{utc_offset}` is the timezone offset from UTC time.

`{startTime}` and `{endTime}` are in 24hr format without the colon.

- 9am     \-\> 0900
- 6:30pm  \-\> 1830
- 12am    \-\> 0000  

Here is an example command to add a constraint: `add +4 1430 1700`

### Clear Constraints:
Clear all the constraints that have been set.

`clear con`

### Find Common Time Frame:
Find a common time frame within the constraints if one exists.

`run` 

### Visualize Constraints:
Visualize all the constraints in UTC time accurate to 30 mins.

`vis`

### Terminate the Script:

`quit`
