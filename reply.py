from sendMsg import sendToPhone
import imaplib, email, re, random
import timeBasedSending
import PASSWORD

class Reply():
    def sendReplies(self, gurmukhiHukam, gurmukhiRand):
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

            a = re.search("[0-9]{10}", theNumber)
            if a != None:
                    mms = self.getCarrier(carrier)
                    if mms==carrier:
                        continue
                    phone = theNumber + mms
            else:
                    phone=whoSent # if sent from email, phone variable is equal to the email
            print(phone)
            for part in emailMessage.walk():
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    sentFromPhone = body.decode()
                    sentFromPhone = sentFromPhone.lower()

                    theShabad = f"Please enter valid value for a shabad. \"{sentFromPhone}\" is not a valid. Press 5 for options."
                    title = "Not Valid"
                    if "1" in sentFromPhone.strip():
                        title = "Random Shabad(With Gurmukhi)"
                        theShabad = gurmukhiRand
                    elif "2" in sentFromPhone.strip():
                        title = "Hukamnama fromDarbar Sahib(With Gurmukhi)"
                        theShabad = gurmukhiHukam.replace(" ","")

                    elif "3" in sentFromPhone.strip():
                        title = "added to daily hukamnama"
                        if phone not in timeBasedSending.IfTimeSendSms.people:
                            theShabad = "You have been added to the daily hukamnama list."
                            timeBasedSending.IfTimeSendSms.people.append(phone)
                        else:
                            theShabad = "You are already in the Daily hukamnam list"
                    elif "4" in sentFromPhone.strip():
                        title = "removed from daily hukamnama"
                        theShabad = "You have been removed to the daily hukamnama list."
                        try:
                            timeBasedSending.IfTimeSendSms.people.remove(phone)
                        except ValueError:
                            theShabad = "You are not in the list"

                    elif "options" in sentFromPhone.lower() or "5" == sentFromPhone.strip():
                        title = "Options"
                        theShabad ="1. random (get random shabad)\n2. Hukam(get Darbar Sahib Hukamnama)\n3. Get added to daily Hukamnama list. (you will recive the daily hukamnama at 10 am EST)\n4. Remove from daily Hukamnama list\n5. See Options again\n(Type the corresponding number of the option you want to select!!)"
                    elif "$allgurmukhi" in sentFromPhone:
                        title = "shUUU"
                        theShabad = str(gurmukhiRand)
                    sendToPhone(title, theShabad, phone)
                    print("sent")

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


