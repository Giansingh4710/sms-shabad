import requests,json
from bs4 import BeautifulSoup as bs
from SantJiKathas import KATHAS

class GetShabad():
    def  __init__(self):
        self.santJiKhata=KATHAS
        
    def getRandomShabad(self):
        url="https://api.gurbaninow.com/v2/shabad/random"
        shabadJson=requests.get(url).json()
        shabadId=shabadJson['shabadinfo']['shabadid']
        angNum=shabadJson['shabadinfo']['pageno']
        shabad=shabadJson['shabad']
        shabad=self.getShabadFromJson(shabad,angNum)
        return shabad

    def getHukamnama(self):
        url="https://api.gurbaninow.com/v2/hukamnama/today"
        shabadJson=requests.get(url).json()
        shabadId=shabadJson['hukamnamainfo']['shabadid'][0]
        angNum=shabadJson['hukamnamainfo']['pageno']
        hukam=shabadJson['hukamnama']
        shabad=self.getShabadFromJson(hukam,angNum)
        return shabad

    def getShabadFromJson(self,pangtiList,angNum):
        shabad=""
        for i in pangtiList:
            line=i['line']['gurmukhi']['unicode']
            translation=i['line']['translation']['english']['default']
            shabad+=line+"\n"+translation+"\n\n"
        try:
            santJi=self.santJiKhata[angNum]
            shabad+=f"\n\nKatha of Ang {angNum} By Sant Giani Gurbachan Singh Ji Bhindran Vale:\n"
            for i in santJi:
                shabad+="\nTitle: "+i['title']
                shabad+="\nLinks: "+str(i['links'])
        except KeyError:
            print(f"Sant Ji Katha not avaliable for ang {angNum}")
        return shabad

# a=SmsHukam()
# b=a.gurmukhiHukam()
# print(b)
