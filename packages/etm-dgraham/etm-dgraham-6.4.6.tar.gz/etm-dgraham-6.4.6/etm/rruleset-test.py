from datetime import datetime
from dateutil.rrule import rrule, rruleset, DAILY, rrulestr
from dateutil.tz import gettz
import textwrap

def is_naive(dt):
    return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None

# Function to create a string representation of the rruleset
def rruleset_to_string(rruleset_obj):
    parts = []
    # parts.append("rrules:")
    for rule in rruleset_obj._rrule:
        # parts.append(f"{textwrap.fill(str(rule))}")
        parts.append(f"{'\\n'.join(str(rule).split('\n'))}")
    # parts.append("exdates:")
    for exdate in rruleset_obj._exdate:
        parts.append(f"EXDATE:{exdate}")
    # parts.append("rdates:")
    for rdate in rruleset_obj._rdate:
        parts.append(f"RDATE:{rdate}")
    return "\n".join(parts)

# Define the timezone (replace 'America/New_York' with your specific timezone)
pacific = gettz('US/Pacific')
mountain = gettz('America/Denver')
central = gettz('US/Central')
eastern = gettz('America/New_York')
local = gettz()
utc = gettz('UTC')
naive = None

tz = eastern
# Define the start date
start_date = datetime(2024, 10, 28, 13, 30, tzinfo=tz)  # 0:30 on Mon Oct 28, 2024

rules_lst = []

# Create a recurrence rule for daily events
rule1 = rrule(freq=DAILY, dtstart=start_date, count=14)
rules_lst.append(str(rule1))
# Create another recurrence rule for specific days (e.g., every 2 days)
rule2 = rrule(freq=DAILY, dtstart=start_date, interval=2, count=7)
rules_lst.append(str(rule2))

# Create an rruleset
rules = rruleset()

# Add the rules to the rruleset
rules.rrule(rule1)
rules.rrule(rule2)

# Add a specific date to include
plusdates = [datetime(2024, 11, 4, 13, 45, tzinfo=tz), datetime(2024, 11, 5, 15, 15, tzinfo=tz)]
for dt in plusdates:
    rules.rdate(dt)
    rules_lst.append(dt.strftime("RDATE:%Y%m%dT%H%M%S"))

# Add a specific date to exclude
minusdates = [datetime(2024, 11, 4, 13, 30, tzinfo=tz),]
for dt in minusdates:
    rules.exdate(dt)
    rules_lst.append(dt.strftime("EXDATE:%Y%m%dT%H%M%S"))

# Generate the occurrences of the event
occurrences = list(rules)


print(f"\nrules:")
print(rruleset_to_string(rules))

# Print the occurrences
print("\noccurrences from rules:")
for occurrence in occurrences:
    print(occurrence.strftime("  %a %Y-%m-%d %H:%M %Z %z"))

print("\nlist of string representations of rules:")
print('\n'.join(rules_lst))

print("\nfrom list of string representations to new rules:")
rules_from_str = rrulestr('\n'.join(rules_lst))
print(rruleset_to_string(rules_from_str))

occurrences_from_str = list(rules_from_str)
print("\noccurrences from new rules:")
for occurrence in occurrences_from_str:
    print(occurrence.strftime("  %a %Y-%m-%d %H:%M %Z %z"))