from datetime import datetime, timedelta, date, time
from math import floor



def majority_count(member_count):
    return floor(member_count / 2) + 1 if member_count else 1



def half_hour_slots(start_hour=8, end_hour=22):
    slots = []

    current = datetime.combine(date.today(), time(start_hour))
    end = datetime.combine(date.today(), time(end_hour))

    while current < end:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)

    return slots