import requests as r
from bs4 import BeautifulSoup as s
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from tabulate import tabulate_formats
import time 
from colorama import Fore,Back,Style
import getpass
import tqdm
from itertools import repeat
# import pygetwindow  as gw
data={}
detail={}
url=''
## td.find("input")
## inp["value"]
##

def login():
      rolln=input("Enter username(roll no.): ")
      x=True
      while x:
            password=getpass.getpass("Enter password: ")
            cpassword=getpass.getpass("Confirm password: ")
            if password==cpassword:
                  x=False
            else:
                  print(Fore.RED,"Wrong Password! try again")
                  print(Style.RESET_ALL)
      

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
                  print(Fore.GREEN,'\n Logged in Successfully \n')
                  print(Style.RESET_ALL)
      else:
                  print(Fore.RED,'\n ERP Login Failed\n')
                  print(Style.RESET_ALL)

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
            try:
                  index=int(input('\nChoose Option :'))
            except:
                   print('Please enter valid data')
                   index=int(input('\nChoose Option :'))
            url=urls_text[index]
            url=url.get('href')
            #print(url)
      
            if index==5:
                  personal(url)
            elif index==6:
                  attendance(url)
            elif index==7:
                  evaluation(url)
            elif index==11:
                  result()
            try:
                  flag=input("Continue(Y/N): ").upper()
            except:
                  print("please enter a valid input")
                  flag=input("Continue(Y/N): ").upper()
            if flag=='Y':
                  flag=1
            else:
                  flag=0
                  flag2=input("Check for other user(Y/N): ").upper()
                  if flag2=='Y':
                        flag2=True
                        return True
                  else: 
                   
                   flag2=False
                   print(Fore.BLUE,'Have a Nice day!')
                   
                   print(Style.RESET_ALL)
                   return False
def personal(url):
      print(Fore.GREEN,'\nPersonal Details:')
      print(Style.RESET_ALL)
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


def attendance(url):
      erp_response=session.get(url)
      html_text=erp_response.text
# print(html_text)
      soup_text=s(html_text,'html.parser')
      title=soup_text('title')
#for t in title:
 #print(t.text)

      print(Fore.GREEN,'\nStudent Detail\n')
      print(Style.RESET_ALL)
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

      print(Fore.GREEN,"\nAttendance Detail\n")
      print(Style.RESET_ALL)
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
      df=df.iloc[[1,2,5]]
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
           print(f"You have ",end='')
           print(Fore.RED,f"{a}% ",end='')
           print(Style.RESET_ALL)
           print('less attendance in ',end='')
           print(Fore.RED,f'{subject[i]}')
           print(Style.RESET_ALL)

           #xf=pd.DataFrame(x)
          # print(xf)
           #print(tabulate(x,tablefmt='heavy_grid'))
           ctr+=1
      if ctr==0:
           print(Fore.GREEN,"You have more than 75% in all subjects\n")
           print(Style.RESET_ALL)
      try:
            flag=input('Do you want to see graph?(Y/N)')
      except:
           print("please enter valid input")
           flag=input('Do you want to see graph?(Y/N)')

      if flag.upper()=='Y':
      #   s_width,s_height=gw.getWindowsWidthTitle('')[0].size
      #   dpi=100
      #   fig_width=s_width/dpi
      #   fig_height=s_height/dpi
        fig_width=12
        fig_height=10
        dpi=100
        fig=plt.figure(figsize=(fig_width,fig_height),dpi=dpi)
        #plt.figure()
        plt.plot(subject,percentage1,'b-',marker='*')
        per_75=list(repeat(75,len(subject)))
        plt.plot(subject,per_75,'r--',label='75% ')
        plt.title("Attendance Graph")
        plt.xlabel("Subjects")
        plt.ylabel("Attendance Percentage") 
        plt.legend()
        suffix=str(time.time())
        
        plt.savefig(f'{suffix[5:10]}.png')
        plt.show()
        
        #print(time.time())
       # name=str(time.time())
        

def evaluation(url):
      
      erp_response=session.get(url)
      html_text=erp_response.text
      # print(html_text)
      soup_text=s(html_text,'html.parser')
      title=soup_text('title')
      for t in title:
       print('\n')
       print(Fore.GREEN,t.text)
       print(Style.RESET_ALL)
       tables1=soup_text.find('div',class_='col-md-12')
       trs=tables1.find_all('tr')

      #ths=trs[0].find_all('th')
      table={}
      total_course=len(trs)
      for index,tr in enumerate(trs):
        table[index]=tr.text.split("\n")
      df=pd.DataFrame(table)
      df=df[1:3]
      #print(df.T)
      print(tabulate(df.T,tablefmt='heavy_grid'))
      try:
            choice=input("Select Course No.(x=all): ")
      except:
           print('please enter a valid Course No.')
           choice=input("Select Course No.: ")
      #print(f'{df[choice]}')
      if choice=='x':
           for choice in range(1,total_course):
                eval_sub_wise(df,choice)
      else:
           eval_sub_wise(df,int(choice))
      
        
def eval_sub_wise(df,choice):
      sf=df[choice]
      #print(tabulate(sf[1:3],tablefmt='plain'))
      formats=tabulate_formats
     # for i in formats:
       #  print(i)
       #  print(tabulate(sf,headers='firstrow',tablefmt=i))
      
      subject=sf[1]
      sub=sf[2]
      print('')
      print(Fore.GREEN,sub)
      print(Style.RESET_ALL)
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
def result(url2="https://v1.nitj.ac.in/erp/result/user_home"):
        response2=session.get(url2)  
        # print(response2) 
        response2=response2.text
        # print(response2)
     
        response2=s(response2,'html.parser')
        title=response2.find('title')
        # print(title.text)
        print(Fore.BLUE,"\nExamination Result")
        print(Style.RESET_ALL)
        response2=response2.find('div',class_='dataTable_wrapper') 
     
        tables=response2.find_all('table')
        for i,tables in enumerate(tables):
            sem_url=[]
            sem=0 
            if i==0:
                    data=[]
                    for index2,row in enumerate(tables.find_all('tr')):
                        
                            row_data=[]
                            
                            for index,cell in enumerate(row.find_all(['td','th','input'])):
                                    
                                            
                                            
                                row_data.append(cell.text)                       
                            data.append(row_data)
                    df=pd.DataFrame(data)
                    # print(df)
                    print(tabulate(df.T,tablefmt='heavy_grid'))
            else:
                    data=[]
                    for index2,row in enumerate(tables.find_all('tr')):
                        if index2!=1:
                            row_data=[]
                            
                            for index,cell in enumerate(row.find_all(['td','th'])):   
                                        row_data.append(cell.text)   
                                        
                        
                                        cell=cell.find('a')
                                        if cell:
                                            #print(cell.get('href'))
                                            sem_url.append(cell.get('href'))
                                                            
                            data.append(row_data)
                        
                    df=pd.DataFrame(data)
        #print(sem_url)
        sem+=1
        df1=df.T
        print(tabulate(df1,tablefmt='heavy_grid'))
        print(Fore.GREEN,"\nAvailable Results")
        print(Style.RESET_ALL)
        temp_dict={}
        for i,item in enumerate(sem_url):
            #  print(item)
             temp_dict[i]=item.split('/')[0].upper()
            #  print(i,": ",f'{item.split('/')[0].upper()}')
             print("{}: {}".format(i, item.split('/')[0].upper()))

        print('\n')
        #print(sem_url)
      #   df3=pd.DataFrame(temp_dict)
      #   print(tabulate(df3,tablefmt="heavy_grid"))
        sem_choice=int(input("Enter Serial No.:"))
        url2=f'https://v1.nitj.ac.in/erp/result/{sem_url[sem_choice]}'
        
        result_sem(url2)
            
def result_sem(url2):
    #  print(url2)
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
     try:
            c=input("download result(Y/N): ").upper()
     except:
           print("please enter a valid input")
           c=input('Download result(Y/N): ')
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
            #      rp=rp.content

                 #total_size=int(rp.headers.get('content-length',360)) 
                 total_size=354000
                 chunk=1024
                 t=tqdm.tqdm(desc="downloading" ,total=total_size,dynamic_ncols=True,unit='iB',unit_scale=True,colour='green')
                 with open('result.pdf',mode='wb') as fhand:
                     for rp_data in rp.iter_content(chunk_size=chunk):
                          t.update(len(rp_data))
                          time.sleep(0.01)
                          fhand.write(rp_data)   
                 
#for websites which need authentication
session=r.Session()
# rolln=23104055
# password=''
# #options
# choice=input("New user(Y/N)")
# if choice.upper()=='Y':

print(Fore.BLUE,"\nWelcome to myErp")
print(Style.RESET_ALL)
flag2=True
while flag2:
   flag2=login()
def exit():
    pass