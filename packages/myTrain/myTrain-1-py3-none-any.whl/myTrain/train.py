import requests as r
from bs4 import BeautifulSoup as s
import pandas as pd
import json
import sys
from tabulate import tabulate
from colorama import Fore,Back,Style

def train(station):
    data={}
    date=str(input("Enter date(eg. 03) : "))
    month=str(input("Enter month(eg. 05) : "))
    for index in range(2):
        if index==0:
            search=input('Enter Source Station: ')
        else:
            search=input('Enter Destination Station: ')
  
        search=search.upper()
   
        x=len(search)
#with open('station.csv','a+') as file:
 # for key,value in station.items():
 #   file.write(str(key)+','+value)
  #  file.write('\n')
        ctr=0
        result={}

        for key,value in station.items():
  
            if value[:x]==search:
                ctr+=1
                print(ctr,station[key],station[key-1])
                result[station[key-1]]=station[key]
    #resultdf=pd.DataFrame(result)  
    #print(tabulate(resultdf,tablefmt='heavy_grid'))
        choice=int(input("choose option: "))
   
        for index1,key in enumerate(result.keys()):
      
                if index1==choice-1:
                    print(result[key],key)
                    if index==0:
                        data['SRC']=key
                    else:
                        data['DEST']=key
#for key,value in data.items():
#  print(key, value)
#print(data["SRC"],data["DEST"])
# Define the JSON data


# Define the URL
    url = "https://www.irctc.co.in/eticketing/protected/mapps1/altAvlEnq/TC"

# Define the JSON data
    data1 = {
    "concessionBooking": False,
    "srcStn": data['SRC'],
    "destStn": data['DEST'],
    "jrnyClass": "",
    "jrnyDate": "2024"+month+date,
    "quotaCode": "GN",
    "currentBooking": False,
    "flexiFlag": False,
    "handicapFlag": False,
    "ticketType": "E",
    "loyaltyRedemptionBooking": False,
    "ftBooking": False
}

# Convert the data to JSON format
    json_data = json.dumps(data1)

# Define headers
    headers = {
    "Host": "www.irctc.co.in",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.0",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": str(len(json_data)),
    "Referer": "https://www.irctc.co.in/nget/train-search",
    "greq": "1714287603035",
    "bmirak": "webbm",
    "Content-Language": "en",
    "Origin": "https://www.irctc.co.in",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Connection": "keep-alive",
    "Cookie": ""
}

# Make the POST request
    response = r.post(url, data=json_data, headers=headers)

# Print the response

    individual_dict={
                'trainNumber':[],  
                      'trainName':[],
                      'fromStnCode' :[],
                      'toStnCode' :[],
                      'arrivalTime':[],
                        'departureTime':[],
                          'distance':[],
                          'duration':[],
                          'avlClasses':[]
 
}
    d=individual_dict

    response=response.json()
    try:
        
        
        response=response['trainBtwnStnsList']
    
        for index,item in enumerate(response):
            ctr=0
            for key,value in item.items():
                if ctr>=0 and ctr<=7:
                #print(key,len(value) ,value)
                    individual_dict[key].append(value)
                elif ctr==15:
                # print(key,len(value),value)
                    individual_dict[key].append(value)
                ctr+=1
  #print(individual_dict)
            df=pd.DataFrame(individual_dict)
#df=df.sort_values(by='departureTime',ascending=True)
#df.style.hide_index()
        f2=1
        while f2:
                #print(df)
                print(tabulate(df,tablefmt='heavy_grid'))
                dfx=df
                choice=int(input("Select train: "))
                k=choice
                train_dict={
                            'trainNumber':[d['trainNumber'][k]],  
                                'trainName':[d['trainName'][k]],
                                'fromStnCode' :[d['fromStnCode'][k]],
                                'toStnCode' :[d['toStnCode'][k]],
                                'arrivalTime':[d['arrivalTime'][k]],
                                    'departureTime':[d['departureTime'][k]],
                                    'distance':[d['distance'][k]],
                                    'duration':[d['duration'][k]],
                                    'avlClasses':[d['avlClasses'][k]]
            
            }   
                train_d=pd.DataFrame(train_dict)
                #print(train_d)
                train_d=train_d.T
                print(tabulate(train_d,tablefmt='heavy_grid'))
                dfx=dfx.iloc[choice]
            # print(dfx)
                
                #print(dfx,type(dfx))
                #print(tabulate(dfx,tablefmt='grid'))

                trainNo=dfx.loc['trainNumber']
                sStn=dfx.loc['fromStnCode']
                dStn=dfx.loc['toStnCode']
                jdate="2024"+month+date

                c=dfx.loc['avlClasses']
                f1=1
                while f1:
                    print(f'Enter Class (x=all) {c} ==> ',end= ' ')
                    jclass=str(input()).upper()
                    
                    if jclass=='X':
                            for i in c:
                                jclass=i
                                class_tickets(trainNo,sStn,dStn,jdate,jclass)
                                pass
                    else:
                                class_tickets(trainNo,sStn,dStn,jdate,jclass)
                    f1=input('other class(Y/N) : ').upper()
                    if f1=='Y':
                            f1=1
                    else:
                            f1=0
                f=input('other train(Y/N) : ').upper()
                if f=='Y':
                    f2=1
                else:
                    f2=0
                f=input('other journey(Y/N) : ').upper()
                if f=='Y':
                    f3=1
                else:
                    f3=0
    except KeyError:
            #print(response)
            print(Fore.RED+'\n\n'+response['errorMessage']+'\n')
            print(Style.RESET_ALL)
            f=input('other journey(Y/N) : ').upper()
            if f=='Y':
                    f3=1
            else:
                    f3=0


def class_tickets(trainNo,sStn,dStn,jdate,jclass):
    
    data={
      "paymentFlag":"N",
      "concessionBooking":False,
      "ftBooking":False,
      "loyaltyRedemptionBooking":False,
      "ticketType":"E",
      "quotaCode":"GN",
      "moreThanOneDay":True,
      "trainNumber":trainNo,
      "fromStnCode":sStn,
      "toStnCode":dStn,
      "isLogedinReq":False,
      "journeyDate":jdate,
      "classCode":jclass
 }
    json_data=json.dumps(data)
#print(json_data)
    header={
  'Host': 'www.irctc.co.in',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0',
'Accept': 'application/json, text/plain, */*',
'Accept-Language': 'en-US,en;q=0.0',
'Accept-Encoding': 'gzip, deflate, br',
'Content-Type': 'application/json; charset=utf-8',
'Content-Length': str(len(json_data)),
'Referer': 'https://www.irctc.co.in/nget/booking/train-list',
'greq': '1714383375941',
'bmirak': 'webbm',
'Content-Language': 'en',
'bmiyek': '00DD1340D0ABB1CCF44EA92FCF28535C',
'Origin': 'https://www.irctc.co.in',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'Connection': 'keep-alive',
'Cookie': ''
}
    url=f'https://www.irctc.co.in/eticketing/protected/mapps1/avlFarenquiry/{trainNo}/{jdate}/{sStn}/{dStn}/{jclass}/GN/N'
    response=r.post(url,data=json_data,headers=header)
    response=response.json()
    decide=0
    try:
      e_msg=response['errorMessage']
      print(Fore.RED+'\n\n'+e_msg+'\n')
      print(Style.RESET_ALL)
    except KeyError:
       decide=1
    
    ticket_avl={
  'availablityDate':[],
  'availablityStatus':[],
  #4'currentBkgFlag':[],
  #'wlType':[] 
}
    detail={}
    index=0
    index2=0
    list=[1,5,6,7,8,19]
    for key,value in response.items():
      index+=1
      if index in list:
       index2+=1
       if index==19:
         detail[key]=[f"Rs{value}"]
         
       else:
         detail[key]=[value]
      elif index==29:
  
         for key,dict_v in enumerate(value):
            i=0
            for k1,i2 in dict_v.items():
              if i in [0,1]:
               if i==0:
                  ticket_avl[k1].append(i2)
               else:
                    
                    if i2[:9]=='AVAILABLE':
                      #print(i2)
                     # i2=Fore.GREEN+i2
                     
                      ticket_avl[k1].append(i2)
                      #print(Style.RESET_ALL)
                    else: 
                        
                       
                        ticket_avl[k1].append(i2)
                       
              i+=1
    if decide:
            df0=pd.DataFrame(detail)
        # print(df0.T)
            print(tabulate(df0,tablefmt='heavy_grid'))
            df1=pd.DataFrame(ticket_avl)
    
            #print(df1)
            print(tabulate(df1,tablefmt='heavy_grid'))
    
print(Fore.BLUE+'\nWelcome to PyTrain\n')
print(Style.RESET_ALL)
session=r.Session()
response=r.get('https://icf.indianrailways.gov.in/PB/pass/stations.html')
response=response.text
response_html=s(response,'html.parser')
table=response_html.find('table')
station=table.text
#print(type(station))
station_list=station.split()
#print(station_list)
station={}
for i in range(len(station_list)):
  station[i]=station_list[i]
f3=1
while f3:
    train(station)

def exit():
    pass


   


