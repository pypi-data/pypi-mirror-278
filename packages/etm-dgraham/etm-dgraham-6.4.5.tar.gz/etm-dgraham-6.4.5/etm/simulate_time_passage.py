#! /usr/bin/env python3
from datetime import datetime, timedelta
import time
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
start_date = datetime(2024, 3, 10, 0, 30, tzinfo=tzinfo)  
# start_date = datetime(2024, 11, 3, 0, 30, tzinfo=tzinfo)  

float = is_naive(start_date)

def simulate_time_passage(start_time, end_time, interval_seconds):
    current_time = start_time
    while current_time <= end_time:
        print(f"Current simulated time: {current_time}")
        # Create a recurrence rule for daily events
        # rule = rrule(freq=DAILY, dtstart=start_date)
        # rule = rrule(
        #     freq=DAILY,
        #     dtstart=current_time.replace(hour=0, minute=30),
        #     until=current_time.replace(hour=3, minute=30),
        #     byhour=[0, 1, 2, 3],
        #     byminute=[30]
        # )
        # print(rrule.__str__(rule))

        # Generate the next 14 occurrences of the event
        occurrences = [dt for dt in rule[:4] if dt >= current_time]
        for occurrence in occurrences:
            if float:
                occurrence = occurrence.replace(tzinfo=tzinfo)
            if tzinfo == naive:
                local_time = occurrence.replace(tzinfo=None)
            elif tzinfo == utc:
                local_time = occurrence.astimezone(utc)
            else:
                utc_time = occurrence.astimezone(utc)
                local_time = utc_time.astimezone(tzinfo)
            print(local_time.strftime("%a %Y-%m-%d %H:%M %Z %z"))

        current_time += timedelta(seconds=interval_seconds)
        time.sleep(1)  # Pause to simulate real-time passage

# Define the start and end time for the simulation
# start_time = datetime(2024, 11, 3, 0, 29, tzinfo=tzinfo)
# end_time = start_time + timedelta(hours=3)

for start_time in [
    datetime(2024, 3, 10, 0, 29, tzinfo=tzinfo),
    datetime(2024, 11, 3, 0, 29, tzinfo=tzinfo),
    ]:
    end_time = start_time + timedelta(hours=3)
    # Simulate passage of time in one-minute intervals
    rule = rrule(
        freq=DAILY,
        dtstart=start_time.replace(hour=0, minute=30),
        until=start_time.replace(hour=3, minute=30),
        byhour=[0, 1, 2, 3],
        byminute=[30]
    )
    print(rrule.__str__(rule))
    simulate_time_passage(start_time, end_time, 60*60)
