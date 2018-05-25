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
    weekday = datetime.today().weekday()+1
    if num_week == 1:
        numDay = weekday
    else:
        numDay = weekday + 6
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

def getMinuts(hours,minuts):
    return hours*60+minuts

def getNumLesson():
    now = datetime.now()
    hours, minuts = (now.hour, now.minute)
    now = getMinuts(hours,minuts)

    lessonTime = [(getMinuts(8,30), getMinuts(10,0)),
                  (getMinuts(10,10), getMinuts(11,40)),
                  (getMinuts(12,10), getMinuts(13,40)),
                  (getMinuts(13,50), getMinuts(15,20)),
                  (getMinuts(15,30), getMinuts(17,00)),
                  (getMinuts(17,10), getMinuts(18,40))]

    for i in range(len(lessonTime)):
        if now>=lessonTime[i][0] and now<=lessonTime[i][1]:
            return i+1





def getTimeList():
    return ['8:30-10:00',
            '10:10-11:40',
            '12:10-13:40',
            '13:50-15:20',
            '15:30-17:00',
            '17:10-18:40']
