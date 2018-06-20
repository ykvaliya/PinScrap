from bs4 import BeautifulSoup as bs
import requests
import json
import db
import pymysql
class PinSearch:
    def __init__(self, term,term_type):
        self.term=term
        self.term_type=term_type
        self.url=''
        if (self.term_type == 'search'):
            self.url= 'https://in.pinterest.com/search/pins/?q=' + self.term
            print(self.url)

    #to get object of BeautifulSoup Object of url use getSoup()
    def getSoup(self, url):
        try:
            page=requests.get(url)
        except:
            return "Connection Error | In getSoup(self, url)"
            print("Connection Error | In getSoup(self, url)")
        if(page.status_code==200):
            soup= bs(page.content,'html.parser')
            return soup
        else:
            return "couldn't connect pintrest | In getSoup(self, url)"
            print("couldn't connect pintrest | In getSoup(self, url)")

    #to get json that contain all link to images is stored in 3rd last script
    #hance, lets try to collect 3rd last script

    def getJSONData(self, soup):
        #Collect all script into 'scripts' variable
        script= soup.find_all('script')[-3].get_text()
        try:
            jsonData = json.loads(script)
            return(jsonData)
        except:
            return "Error In getJSONData(self, soup)"
            print("Error In getJSONData(self, soup)")

    def fetchLinks(self, jsonData):
        try:
            results = jsonData['resourceDataCache'][0]['data']['results']
            links=[]
            for i in range(0,len(results)):
                links.append(results[i]['images']['orig']['url'])
            return links
        except:
            return "Error In fetchLinks(self, jsonData)"
            print("Error In fetchLinks(self, jsonData)")
    def addToDb(self, links, tag):
        conn = pymysql.Connect(host=db.host,
                             user=db.username,
                             password=db.password,
                             db=db.dbname,
                             charset='utf8mb4')
        print("Connection Successful")
        print("Total "+str(len(links))+ " links to be add to database")
        count=0
        for i in range(0,len(links)):
            with conn.cursor() as cursor:
                try:
                    qry = "insert into {table} () value ('{search}','{link}')".format(table=db.table,search=tag,link=links[i])
                    print(qry)
                    cursor.execute(qry)
                    conn.commit()
                    count=count+1
                except:
                    conn.rollback()
                    print("db.rollback() called ")

        print("Total "+str(count)+" Links Has Been Added To Database")