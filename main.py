# from keepAlive import KeepAlive
import timeBasedSending
import getShabad
import reply
import time
import datetime

dayCount=1
while True:
    # KeepAlive()
    print(f"Day: {dayCount}\n")
    #sends the hukamnama every day
    sendToEveryOne = timeBasedSending.IfTimeSendSms() 
    sendToEveryOne.start()  #thread 1

    #sends shabad every hour
    toMe = timeBasedSending.ShabadEveryHour()
    toMe.start()  #thread 2

    bani=getShabad.GetShabad()
    hukamnam=bani.getHukamnama()

    r = reply.Reply()
    while True:
        r.run(hukamnam, bani.getRandomShabad())  #main thread
        time.sleep(5)
        a = datetime.datetime.now()
        nowTime = a.strftime("%I:%M %p")
        if nowTime == "09:00 AM":
            break
