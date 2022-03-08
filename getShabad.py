import requests,json,random
from bs4 import BeautifulSoup as bs
from SantJiKathas import KATHAS

class GetShabad():
    def  __init__(self):
        self.santJiKhata=KATHAS
        
    def getRandomShabadLocal(self):
        with open("./allShabads.json",encoding="utf-8") as f:
            data=json.load(f)
        rand=random.choice(list(data.items()))
        return rand[1]
 
    def getRandomShabad(self):
        shabad=""
        try:
            url="https://api.gurbaninow.com/v2/shabad/random"
            shabadJson=requests.get(url).json()
            shabadId=shabadJson['shabadinfo']['shabadid']
            angNum=shabadJson['shabadinfo']['pageno']
            shabad=shabadJson['shabad']
            shabad=self.getShabadFromJson(shabad,angNum)
            print("API SUCCESS. Got Random Shabad Through Api.")
        except Exception as e:
            print(e)
            print("Couldn't get shabad from api so getting from allShabads.json")
            shabad=self.getRandomShabadLocal()
        return shabad

    def getHukamnama(self):
        url="https://api.gurbaninow.com/v2/hukamnama/today"
        shabad="Error"
        try:
            shabadJson=requests.get(url)
            shabadJson=shabadJson.json()
            shabadId=shabadJson['hukamnamainfo']['shabadid'][0]
            angNum=shabadJson['hukamnamainfo']['pageno']
            hukam=shabadJson['hukamnama']
            shabad=self.getShabadFromJson(hukam,angNum)
            print("API SUCCESS.Got Hukam Through Api.")
        except Exception as e:
            print("Error getting Hukamnama... Got Hukam from allShabads.json")
            print(e)
            shabad=self.getRandomShabadLocal()
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


# headers = {
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language': 'en-US,en;q=0.5',
    # 'DNT': '1',
    # 'Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': '1',
# }

# def getHukamnama():
    # url="https://api.gurbaninow.com/v2/hukamnama/today"
    # shabad="Error"
    # shabadJson=requests.get(url,headers=headers)
    # print(shabadJson)
    # shabadJson=shabadJson.json()
    # shabadId=shabadJson['hukamnamainfo']['shabadid'][0]
    # angNum=shabadJson['hukamnamainfo']['pageno']
    # hukam=shabadJson['hukamnama']
    # shabad=self.getShabadFromJson(hukam,angNum)
    # return shabad
# a=getHukamnama()
# print(a)
# headers = {
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Language': 'en-US,en;q=0.5',
    # 'DNT': '1',
    # 'Connection': 'keep-alive',
    # 'Upgrade-Insecure-Requests': '1',
# }
# url="https://api.gurbaninow.com/v2/hukamnama/today"
# response = requests.get(url, headers=headers)
# print(response)
