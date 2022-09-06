import timeBasedSending
import getShabad
import reply
import getTime
import time

dayCount=1


#sends the hukamnama every day
sendToEveryOne = timeBasedSending.sendHukam().start()  #thread 1

#sends shabad every hour
# toMe = timeBasedSending.ShabadEveryHour().start()  #thread 2

bani=getShabad.GetShabad()
r = reply.Reply()
while True:
    print(f"Day) {dayCount} : {getTime.getCurrentDatetime()}")
    hukamnam=bani.getHukamnama()
    while True:
        nowTime=getTime.getCurrentDatetime()
        try:
            r.sendReplies(hukamnam, bani)  #main thread
        except Exception as e:
            if "AUTHENTICATIONFAILED" in e.__str__():
                print(f"AUTHENTICATION FAILED (failed to connect to gmail server): {nowTime}")
            else:
                print(f"Error: {e} at {nowTime}")
            time.sleep(2)


        if getTime.getCurrentTime()==timeBasedSending.timeToSendDailyHukam:
            #sleepling so it doesnt keep breaking from the while loop and adding +1 to dayCount
            time.sleep(60)
            break #the reason we break is so we can set the hukamnam variable to a new shabad
    dayCount+=1

#run scrpit in background: nohup python3 -u ~/projects/sms-shabad/main.py &
#look at background scripts running: ps ax |grep main.py
# stop a script: kill PID
# I followed this link to get it to run
#https://janakiev.com/blog/python-background/
