# Cross Timezone Coordinator
Python script to find a common time frame within several time frame constraints with different timezones.

A period of time is called a "time frame".
Time frames have a "starting" and "ending" time which are in 24hr format.
Each time frame is accompanied by a location.
Locations must include the city's name. Country's name is optional.

A (location,time frame) pair is called a "constraint".

## Commands

### Add Constraint:
Add a new constraint.

`>> add`

#### Parameters

`{city, country}` the local time will be found using Abstract's timezone API and it will account for Daylight Saving Time.
`{startTime}` in 24hr format without the colon (HHMM).
`{endTime}` in 24hr format without the colon (HHMM).

- 9am     \-\> 0900
- 6:30pm  \-\> 1830
- 12am    \-\> 0000  

### Clear Constraints:
Clear all the constraints that have been set.

`clear`

### Find Common Time Frame:
Find a common time frame within the constraints, if one exists.

`run` 

### Visualize Constraints:
Visualize all the constraints in UTC time accurate to 30 mins.

`vis`

### Terminate the Script:

`quit`
