from allNumbers import allNumbers
from sendMsg import sendToPhone
import imaplib, email, re
import PASSWORD
import getTime

def write_dict_to_file():
    with open("./allNumbers.py",'w') as file:
        file.write("allNumbers={\n")
        for num in allNumbers:
            newLine=f'    "{num}"     :   "{allNumbers[num]}",\n'
            file.write(newLine)
        file.write("}")

def removePersonToHukamList(num):
    allNumbers.pop(num)
    write_dict_to_file()

def addPersonToHukamList(num):
    allNumbers[num]="Unknown"
    write_dict_to_file()

def getOutputData(n):
    data=""
    with open("./nohup.out") as file:
        lines=file.readlines()
        startInd=0
        if len(lines)>n:
            startInd=len(lines)-n
        for i in range(startInd,len(lines)):
            data+=lines[i]
    return data

class Reply():
    def sendReplies(self, hukamnama, bani):
        host = "imap.gmail.com"
        user = "giansingh131313@gmail.com"
        password = PASSWORD.password

        mail = imaplib.IMAP4_SSL(host)
        mail.login(user, password)
        mail.select("inbox")

        _, searchData = mail.search(None, "UNSEEN")
        for num in searchData[0].split():
            _, data = mail.fetch(num, "(RFC822)")
            _, b = data[0]
            emailMessage = email.message_from_bytes(b)
            whoSent = emailMessage["From"]

            theNumber = whoSent.split("@")[0]
            carrier = whoSent.split("@")[1]

            phone="";
            a = re.search("[0-9]{10}", theNumber)
            if a != None:
                mms = self.getCarrier(carrier)
                if mms==carrier:
                    continue
                phone = theNumber + mms
            else:
                phone=whoSent # if sent from email, phone variable is equal to the email

            for part in emailMessage.walk():
                # print(part.get_content_type())
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    sentFromPhone = body.decode()
                    sentFromPhone = sentFromPhone.lower()
                    msgFromUser = sentFromPhone.strip()

                    theShabad = f"Please enter a valid value. \"{sentFromPhone}\" is not a valid\n"
                    title = "Not Valid"

                    if "$shabadlist" == msgFromUser:
                        title="All people in Daily Hukam List"
                        theShabad=str(allNumbers)
                    elif "$update" == msgFromUser:
                        title="Last 30 lines of output"
                        theShabad=getOutputData(30)
                    elif "$updatemore" == msgFromUser:
                        title="Last 100 lines of output"
                        theShabad=getOutputData(100)
                    elif "$updateall" == msgFromUser:
                        title="All the data of the output"
                        theShabad=getOutputData(10000000000)
                    elif "$add"==msgFromUser[:4]:
                        phoneToAdd=msgFromUser[5:].strip()
                        title=f"Couldn't add {phoneToAdd}"
                        theShabad="Couldn't send message to {phoneToAdd}"
                        try:
                            vg="ਵਾਹਿਗੁਰੂ"
                            sendToPhone(vg,"You have been added to daily hukamnama list!!!",phoneToAdd)
                            if phoneToAdd not in allNumbers:
                                addPersonToHukamList(phoneToAdd)
                                title=f"added {phoneToAdd}"
                                theShabad = f"{phoneToAdd} has been added to the daily hukamnama list."
                            else:
                                title=f"{phoneToAdd} is already in the list"
                        except Exception as e:
                            print(f"{theShabad}: {e}")
                    elif "$gupt"==msgFromUser:
                        title=""
                        theShabad="Gupt actions:\n $shabadlist: Shows all people in Daily Hukam List\n $update: Shows last 30 lines of the output\n $updatemore: Shows last 100 lines of output\n $updateall: Shows all the data in outputfile\n $add: follow this command with a phonemuber with its MMS gateway, exp: 6782670271@pm.sprint.com\n $gupt: Get this menu"

                    elif "1" in msgFromUser:
                        title = "Random Shabad (With Gurmukhi)"
                        theShabad=bani.getRandomShabad()
                    elif "2" in msgFromUser:
                        title = "Hukamnama from Darbar Sahib(With Gurmukhi)"
                        theShabad = hukamnama.replace(" ","")
                    elif "3" in msgFromUser:
                        title = "added to daily hukamnama"
                        if phone not in allNumbers:
                            addPersonToHukamList(phone)
                            theShabad = "You have been added to the daily hukamnama list."
                        else:
                            theShabad = "You are already in the Daily hukamnam list"
                    elif "4" in msgFromUser:
                        title = "Removed from Daily Hukamnama"
                        if phone in allNumbers:
                            removePersonToHukamList(phone)
                            theShabad = "You have been removed to the daily hukamnama list."
                        else:
                            theShabad = "You are not already in the Daily hukamnam list"
                    else:
                        theShabad ="Type the number for the corresponding action:\n1. random (get random shabad)\n2. Hukam (get Darbar Sahib Hukamnama)\n3. Get added to daily Hukamnama list. (you will recive the daily hukamnama at 10 am EST)\n4. Remove yourself from daily Hukamnama list\n"
                    
                    nowTime=getTime.getCurrentDatetime()
                    print(f"{phone} : {msgFromUser}. Replied with {title} at {nowTime}")
                    sendToPhone(title, theShabad, phone)

    def getCarrier(self, car):
        opts = {
            'txt.att.net': '@mms.att.net',
            'sms.myboostmobile.com': '@myboostmobile.com',
            'mms.cricketwireless.net': '@mms.cricketwireless.net',
            'msg.fi.google.com': '@msg.fi.google.com',
            'messaging.sprintpcs.com': '@pm.sprint.com',
            'vtext.com': '@vzwpix.com',
            'tmomail.net': '@tmomail.net',
            'message.ting.com': '@message.ting.com',
            'email.uscc.net': '@mms.uscc.net',
            'vmobl.com': '@vmpix.com',
            'mms.att.net': '@mms.att.net',
            'myboostmobile.com': '@myboostmobile.com',
            'pm.sprint.com': '@pm.sprint.com',
            'vzwpix.com': '@vzwpix.com',
            'mms.uscc.net': '@mms.uscc.net',
            'vmpix.com': '@vmpix.com',
            'gmail.com':'@gmail.com',
            'yahoo.com':'@yahoo.com'

        }
        ans=car
        try:
            ans=opts[car]
        except Exception as e:
            print(e)
        return ans
