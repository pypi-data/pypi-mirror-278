#! /usr/bin/env python3

def lag(q: int, d: int, day: int, days: int)->int:
    # return max(int(100*(f*q-d)/(q-d)), 0)
    # return max((f*q-d)/(1-f), 0.0)
    # due = max((q - d), 0.0)
    # left = 1 - f 
    # return round(((day + 1) / days) * q - d, 2)
    return round( ((q - min(d,q)) / q) * days / (days-day), 2)

    # return round((q - min(d, f * q) / (1 - f)), 2)
    # return round(due, 2), round(left, 2), round(due/left, 2) 

    # return max(int(100*(q-d)/(1-f)), 0)

late = []
late_leader = "***"
slow = []
slow_leader = "   "
summary = []

def tup2str(tup):
    return ' '.join([str(x) for x in tup]) 

days = 7
q = 14
late = []
slow = []
late_level = 2
slow_level = 1.25
print(f"for {q = }; {days = }; per-diem = {q/days:.02}")
for d in range(q):
    saved_late = False
    saved_slow = False
    for day in range(0, days):
        res = lag(q, d, day, days)
        if res >= late_level:
            if not saved_late:
                # print(f"{day = }; {days = }; {late_level = }; {slow_level = }")
                summary.append(tup2str([late_leader, day, d, res]))
                saved_late = True
                print(f"{late_leader} {day} {d=} d/q={d/q:.04} f={day/days:.04} lag = {res} vs {slow_level}, {late_level}")
        elif res >= slow_level:
            if not saved_slow:
                # print(f"{day = }; {days = }; {late_level = }; {slow_level = }")
                summary.append(tup2str([slow_leader, day, d, res]))
                saved_slow = True
                print(f"{slow_leader} {day} {d=} d/q={d/q:.04} f={day/days:.04} lag = {res} vs {slow_level}, {late_level}")
        # else:
        #     print(f"      {i} lag(s{q}, {d}, {f:.02}) = {res}")

# print(f"\nfor days = quota = {days}:\n  {'\n  '.join(summary)}\n")
# print(f"late for days = quota = {days}:\n  {'\n  '.join(late)}\n")


 