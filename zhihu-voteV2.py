# -*- coding: utf-8 -*-

__author__ = 'loveQt'


import json
import os
import time
import re
import requests
import ConfigParser
import sys
import xlwt
from bs4 import BeautifulSoup


Zhihu = 'http://www.zhihu.com/'
Login_url = Zhihu + 'login'
#Vote_url = Zhihu + 'answer/' + ans_id +'/voters_profile?total=99999&offset='+str(num)+'0'
def login():
    cf = ConfigParser.ConfigParser()
    cf.read("config.ini")
    cookies = cf._sections['cookies']

    email = cf.get("info", "email")
    password = cf.get("info", "password")
    cookies = dict(cookies)
    global s
    s = requests.session()
    login_data = {"email": email, "password": password}
    header = {
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
    'Host': "www.zhihu.com",
    'Referer': "http://www.zhihu.com/",
    'X-Requested-With': "XMLHttpRequest"
        }
    r = s.post(Login_url, data=login_data, headers=header)   
login()

def get_voters():
#两种思路
    book = xlwt.Workbook(encoding = 'utf-8',style_compression=0)
    sheet = book.add_sheet('data',cell_overwrite_ok = True)
    login()
    ans_id = raw_input('请输入抓包获得的问题id：')
    Vote_url = Zhihu + 'answer/' + ans_id +'/voters_profile'
    h = s.get(Vote_url)
    html = h.content.encode('utf-8')
    #print html
    target = json.loads(html)
    print '总赞同数：',
    print target['paging']['total']
    #total = target['paging']['total']
    #Vote_url = 'http://www.zhihu.com/'+target['paging']['next']
    num = 0
    while target['paging']['next']:
        try:
            h = s.get(Vote_url)
        except:
            time.sleep(2)
            h = s.get(Vote_url)
        html = h.content.encode('utf-8')
        #print html
        target = json.loads(html)
        Vote_url = 'http://www.zhihu.com'+target['paging']['next']
        
        #print html
        #获取用户名
        i = 10*num
        name = r'a title=\\"(.+?)\\"'
        namelist = re.findall(name,html)
        for each in namelist:
            #print each.decode("unicode-escape")
            sheet.write(i,0,each.decode("unicode-escape"))
            i = i+1        
        #获取用户地址
        i = 10*num
        userurl = r'href=\\"(http://www.zhihu.com/people/.*?)\\'
        userurllist = re.findall(userurl,html)
        #print voteslist
        for each in userurllist:
            #print each
            sheet.write(i,5,each)
            i = i+1
        #获取点赞
        i = 10*num
        votes = r'([_a-zA-Z0-9_]{0,10}) \\u8d5e\\u540c'
        voteslist = re.findall(votes,html)
        #print voteslist
        for each in voteslist:
            #print each
            sheet.write(i,1,each)
            i = i+1
        
        #获取感谢
        i = 10*num
        thank = r'([_a-zA-Z0-9_]{0,10}) \\u611f\\u8c22'
        thanklist = re.findall(thank,html)

        for each in thanklist:
            #print (each)
            sheet.write(i,2,each)
            i = i+1
        #获取提问
        i = 10*num
        ques = r'([_a-zA-Z0-9_]{0,10}) \\u63d0\\u95ee'
        queslist = re.findall(ques,html)
        for each in queslist:
            #print (each)
            sheet.write(i,3,each)
            i = i+1
        #获取回答
        i = 10*num
        ans = r'([_a-zA-Z0-9_]{0,10}) \\u56de\\u7b54'
        anslist = re.findall(ans,html)
        for each in anslist:
            #print (each)
            sheet.write(i,4,each)
            i = i+1
        num = num+1
        
    book.save(r'.\\'+str(ans_id)+'v2result.xls')
    print 'Mission Complete'        

start = time.clock()
get_voters()
end = time.clock()
print end-start
