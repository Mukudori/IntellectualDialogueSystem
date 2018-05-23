from datetime import datetime
from calendar import Calendar

def getNumWeek():
    now = datetime.now()
    now_year = now.year

    if now.month > 6:
        first_month = 9
    else:
        first_month = 2
    sum_week = 0
    for i in range(first_month, now.month):
        sum_week+=len(Calendar().monthdatescalendar(now_year, i))
    if sum_week % 2 :
        num_week = 1
    else:
        num_week = 2

    return num_week

def getNumNextWeek():
    now_week = getNumWeek()
    if now_week == 1:
        return 2
    else:
        return 1

def getWeekDay(num_week = 0):
    if not num_week: num_week = getNumWeek()
    if num_week == 1:
        numDay = num_week
    else:
        numDay = num_week + 7
    return numDay

def getDayTupleForThisWeek():
    first_day = getWeekDay()
    return (i for i in range(first_day-2,first_day+5))

def getDayTupleForNextWeek():
    this_week = getNumWeek()
    if this_week == 1:
        first_day = getWeekDay(2)
    else:
        first_day = getWeekDay(1)
    return (i for i in range(first_day-2, first_day + 5))






def getTimeList():
    return ['8:30-10:00',
            '10:10-11:40',
            '12:10-13:40',
            '13:50-15:20',
            '15:30-17:00',
            '17:10-18:40']
