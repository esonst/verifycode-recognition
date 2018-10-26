
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

"""
base中的全局变量为
    url                 登陆网址
    checkurl            验证码网址
    signurl             验证码网址
    stuid               用户名
    password            密码
"""

def printf(n,m):
    print("未满报告：\n")
    for i in n:
        print("\n\t")
        print(str(i[-1])+"\t"+i[1]+"\t"+i[6]+"\t"+i[7]+"\n")
    print("已满报告: ")
    for i in m:
        print("\n\t")
        print(str(i[-1])+"\t"+i[1]+"\t"+i[6]+"\t"+i[7]+"\n")

### 执行5次 强报告        
def choose(n):
    a=5
    while(a>0):
        signclass(n)
        a-=1

#登陆教务网，拿到cookies
jar=login()

#获取报告列表
alist,viewstate,event=get_info(jar)

#处理列表，找出未满报告
n,m=process(alist)

printf(n,m)

#记录上个状态用于对比刷新
m_p=len(m)

while(True):
	### 以下皆为命令行输出
    bar_length=3
    for percent in range(0, 3):
        hashes = '#' * int(percent/3.0 * bar_length)
        spaces = ' ' * (bar_length - len(hashes))

        if m_p!=len(m):
            print("\n\n\n\n\n\n")
            printf(n,m)

        sys.stdout.write("\rruning: %s"%(hashes + spaces))
        sys.stdout.flush()



        time.sleep(3)

        ## 获取最新列表
        alist,viewstate,event=get_info(jar)
        ## 储存上一个状态
        m_p=len(m)

        if(len(alist)>0):
            n,m=process(alist)

            while(len(n)>0):
                print(str(n[0][-1])+"\t"+n[0][1]+"\t"+n[0][6]+"\t"+n[0][7]+"\n")

                choose(n[0][-1])
                n.pop(0)

