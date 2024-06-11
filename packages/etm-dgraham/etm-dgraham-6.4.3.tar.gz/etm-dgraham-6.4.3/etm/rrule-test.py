#! /usr/bin/env python3
from datetime import datetime
from dateutil.rrule import rrule, DAILY
from dateutil.tz import gettz

def is_naive(dt):
    return(dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None
           )

# Define the timezone (replace 'America/New_York' with your specific timezone)
pacific = gettz('US/Pacific')
mountain = gettz('America/Denver')
central = gettz('US/Central')
eastern = gettz('America/New_York')
local = gettz()
utc = gettz('UTC')
naive = None

dt_format = "%a %Y-%m-%d %H:%M %Z %z" 

tzinfo = eastern
# Define the starting date and time for the event
start_date = datetime(2024, 3, 8, 2, 30, tzinfo=tzinfo)  # 2:30 on Mon Oct 28, 2024

float = is_naive(start_date)

print(f"{start_date = }; {float = }")

# Create a recurrence rule for daily events
rule = rrule(freq=DAILY, dtstart=start_date)

# Generate the next 14 occurrences of the event
occurrences = [dt for dt in rule[:14]]

# # Print the occurrences
for tz in [pacific, mountain, central, eastern, local, utc, naive]:
    print(f"\nastimezone {tz} occurences for {tzinfo = }")
    for occurrence in occurrences:
        if float:
            occurrence = occurrence.replace(tzinfo=tz)
        if tz == naive:
            local_time = occurrence.replace(tzinfo=None)
        elif tz == utc:
            local_time = occurrence.astimezone(utc)
        else:
            utc_time = occurrence.astimezone(utc)
            local_time = utc_time.astimezone(tz)
        print(local_time.strftime("%a %Y-%m-%d %H:%M %Z %z"))
