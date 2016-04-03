# timetools
Python library to help manipulate time and timestamps

```python

    import timetools as t

    dateZ	= t.now()                       # "2014-06-03 12:00:00"
    newDate = t.convert(dateZ)              # 1456990232  as a timestamp
    nxt     = t.nextDay(newDate,7)          # a date 7 days later

    wkday   = t.isWeekDay(newDate)          # True if its a Weekday
    str     = t.parseDate(newDate, "ddd")   # Parses out the day of the week "Sun"
    samer   = t.same(dateZ,nxt,"month")     # check if two dates are same month

```  
