import timeBasedSending
import getShabad
import reply
import getTime
import time

dayCount=1


#sends the hukamnama every day
sendToEveryOne = timeBasedSending.sendHukam().start()  #thread 1

#sends shabad every hour
toMe = timeBasedSending.ShabadEveryHour().start()  #thread 2

bani=getShabad.GetShabad()
r = reply.Reply()
while True:
    print(f"Day) {dayCount} : {getTime.getCurrentDatetime()}")
    hukamnam=bani.getHukamnama()
    while True:
        nowTime=getTime.getCurrentTime()
        try:
            r.sendReplies(hukamnam, bani)  #main thread
        except Exception as e:
            print(f"Failed at {nowTime}")
            print(e)
        
        if getTime.getCurrentTime()==timeBasedSending.timeToSendDailyHukam:
            #sleepling so it doesnt keep breaking from the while loop and adding +1 to dayCount
            time.sleep(60)
            break
    dayCount+=1

#run scrpit in background: nohup python3 -u ~/projects/sms-shabad/main.py &
#look at background scripts running: ps ax |grep main.py
# stop a script: kill PID
# I followed this link to get it to run
#https://janakiev.com/blog/python-background/
