import datetime
def getCurrentDatetime():
    a = datetime.datetime.now()
    return a.strftime("%m/%d/%Y, %H:%M:%S")
def getCurrentTime():
    a = datetime.datetime.now()
    return a.strftime("%I:%M %p")
    
