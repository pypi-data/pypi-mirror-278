import requests as r
from bs4 import BeautifulSoup as s
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from tabulate import tabulate_formats
import time 
from colorama import Fore,Back,Style

data={}
detail={}

## td.find("input")
## inp["value"]
##


def personal():
      print('Personal Details:')
      url_response=session.get(url)
      text=url_response.text
      html_text=s(text,'html.parser')
      tables=html_text.find('table',class_='table table-bordered table-striped')
      
      data=[]
      index=0
      for row in tables.find_all('tr'):
       
       if index!=1:
            row_data=[]
           
            for cell in row.find_all(['th','td']):
                  
                  row_data.append(cell.get_text().strip())
            data.append(row_data)
       index+=1
     
      df=pd.DataFrame(data)
      #df=df.T[0,1]
      df=df[1:]
      df=df[[0,1]]
      print(tabulate(df,tablefmt='heavy_grid'))
      #print(df)


def attendance():
      erp_response=session.get(url)
      html_text=erp_response.text
# print(html_text)
      soup_text=s(html_text,'html.parser')
      title=soup_text('title')
#for t in title:
 #print(t.text)

      print('\nStudent Detail\n')
      div_class=soup_text('div',class_='col-md-4')
      for table in div_class:
           table=table
           trs=table.find_all('tr')

           for index,tr in enumerate(trs):
                   if index!=0:
                       detail[index]=tr.text.split('\n') 
  #print(f"{tr.text}")
      df1=pd.DataFrame(detail)
      df1=df1[1:3]
      #print(df1.T)
      print(tabulate(df1.T,tablefmt='heavy_grid'))

      print("\nAttendance Detail\n")
      div_class=soup_text('div',class_='col-md-12')
      for table in div_class:
             table=table
#  print(table.text)
             trs=table.find_all('tr')

             for index,tr in enumerate(trs):
                    data[index]=tr.text.split('\n')
#print(data)
      df=pd.DataFrame(data)
     # print(tabulate(df,tablefmt='heavy_grid'))
      df.to_csv('attendance.csv',index=False)
    #print(df.T)
      df_p=df
      df=df.iloc[[0,2,5]]
      print(tabulate(df.T,tablefmt='heavy_grid'))
      #print(df.T)
      print("\nLess Attendace Subject List:\n")
      subject=df_p.T[1].tolist()
      percentage=df_p.T[5].tolist()
      percentage.pop(0)
      subject.pop(0)
      percentage1=[]
      ctr=0
      for i in range(len(percentage)):
         a=int(percentage[i][:-2])
         percentage1.append(a)
         x=[]
         if a<75:
           a=75-a
           #a=Fore.RED+str(a)
           #subject[i]=Fore.RED+subject[i]
           x.append(f"You have  {a}% less attendace in {subject[i]}")
           print(f"You have  {a}% less attendace in {subject[i]}")
           #print(Style.RESET_ALL)
           #xf=pd.DataFrame(x)
          # print(xf)
           #print(tabulate(x,tablefmt='heavy_grid'))
         ctr+=1
      if ctr==0:
           print("You have more than 75% in all subjects\n")
           
      flag=input('Do you want to see graph?(Y/N)')
      if flag.upper()=='Y':
        plt.figure()
        plt.plot(subject,percentage1,'b-',marker='*')
        plt.plot(subject,[75,75,75,75,75,75,75,75,75],'r--',label='75% ')
        plt.title("Attendance Graph")
        plt.xlabel("Subjects")
        plt.ylabel("Attendance Percentage") 
        plt.legend()
        suffix=str(time.time())
        
        plt.savefig(f'{suffix[5:10]}.png')
        plt.show()
        
        #print(time.time())
       # name=str(time.time())
        

def evaluation():
      
      erp_response=session.get(url)
      html_text=erp_response.text
      # print(html_text)
      soup_text=s(html_text,'html.parser')
      title=soup_text('title')
      for t in title:
       print(t.text)
       tables1=soup_text.find('div',class_='col-md-12')
       trs=tables1.find_all('tr')

      #ths=trs[0].find_all('th')
      table={}
      for index,tr in enumerate(trs):
        table[index]=tr.text.split("\n")
      df=pd.DataFrame(table)
      df=df[1:3]
      #print(df.T)
      print(tabulate(df.T,tablefmt='heavy_grid'))

      choice=int(input("Select Course No.: "))

      #print(f'{df[choice]}')
      sf=df[choice]
      #print(tabulate(sf[1:3],tablefmt='plain'))
      formats=tabulate_formats
     # for i in formats:
       #  print(i)
       #  print(tabulate(sf,headers='firstrow',tablefmt=i))
      print()
      subject=sf[1]
      sub=sf[2]
      print(sub)
      #print(tabulate(sub,tablefmt='heavy_grid'))
      #query string parameter https://v1.nitj.ac.in/erp/evaluation_report_detail?subject=ECDC0102
      erp_response=session.get(f'https://v1.nitj.ac.in/erp/evaluation_report_detail?subject={subject}')

      html_text=erp_response.text
      # print(html_text)
      soup_text=s(html_text,'html.parser')
      tables=soup_text.find('table',id='example')
      data=[]
      for row in tables.find_all('tr'):
           
            row_data=[]
            
            for cell in row.find_all(['th','td']):
                  cell_text=cell.get_text()
                  clean_text=cell_text.replace('\n',' ').strip()
                  row_data.append(clean_text)
                 
            data.append(row_data)
      df=pd.DataFrame(data)
      print(tabulate(df.T,tablefmt='heavy_grid'))
    #  print(df.T)

        
      
def result(url2='https://v1.nitj.ac.in/erp/result/result_1_2023/user_home'):
     
     response2=session.get(url2)  
     #print(response2) 
     response2=response2.text
     response2=s(response2,'html.parser')
     title=response2.find('title')
     print(title.text)
     response2=response2.find('div',class_='col-md-12') 
     
     tables=response2.find_all('table')
     
     for i,tables in enumerate(tables):
      if i==0:
        data=[]
     
        for index2,row in enumerate(tables.find_all('tr')):
            row_data=[]
            if index2!=12:
                    for index,cell in enumerate(row.find_all(['td','th','input'])):
                        row_data.append(cell.text)                       
                    data.append(row_data)
        df=pd.DataFrame(data)
        

        df=df.T[1:]
        print(tabulate(df.T,tablefmt='heavy_grid'))
        #print(df.T)
      else:
           data=[]
           for row in tables.find_all('tr'):
                row_data=[]
                for i,cell in enumerate(row.find_all('td')):
                   if  i==0:
                        row_data.append(cell.text) 
                   else:
                        cell=cell.find('input')
                        x=cell.get('value')
                        row_data.append(x)
                data.append(row_data)
           df=pd.DataFrame(data)
           print(tabulate(df,tablefmt="heavy_grid"))
      c=input("download result(Y/N): ").upper()
      if c=='Y':
                 header={
                      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, br, zstd',
'Accept-Language': 'en-US,en;q=0.9',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
# 'Cookie': 'erp_login=52edf58b2ccfd07ab5de13e3d09be698; PHPSESSID=2go62bocmvh6vj9bumd3boisf3',
'Host': 'v1.nitj.ac.in',
'Pragma': 'no-cache',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'none',
'Sec-Fetch-User': '?1',
'Sec-GPC': '1',
'Upgrade-Insecure-Requests':'1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
'sec-ch-ua': '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "Linux"
                 }
                 rp=session.get('https://v1.nitj.ac.in/erp/result/result_1_2023/app/fpdf/result-pdf',headers=header)
                 rp=rp.content
                 
                 with open('result.pdf',mode='wb') as fhand:
                     fhand.write(rp)   
#for websites which need authentication
session=r.Session()
# rolln=23104055
# password=''
# #options
# choice=input("New user(Y/N)")
# if choice.upper()=='Y':

print(Fore.BLUE,"\nWelcome to pyErp")
print(Style.RESET_ALL)
rolln=input("Enter username(roll no.): ")
password=input("Enter password: ")

login_data={

             'username': rolln ,
             'pwd': password,
             'login':''

            }

# erp_response=r.get("https://v1.nitj.ac.in/erp/login")
# print('website status: '+str(erp_response))
erp_response=session.post('https://v1.nitj.ac.in/erp/login',data=login_data)
#print('login status: '+str(erp_response))
if erp_response.status_code==200:
            print('\n Logged in Successfully \n')
else:
             print('\n ERP Login Failed\n')

html_text=erp_response.text
Soup_text=s(html_text,'html.parser')

#extraction from soup_text
urls_text=Soup_text.find_all('a')

flag=1
while flag:
      for index,link in enumerate(urls_text):
            if index in [5,6,7,11]:
     #print(f'Link {index} : {link.get('href')}')
               print(f'Option {index} : {link.text}')
      index=int(input('\nChoose Option :'))
      url=urls_text[index]
      url=url.get('href')
      #print(url)
      if index==5:
            personal()
      elif index==6:
            attendance()
      elif index==7:
            evaluation()
      elif index==11:
            result()
           
      flag=input("Continue(Y/N)").upper()
      if flag=='Y':
            flag=1
      else:
            flag=0
def exit():
    pass