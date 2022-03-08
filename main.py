import timeBasedSending
import getShabad
import reply
import time
import datetime

dayCount=1

#sends the hukamnama every day
sendToEveryOne = timeBasedSending.IfTimeSendSms() 
sendToEveryOne.start()  #thread 1

#sends shabad every hour
toMe = timeBasedSending.ShabadEveryHour()
toMe.start()  #thread 2

bani=getShabad.GetShabad()
r = reply.Reply()
while True:
    #so I can get hukam daily
    hukamnam=bani.getHukamnama()
    print(f"Day: {dayCount}\n")
    while True:
        a = datetime.datetime.now()
        try:
            r.sendReplies(hukamnam, bani)  #main thread
        except Exception as e:
            print(f"Failed at {a}:")
            print(e)
        nowTime = a.strftime("%I:%M %p")
        if nowTime == timeBasedSending.timeToSendDailyHukam:
            break
    dayCount+=1

#run scrpit in background: nohup python3 -u ~/projects/sms-shabad/main.py &
#look at background scripts running: ps ax |grep main.py
# stop a script: kill PID
# I followed this link to get it to run
#https://janakiev.com/blog/python-background/
