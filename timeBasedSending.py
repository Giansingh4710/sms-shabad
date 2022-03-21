from sendMsg import sendToPhone
import time
from threading import Thread
import getShabad
import getTime

def getAllNumbers():
    from reply import allNumbers
    #importing from reply because in reply, we potentionaly change allNumbers
    return allNumbers

class ShabadEveryHour(Thread):
    def run(self):
        count=0
        while True:
            count+=1
            shabad = "ਵਾਹਿਗੁਰੂ"
            sendToPhone("Remember", shabad, "6782670271@pm.sprint.com")
            nowTime = getTime.getCurrentDatetime()
            print(f"{count}){shabad} reminder sent: {nowTime}")
            time.sleep(3600)

timeToSendDailyHukam="03:00 PM" # 10:00 AM server time
class sendHukam(Thread):
    def run(self):
        h = getShabad.GetShabad()
        while True:
            nowTime=getTime.getCurrentTime()
            if nowTime == timeToSendDailyHukam:
                numbers=getAllNumbers()
                hukam = h.getHukamnama()
                for num in numbers:
                    sendToPhone("Daily Hukam", hukam, num)
                    print(f"Sent hukamnama to {numbers[num]} at {getTime.getCurrentDatetime()}")
                time.sleep(60)


def sendBegingToAll():
    hukam = "Vaheguru Ji Ka Khalsa, Vaheguru Ji Ki Fathe.\nThis is an automated Shabad sender. You all are already in the the daily hukamanama list. To remove yourself, press '4'. There may be some bugs. Will try my best to fix as we go. (Press '5' for all options)"
    people=getAllNumbers()
    for i in people:
        sendToPhone("Hello", hukam, i)

# a=IfTimeSendSms()
# a.run()
