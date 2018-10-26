import re
from bs4 import BeautifulSoup
import requests
from recognizition import *
import matplotlib.image as mpimg
model=load_models("My_paras.h5")

url="http://202.4.152.190:8080/pyxx/login.aspx"
checkurl=r"http://202.4.152.190:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"
signurl=r"http://202.4.152.190:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"
jar=requests.cookies.RequestsCookieJar()
viewstate=''
event=''

def getusers():
    try:
        with open("pass.txt","r") as f:
            info=f.read()
        if(info==''):
            print("没有找到备份")
            raise Exception('无保存密码')
        stuid=info[:10]
        password=info[10:]
        print("stuid="+stuid)
    except:
        stuid=input("student_id=")
        password=input("password=")
    return stuid,password

# 获取用户名和密码
stuid,password=getusers()
def login():
    while(True):
        jar=get_cookies_pic()
        req=login_post(jar)
        if req.url=='http://202.4.152.190:8080/pyxx/Default.aspx':
            with open("pass.txt","w") as f:
                f.write(stuid+password)
            print("Log in Successful!")
            return jar
        else:
            print(re.findall("alert.*\)",req.text)[0])

def get_cookies_pic():
    try:
        cook=requests.get(checkurl,timeout=5)
    except:
        print("连接超时")
    jar=requests.cookies.RequestsCookieJar()
    jar.set('ASP.NET_SessionId',cook.cookies['ASP.NET_SessionId'],domain='202.4.152.190')
    with open('logcode.gif', 'wb') as f:
        f.write(cook.content)
    return jar

def get_info(jar):
    """
    output
    alist:报告列表
    viewsteta,event：重要参数
    """
    try:
        ans=requests.get("http://202.4.152.190:8080/pyxx/txhdgl/hdlist.aspx?xh="+stuid,cookies=jar,timeout=5)
    except:
        print("获取列表出现错误连接超时")
    soup=BeautifulSoup(ans.text,"html.parser")
    viewstate=soup.find(id="__VIEWSTATE").attrs['value']
    event=soup.find(id="__EVENTVALIDATION").attrs['value']
    target=soup.findAll("table")[-1]
    classnum=len(target.findAll("tr"))-1  # 报告数量
    alist=[[]]*classnum
    for n in range(classnum):
        for info in target.findAll("tr")[n+1].findAll("td")[:11]:
            alist[n]=alist[n]+[info.text]
    return alist,viewstate,event

def recogniztion(model,name):
    image=mpimg.imread(name)[:,:,0:3]
    return pre_process(model,image)


def login_post(jar):
    a=requests.get(url).text
    s=BeautifulSoup(a,"html.parser")
    
    viewstate=s.find(id="__VIEWSTATE").attrs['value']
    event=s.find(id="__EVENTVALIDATION").attrs['value']
    
    checkcode=recogniztion(model,"logcode.gif")
    
    data={"__VIEWSTATE":viewstate,
          "__EVENTVALIDATION":event,
      "_ctl0:txtusername":stuid,
      "_ctl0:txtpassword":password,
      "_ctl0:txtyzm":checkcode,
      "_ctl0:ImageButton1.x":"56",
      "_ctl0:ImageButton1.y":"12"
     }
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        req=requests.post(url,data=data,cookies=jar,headers=headers,timeout=5)
    except:
        print("连接超时")

    return req


def get_signcode():
    cook=requests.get(signurl,cookies=jar)
    with open('signcode.gif', 'wb') as f:
        f.write(cook.content)

def signclass(n):
    n=n+2
    
    get_signcode(signurl,jar)
    signcode=recogniztion(model,"signcode.gif")
    data={"__EVENTTARGET":"dgData00$_ctl"+str(n)+"$Linkbutton3",
         "__EVENTARGUMENT":"",
         "__VIEWSTATE":viewstate,
         "__EVENTVALIDATION":event,
         "txtyzm":signcode}
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
    try:
        req=requests.post("http://202.4.152.190:8080/pyxx/txhdgl/hdlist.aspx?xh="+stuid,data=data,cookies=jar,headers=headers,timeout=5)
    except:
        print("连接超时")
    print(re.findall("alert.*\)",req.text)[0])
    return

def process(alist):
    n=[]
    m=[]
    for i in range(len(alist)):
        if(int(alist[i][7])<int(alist[i][6])):
            n.append(alist[i])
            n[-1].append(i)
        else:
            m.append(alist[i])
            m[-1].append(i)
    return n,m