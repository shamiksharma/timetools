
import os, time, datetime
import sys, getopt
import arrow

# ----------------------------------------------------
# Wrapper around Arrow time manipulation library
#
# 0. Setup
#
# pip install arrow
# read doc at http://crsmithdev.com/arrow/
#
# 1. Create 
#
# a = arrow.get(0)            <Arrow [1970-01-01T00:00:00+00:00]>
# a = arrow.get("2016-04-01 12:00:00")  
# a = arrow.get()             same as arrow.utcnow()
# 
# 2. Output 
# 
# a = arrow.get()
# epochInt = a.timestamp       1459650327
# dateStr  = a.format()        or a.format('YYYY-MM-DD HH:mm:ss ZZ')
# humanStr = a.humanize()      "2 days ago"
#
# 3. Manipulate
#
# localDate = a.to('local')       server's local time
# localDate = a.to('US/Pacific')  for bay area
# localDate = a.to('+05:30')      for India
# 
# 4. Get a new date
#
# b = a.replace(days=+7)          new Arrow object 7 days hence
# b = a.replace(weeks=+2)         new Arrow object 14 days hence
#
# --------------------------------------------------

#
#  Internal function to create an Arrow object
#
def _getArrow(date=None):
    if (date == "now") : 
        date = arrow.utcnow() 
    else:
        date = arrow.get(date)
    return date



#
#  Convenient function to get current time as Epoch timestamp
#  Note that Epoch is always UTC
#
def nowEpoch():
    return arrow.utcnow().timestamp

#
#  Convenient function to get current UTC time as string
#  Will look like "2016-04-01 12:34:59"
#
def now():  
    return arrow.utcnow().format()

#
#  Convenient function to get current Local time (of server)
#  Will look like "2016-04-01 12:34:59 +05:30 for India"
#
def nowLocal():
    return arrow.utcnow().to('local')

#
#  Convert a UTC date string to local TZ (of server)
#
def local(utcdate) :
    a = _getArrow(utcdate)
    return a.to('local').format()


#
#  Check if its a weekday. returns Bool
#
def isWeekDay(date=None):
    a = _getArrow(date).to('local')
    return True  if (a.isoweekday() < 6) else False  # [1..7] for [Mon..Sun]

#
#  Convert from date-string to UTC-Epoch or vice-versa
#   
def convert(date):
    a = _getArrow(date)
    if isinstance(date,(int,long)): 
        return a.format()
    else:  
        return a.timestamp
#
#  Check if any two times are the same within some period granularity
#  The period granularity can be "minute" "day" "month" "year"
#   
def same(date1, date2, period="day"):   # checks if same day (rounds to midnight)
    e1 = _getArrow(date1).ceil(period).timestamp
    e2 = _getArrow(date2).ceil(period).timestamp
    return True if (e1==e2) else False

#
#  Returns a UTC date-string that is N weeks after the provided date
# 
def nextWeek(date=None,num_weeks=1):   
    a = _getArrow(date)
    return a.replace(weeks=+num_weeks).format()

#
#  Returns a UTC date-string that is N days after the provided date
# 
def nextDay(date=None,num_days=1):   
    a = _getArrow(date)
    return a.replace(days=+num_days).format()

#
#  Returns a UTC date-string that is N days after the provided date
# 
def nextMonth(date=None,num_months=1):   
    a = _getArrow(date)
    return a.replace(months=+num_days).format()

#
# Parses out the month, day, year etc. from a given date
#
# "ddd"=[Mon..Sun], 
# "d"  =[1..7], 
# "D"  =[1..31]
# "DDD" = [0..365]    day of year
# "M"  =[1..12]
# "YYYY"  =  [0..2016]
# "H"  = [0..24]
# "h"  = [0..12]
# "m"  = [0..59]
# "s"  = [0..59]
#
def parseDate(date, fmt="ddd"): 
    a = _getArrow(date)
    return a.to('local').format(fmt)



# ------------------------------------------
#
# Unit Tests
#
# ------------------------------------------

def runTest(args) :
    if len(args) > 1 : 
        dateZ = args[1]       # test with "now" or "1969-01-01 13:01:34"
    else :
        dateZ	= now()

    newDate = convert(convert(dateZ))
    nxt     = nextDay(newDate,7)
    print "Date : %s \n New Date : %s \n  Next : %s \n"  % (dateZ, newDate, nxt)
    wkday   = isWeekDay(newDate)
    str     = parseDate(newDate, "ddd")
    samer   = same(dateZ,nxt,"month")
    print "Weekday: %s \n Part of date: %s  \n same-month: %s " % (wkday,str,samer)


    


# ------------------------------------------
#
# A general scaffolding for all python modules
#
# ------------------------------------------


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
             
        runTest(argv)

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
