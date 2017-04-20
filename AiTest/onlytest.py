#-*-coding:utf-8-*-
#socket编程示例

 
import time,datetime
from selenium import webdriver
from selenium import selenium
import os
import json

from email.mime.text import MIMEText
import smtplib
from test.test_imageop import AAAAA

 
# wd=webdriver.Ie()
# wd.get("http://mytestlink.vicp.net:8001/redirect1.html")
# wd.execute_script("alert('呵呵')".decode('gbk'))
# wd.execute_script("if('呵呵'==='呵呵'){alert(1)}".decode('gbk'))
# wd.quit()
# print "中文123".decode('gbk')
# wd.find_element_by_css_selector("#cm").click()

#wd.switch_to_alert().accept()
#wd.find_element_by_css_selector("a").click()



# import urllib
# str = '{json_name:PythonTab中文网,json_age:22}'
# #str = str.encode('utf-8')
# d = {'name':str,'age':'"18'}
# print len(d)
# q = urllib.urlencode(d)
# print q
# 
# tmp='[{"field1":"wujt3@asiainfo.com","field2":"","field3":"","text":"吴锦涛/wujt3","type":"","value":"31535033"},{"field1":"wujt3344@asiainfo.com","field2":"","field3":"","text":"wujt3344/wujt3344","type":"","value":"35897406"}]'
# tmp1=eval(tmp)
# print tmp1[0]['text']

# import cx_Oracle
# conn=cx_Oracle.connect("base/Abcd123@10.182.20.42:9403/nctstdb")
# cursor=conn.cursor()
# sql="select user_id,cust_id from so1.ins_user_771 a  where a.bill_id = '13481118910' and a.state='1'"
# cursor.execute(sql)
# r=cursor.fetchall()
# print r
print '2091912938'[-1:]
if 'xxx' not in locals().keys():
    print 'hehe'
print time.strftime("%Y%m")
import traceback
import sys
import logging
logging.basicConfig(level=10,format='%(asctime)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
try:
    print 1+"1"
    #print 1/0
except ZeroDivisionError,e:
    logging.debug('hehe')
    logging.exception(e)
    logging.error('haha')
    #print e
    #traceback.print_exc(file=sys.stdout)
    print 'start next'
except TypeError:
    print 'type error'
print '==='

print map(lambda x: x[10:14], ['AT_SCRIPT_0003.py'])
for i in range(0,1):
    print 'iiii'

import random
print time.strftime("%Y%m%d")
print str(random.randint(100, 200))

print '新增成功！集团号为：7717149428'[-10:]

a='''pass|
err|
pass|
'''
print a.count('\n')

