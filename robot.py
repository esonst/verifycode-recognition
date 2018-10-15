
# coding: utf-8

# In[1]:


import re
from bs4 import BeautifulSoup
import requests
from base import *
import time
import getpass
import ctypes
import sys
import shutil


# In[2]:


print("robots V2.0\n")

# In[3]:


url="http://202.4.152.190:8080/pyxx/login.aspx"
checkurl=r"http://202.4.152.190:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"
signurl="http://202.4.152.190:8080/pyxx/PageTemplate/NsoftPage/yzm/IdentifyingCode.aspx"


# In[5]:


def login(checkurl,url):
    while(True):
        jar=get_cookies_pic(checkurl)
        req,stuid,password,checkcode=login_post(url,jar)
        if req.url=='http://202.4.152.190:8080/pyxx/Default.aspx':
            with open("pass.txt","w") as f:
                f.write(stuid+password)
            print("Log in Successful!")
            return stuid,jar
        else:
            print(re.findall("alert.*\)",req.text)[0])


# In[8]:


stuid,jar=login(checkurl,url)


# In[9]:


def get_info(stuid,jar):
    try:
        ans=requests.get("http://202.4.152.190:8080/pyxx/txhdgl/hdlist.aspx?xh="+stuid,cookies=jar,timeout=5)
    except:
        print("连接超时")
    soup=BeautifulSoup(ans.text,"html.parser")
    target=soup.findAll("table")[-1]
    classnum=len(target.findAll("tr"))-1  # 报告数量
    alist=[[]]*classnum
    for n in range(classnum):
        for info in target.findAll("tr")[n+1].findAll("td")[:11]:
            alist[n]=alist[n]+[info.text]
    return alist
alist=get_info(stuid,jar)


# In[10]:


def choose(n,signurl,stuid,jar):
    while(True):
        signclass(signurl,stuid,jar)
        if not input("继续选课？:(是/否) y/n ")=='y':
            return


# In[11]:

n,m=printf(alist)
print("未满报告：\n")
for i in n:
    print("\n\t")
    print(i[1]+"\t"+i[6]+"\t"+i[7]+"\n")
print("已满报告: ")
for i in m:
    print("\n\t")
    print(i[1]+"\t"+i[6]+"\t"+i[7]+"\n")

while(True):
    n_p=n
    m_p=m
    bar_length=3

    for percent in range(0, 3):
        hashes = '#' * int(percent/3.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))
        if n_p!=n:
            print("未满报告：\n")
            for i in n:
                print("\n\t")
                print(i[1]+"\t"+i[6]+"\t"+i[7]+"\n")
        if m_p!=m:
            print("已满报告: ")
            for i in m:
                print("\n\t")
                print(i[1]+"\t"+i[6]+"\t"+i[7]+"\n")
        sys.stdout.write("runing: %s"%(hashes + spaces))
        sys.stdout.flush()
        time.sleep(3)
        if(len(alist)>0):
            n,m=printf(alist)
            while(len(n)>0):
                choose(len(alist),signurl,stuid,jar,n[0][-1])
                n=n.pop(0)


# In[29]:




