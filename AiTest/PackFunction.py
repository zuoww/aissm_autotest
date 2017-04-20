#-*-coding:utf-8-*-
import time,datetime
from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchFrameException as NoSuchFrameException,\
    NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException as NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException as UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchWindowException as NoSuchWindowException
from selenium.common.exceptions import ElementNotVisibleException as ElementNotVisibleException
from selenium.common.exceptions import TimeoutException as TimeoutException
from OcrMod import getChr,getSplitLenth
#这个包下的代码只允许打印debug日志，自定义的debug，因为selenium模块会打出很多debug日志
from BasicFunction import *
import random
import socket
import logging
import subprocess
from selenium.webdriver.common.action_chains import ActionChains
import codecs

#接口函数使用
import urllib2
import cookielib
import time
import json
import shutil
import linecache
from email.mime.text import MIMEText
import smtplib
from encodings import gbk
#from email.header import Header

#about send mail
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.encoders import encode_base64

#other user
import sqlite3
from DBpool import DBSql
from StepReport import StepReport


WD=None
Cnt=0   #用于自动截图
TmpCnt=0  #兼容ie6，7用，计数，暂时无用
curFrameLoc=[0,0]   #当前frame的坐标，用来计算绝对位置
#记录时间差
sTime=None
eTime=None
cookie=None
EX=None

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='./logs/log',
                filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler();
console.setLevel(logging.INFO);
# set a format which is simpler for console use
formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
# tell the handler to use this format
console.setFormatter(formatter);
logging.getLogger('').addHandler(console);

#************************/改造增加部分/*************************************
#*********************/执行公共参数初始化/*********************
class ExecuteDb(object):
    '''
                执行过程中数据生成与沉淀
    '''
    def __init__(self):
        
        #实例化数据库连接，统一使用
        self.DB=DBSql(CONFIG['mysql_conStr'])
        
        #初始化执行公共参数，统一调用
        self.plan_id=str(CONFIG['plan_id'])
        self.pre_planbatchid=str(CONFIG['pre_planbatchid'])
        self.group_id=str(CONFIG['group_id'])
        if self.pre_planbatchid!='':
            self.plan_id=self.pre_planbatchid.split('_')[0]
        sql0="select project_id,eparchy_code from tbl_plan_def where plan_id='"+self.plan_id+"'"
        ID=self.DB.getSqlList(sql0)
        self.project_id=str(ID[0][0])
        self.eparchy_code=str(ID[0][1])
        self.REGION_ID=str(int(self.eparchy_code))
        self.extend_code='1'
        self.pre_batchId=''
        self.if_group=''
        self.group_name=''
        self.before_node=''
        self.next_node=''
        self.chk_caseidx=''
        self.is_wait='0'
        self.loop_number='1'
        self.nextcase_number=''
        self.exec_machine='0'
        self.exec_index='2'
        self.nextcase_id=''
        self.extend_col=''
        self.log_type='3'
        self.sub_system=''
        self.pre_batchId=''
        self.plan_group=''
        self.exec_module='0'
        self.env='1'
        
     
    #*********************/执行公共参数初始化/*********************
    #执行入库等funs:
    def getCurrentTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def getNextMonth(self):
        nextmonth=str(time.localtime()[1]+1 or 1)
        year=str(time.localtime()[0])
        if nextmonth=='13':
            nextmonth='01'
            year=str(time.localtime()[0]+1)
        if len(nextmonth)==1:
            nextmonth='0'+nextmonth
        NextTime=year+nextmonth
        return NextTime

    def getLastMonth(self):
        lastmonth=str(time.localtime()[1]-1 or 12)
        year=str(time.localtime()[0])
        if lastmonth=='12':
            year=str(time.localtime()[0]-1)
        if len(lastmonth)==1:
            lastmonth='0'+lastmonth
        LastTime=year+lastmonth
        return LastTime
         
    def get_PlanBatchId(self):
        global plan_batch_id
        if self.pre_planbatchid!='':
            plan_batch_id=self.pre_planbatchid
        else:        
            sql="select plan_batch_id from tbl_plan_exec where plan_id='"+self.plan_id+"' and exec_index='1' and status in ('1','2')"
            plan_batch_id=self.DB.getSqlFirst(sql)
            if plan_batch_id=='': 
                self.exec_index='1'             
                plan_batch_id=self.gettemp_PlanBatchId()            
        return plan_batch_id
        
    def gettemp_PlanBatchId(self):
        global templan_batch_id
        plan_begin_time=time.strftime("%Y%m%d%H%M%S")
        templan_batch_id=self.plan_id+'_'+plan_begin_time        
        return templan_batch_id

    def get_BatchId(self,caseid):
        global plan_batch_id
        plan_batch_id=self.get_PlanBatchId()  
        global case_id
        case_id=caseid        
        case_start_time=time.strftime("%Y%m%d%H%M%S")
        global batch_id
        batch_id=plan_batch_id+'_'+case_id+'_'+case_start_time        
        return batch_id

    def plan_Import_Cases(self,casespath,path):  
        if self.group_id=='' and self.pre_planbatchid=='':
            tmpsql="select count(1) from tbl_plan_exec where plan_id='"+self.plan_id+"' and status in ('2')"
            if self.DB.getSqlFirst(tmpsql)!='0':
                logging.info("当前计划".decode('utf-8').encode('gbk')+self.plan_id+"，正在执行中，不允许同时执行".decode('utf-8').encode('gbk'))
                raise SystemExit 
            else:
                sql="select case_id from tbl_plan_case_rel where plan_id='"+self.plan_id+"' and nodefunc_type='CASE' and status='1'"
        else:
            tmpsql="select count(1) from tbl_plan_exec where plan_id='"+self.plan_id+"' and plan_group='"+self.group_id+"' and status in ('2')"
            if self.DB.getSqlFirst(tmpsql)!='0':
                logging.info("当前计划".decode('utf-8').encode('gbk')+self.plan_id+"对应的".decode('utf-8').encode('gbk')+self.group_id+"号组计划，正在执行中，不允许同时执行".decode('utf-8').encode('gbk'))
                raise SystemExit
            elif self.pre_planbatchid=='':
                sql="select case_id from tbl_plan_case_rel where plan_id='"+self.plan_id+"' and group_id='"+self.group_id+"' and nodefunc_type='CASE' and status='1'"
            elif self.group_id=='':
                sql="select node_id from tbl_auto_dataresult where plan_batch_id='"+self.pre_planbatchid+"' and status!='1' and node_type='CASE'"
            elif ('-5' in self.group_id) & (len(self.group_id)>2):
                sql="select node_id from tbl_auto_dataresult where plan_batch_id='"+self.pre_planbatchid+"' and extend_col='"+self.group_id[0:-2]+"' and status='5' and node_type='CASE'"
            else:
                sql="select node_id from tbl_auto_dataresult where plan_batch_id='"+self.pre_planbatchid+"' and extend_col='"+self.group_id+"' and status!='1' and node_type='CASE'" 
                #tempsql="update tbl_plan_exec set status=1 where plan_batch_id='"+self.pre_planbatchid+"' and plan_group='"+self.group_id+"'"
                #self.Db.dbwSql(tempsql)
        tmpsql="select C.script_name from tbl_fk_case_script_rel A, tbl_fk_scripts C where A.case_id in ("+sql+") and A.script_id=C.script_id"
        case_id=self.DB.getSqlList(tmpsql)
        print case_id
        #i=0
        for caseid in case_id: 
            caseid=str(caseid[0])
            #i=str(int(i)+1)
            i=str(int(caseid[-7:-3]))#取caseid的尾数编码
            startCase=str('startCase('+i+')\n')
            endCase='\nendCase('+i+',Dict,1)\n'
            #caseid='AT_SCRIPT_'+caseid+'.py'
            print caseid
            try:
                tag=True
                fp=file(casespath+caseid)    
                lines=[]
                for line in fp:
                    lines.append(line)
                fp.close()
                lines.insert(0,'#-*-coding:utf-8-*-\n')
                lines.insert(1,startCase)
                lines.insert(len(lines),endCase)
                s=''.join(lines)
                fp=file(path+caseid,'w')
                fp.write(s)
                fp.close()
            except Exception,e:
                tag=False
                tmpPathErr=str(e)
                if type(tmpPathErr)!=gbk and type(tmpPathErr)!=unicode:
                    tmpPathErr.decode('utf-8')
                logging.exception(tmpPathErr)
                continue
            finally:
                if tag==True and self.pre_planbatchid=='':
                    self.insert_DataResultAll(i)
                pass   
             
    def insert_WebLogs(self,List):
        sql=[]
        i=len(List)
        for j in range (i):
            begin_time=List[j][0]        
            step_desc=List[j][1]      
            input_desc=List[j][2]
            end_time=List[j][3]
            #exec_time=List[j][4] /*执行时间，需要用到的时候，反注释*/
            exec_result=List[j][5]
            step_index=str(j+1)
            tempsql="insert into tbl_fk_weblogs values('"+plan_batch_id+"','"+batch_id+"','"+case_id+"','"+step_index+"','"+step_desc+"','"+input_desc+"','"+begin_time+"','"+end_time+"','"+exec_result+"','"+self.log_type+"','"+self.project_id+"','"+self.eparchy_code+"','"+self.extend_col+"')"
            sql.append(tempsql)
        tmpsql="delete from tbl_fk_weblogs where batch_id like '"+batch_id[:-13]+"%'"#and LENGTH(batch_id)=LENGTH('"+batch_id+"')
        self.DB.dbwSql(tmpsql)
        self.DB.dbwSql(sql)
        
    def insert_DataResultAll(self,case_id): 
        global plan_batch_id
        global begin_time
        batch_id=self.get_BatchId(case_id)
        begin_time=self.getCurrentTime()       
        end_time=begin_time    
        node_id=case_id
        extend_col=self.group_id
        status='-1'#\*默认初始化为未执行状态*\
        sql=[]
        tmpSql="select node_seq,nodefunc_type from tbl_plan_case_rel where plan_id='"+self.plan_id+"' and case_id='"+case_id+"'"
        node=self.DB.getSqlList(tmpSql)
        for nodeid in node:
            node_seq=str(nodeid[0])
            node_type=str(nodeid[1])
            rel_node_seq=node_seq
            tempsql="insert into tbl_auto_dataresult(plan_batch_id,batch_id,exec_machine,node_id,node_type,node_seq,rel_node_seq,status,extend_col,begin_time,end_time,project_id,eparchy_code,sub_system,nextcase_id,exec_index,plan_id,loop_number,nextcase_number,is_wait,chk_caseidx)values('"+plan_batch_id+"','"+batch_id+"','"+self.exec_machine+"','"+node_id+"','"+node_type+"','"+node_seq+"','"+rel_node_seq+"','"+status+"','"+extend_col+"','"+begin_time+"','"+end_time+"','"+self.project_id+"','"+self.eparchy_code+"','"+self.sub_system+"','"+self.nextcase_id+"','"+self.exec_index+"','"+self.plan_id+"','"+self.loop_number+"','"+self.nextcase_number+"','"+self.is_wait+"','"+self.chk_caseidx+"')"
            sql.append(tempsql)
        #tmpsql="delete from tbl_auto_dataresult where plan_batch_id='"+plan_batch_id+"' and status not in (1,3)
        #self.DB.dbwSql(tmpsql)
        self.DB.dbwSql(sql)
        
    def insert_DataResult(self): 
        global plan_batch_id,batch_id
        global begin_time,case_id
        begin_time=self.getCurrentTime()       
        end_time=begin_time    
        node_id=case_id
        extend_col=self.group_id
        status='-1'#\*默认初始化为未执行状态*\
        sql=[]
        tmpSql="select node_seq,nodefunc_type from tbl_plan_case_rel where plan_id='"+self.plan_id+"' and case_id='"+case_id+"'"
        node=self.DB.getSqlList(tmpSql)
        for nodeid in node:
            node_seq=str(nodeid[0])
            node_type=str(nodeid[1])
            rel_node_seq=node_seq
            tempsql="insert into tbl_auto_dataresult(plan_batch_id,batch_id,exec_machine,node_id,node_type,node_seq,rel_node_seq,status,extend_col,begin_time,end_time,project_id,eparchy_code,sub_system,nextcase_id,exec_index,plan_id,loop_number,nextcase_number,is_wait,chk_caseidx)values('"+plan_batch_id+"','"+batch_id+"','"+self.exec_machine+"','"+node_id+"','"+node_type+"','"+node_seq+"','"+rel_node_seq+"','"+status+"','"+extend_col+"','"+begin_time+"','"+end_time+"','"+self.project_id+"','"+self.eparchy_code+"','"+self.sub_system+"','"+self.nextcase_id+"','"+self.exec_index+"','"+self.plan_id+"','"+self.loop_number+"','"+self.nextcase_number+"','"+self.is_wait+"','"+self.chk_caseidx+"')"
            sql.append(tempsql)
        tmpsql="delete from tbl_auto_dataresult where batch_id like '"+batch_id[:-14]+"%'"
        self.DB.dbwSql(tmpsql)
        self.DB.dbwSql(sql)

    #执行状态-1：未执行，0：失败，1：成功，2：正在执行，3：准备执行，4：前台成功，但是不需要数据验证
    #stream_attr是否为异常流不需要后台校验
    def update_DataResult(self,flag=True):
        global plan_batch_id,batch_id,case_id    
        end_time=self.getCurrentTime()
        if flag==False:
            status='2'
            sql="update tbl_auto_dataresult set batch_id='"+batch_id+"',status='"+status+"',begin_time='"+end_time+"' where plan_batch_id='"+plan_batch_id+"' and node_id='"+case_id+"' and node_type='CASE'"
        else:
            CaseStatus=CONFIG["CaseStatus"]
            sql="select stream_attr from tbl_case_def where case_id='"+case_id+"'"
            global stream_attr
            stream_attr=self.DB.getSqlFirst(sql)
            print stream_attr
            if CaseStatus=='pass' and stream_attr=='2':
                status='4'
            elif CaseStatus=='pass' :
                status='1'
                verf_status='3'
                tmpsql="update tbl_auto_dataresult set batch_id='"+batch_id+"',status='"+verf_status+"',end_time='"+end_time+"' where plan_batch_id='"+plan_batch_id+"' and node_id='"+case_id+"' and node_type='VERIFY'"
                self.DB.dbwSql(tmpsql)
            else:
                status='0'
            sql="update tbl_auto_dataresult set batch_id='"+batch_id+"',status='"+status+"',end_time='"+end_time+"' where plan_batch_id='"+plan_batch_id+"' and node_id='"+case_id+"' and node_type='CASE'"       
        self.DB.dbwSql(sql)

    def insert_DataInterface(self,Dict):  
        global case_id,batch_id,begin_time
        begin_time=self.getCurrentTime()
        tmpsql="select group_id from tbl_bk_case_group_step_rel where case_id='"+case_id+"' and eparchy_code='"+self.eparchy_code+"'"
        group_id=self.DB.getSqlFirst(tmpsql)
        case_exec_time=begin_time
        sql=[]
        for keyword_name,keyword_value in Dict.items():
            tmpsql="insert into tbl_auto_datainterface values('"+batch_id+"','"+case_id+"','"+group_id+"','"+str(keyword_name)+"','"+str(keyword_value)+"','"+self.group_id+"','"+case_exec_time+"','"+self.project_id+"','"+self.eparchy_code+"')"
            sql.append(tmpsql)
        self.DB.dbwSql(sql)
        Dict={}

    #1：准备执行，2：执行中，3：执行成功，4：执行失败
    def insert_Plan_Exec(self):
        global templan_batch_id
        sql="select exec_id from tbl_plan_exec order by exec_id desc LIMIT 1"
        bf_exec_id=self.DB.getSqlFirst(sql)
        exec_id=str(int(bf_exec_id)+1)
        begin_time=self.getCurrentTime()
        end_time=begin_time
        status='1'
        sql="insert into tbl_plan_exec(exec_id,plan_id,exec_index,exec_machine,pre_batchId,plan_group,exec_module,env,plan_batch_id,begin_time,end_time,status,project_id,eparchy_code,extend_code,sub_system)values('"+exec_id+"','"+self.plan_id+"','"+self.exec_index+"','"+self.exec_machine+"','"+self.pre_batchId+"','"+self.group_id+"','"+self.exec_module+"','"+self.env+"','"+templan_batch_id+"','"+begin_time+"','"+end_time+"','"+status+"','"+self.project_id+"','"+self.eparchy_code+"','"+self.extend_code+"','"+self.sub_system+"')"            
        self.DB.dbwSql(sql)

        
    def update_Plan_Exec(self,status=2):
        global templan_batch_id
        end_time=self.getCurrentTime()
        sql="update tbl_plan_exec set status='"+str(status)+"',end_time='"+end_time+"' where plan_batch_id='"+templan_batch_id+"'"
        self.DB.dbwSql(sql)
#实例化

#************************/改造增加部分/*************************************


#日志装饰器---------------------------------------------------------
def log(inFunc):
    global WD
    def wrapper(*args,**kw):
        global WD
        #内部函数不打印函数开始和结束信息
        rr=""
        for i in args:
            if type(i)==str:
                rr=rr+",\""+i+"\""
            else:
                rr=rr+","+str(i)
        rr="function < "+inFunc.__name__+"("+rr[1:]+") > start"
        rr=rr.decode('utf-8').encode('gbk')
        logging.info(rr)
        #获取参数需要区分执行模式
        tmp=inFunc(*args,**kw)
        rr=""
        for i in args:
            if type(i)==str:
                rr=rr+",\""+i+"\""
            else:
                rr=rr+","+str(i)
        rr="function < "+inFunc.__name__+"("+rr[1:]+") > end"
        rr=rr.decode('utf-8').encode('gbk')
        logging.info(rr)
        return tmp
    return wrapper
#日志装饰器---------------------------------------------------------------


#测试函数
@log
def noCall():
    return 'return noCall'
    

def startCase(LineNum):
    global Cnt,sTime
    global Dict
    Dict={}    
    sTime=datetime.datetime.now()
    Cnt=1
    if CONFIG["executeMode"]==1:
        CONFIG["CaseNumber"]=LineNum[0]
    else:
        CONFIG["CaseNumber"]=LineNum
    CONFIG["CaseStatus"]="empty"
    CONFIG["output"]=""
    logging.info("case "+str(LineNum)+" begin:")
    #******************/更新用例执行状态/*********************
    global EX

    EX.update_DataResult(False)
    #******************/更新用例执行状态/*********************


def endCase(LineNum,Dict={},CallInter=0):
    global WD,sTime,eTime,EX
    global stream_attr
    if CallInter==0:
        return
    '''
        备注：
        更改前：
        eTime=datetime.datetime.now()
        tTime=str(eTime-sTime).split('.')[0]
        更改后：
        if Dict=={}:
            tTime='0:00:00'
        else:
            eTime=datetime.datetime.now()
            tTime=str(eTime-sTime).split('.')[0]
    '''
    if Dict=={}:
        tTime='0:00:00'
        if 'output' not in CONFIG.keys():
            CONFIG["output"]="case "+str(LineNum)+"对应数据池为空"
    else:
        eTime=datetime.datetime.now()
        tTime=str(eTime-sTime).split('.')[0]
    if CONFIG["executeMode"]==1:
        CONFIG["CaseNumber"]=LineNum[0]
    else:
        CONFIG["CaseNumber"]=LineNum
    #单条用例测试结束后，写入执行情况
    tmpPath=CONFIG['path']+'\\result.txt'
    with open(tmpPath,'a') as f1:
        f1.write(CONFIG["CaseStatus"]+"|"+tTime+"|"+CONFIG["output"] + '\n')
    #如果配置fail后退出，则退出
    if CONFIG['stopOnCheckFail']=='y' and CONFIG["CaseStatus"]=="fail":
        if CONFIG['quitBrowser']=='y':
            WD.quit()
            #***************更新计划执行状态\失败***************
            ExecuteDb().update_Plan_Exec(4)
            #***************更新计划执行状态\失败***************
            raise SystemExit
        else:
            os.system("taskkill -f /im IEDriverServer.exe")
        tmpPath=CONFIG['path'] + '\\result.txt'
        with codecs.open(tmpPath,'rb','utf-8') as f1:
            tmpText=f1.read()
        with codecs.open(tmpPath,'wb','gbk') as f2:
            f2.write(tmpText)
        #raise SystemExit
    if CONFIG["CaseStatus"]=="empty":
        CONFIG["CaseStatus"]="pass"
    #******************/更新用例执行状态/***************
    EX.update_DataResult()
    #******************/数据沉淀/*********************
    List=StepReport().getStepList()
    if List==[] and Dict!={}:
        logging.info("case "+str(LineNum)+"传入的步骤记录为空，请检查List出现的异常（内存丢失）".decode('utf-8').encode('gbk'))
    elif List!=[]:
        EX.insert_WebLogs(List)
        StepReport().AI_ClearStepList()
    if Dict!={}:
        Dict['REGION_ID']=EX.REGION_ID
        Dict['MONTH']=time.strftime('%Y%m')
        Dict['LAST_MONTH']=EX.getLastMonth()
        Dict['NEXT_MONTH']=EX.getNextMonth()
        EX.insert_DataInterface(Dict)
    elif CONFIG["CaseStatus"]=="pass" and stream_attr=='-1':
        logging.info("case "+str(LineNum)+"属性为异常流，无需后台校验".decode('utf-8').encode('gbk'))
    elif CONFIG["CaseStatus"]=="pass":
        logging.info("case "+str(LineNum)+"前台执行成功却未插入后台数据，请检查用例是否需要后台验证".decode('utf-8').encode('gbk'))     
    #******************/数据沉淀/*********************
    logging.info("case "+str(LineNum)+" finish,status="+CONFIG["CaseStatus"])

@log
def exeJs_v(inScript,inV=[],fpath=""):
    global WD
    tmpJs='''
    if (!document.querySelectorAll2) {
        document.querySelectorAll2 = function (selectors) {
            var style = document.createElement('style'), elements = [], element;
            document.documentElement.firstChild.appendChild(style);
            document._qsa = [];
            style.styleSheet.cssText = selectors + '{x-qsa:expression(document._qsa && document._qsa.push(this))}';
            window.scrollBy(0, 0);
            style.parentNode.removeChild(style);
            while (document._qsa.length) {
                element = document._qsa.shift();
                element.style.removeAttribute('x-qsa');
                elements.push(element);
            }
            document._qsa = null;
            return elements;
        }
    }'''
    if fpath!="":
        #自动切入相应的frame
        _autoSwitchFramesByJs(fpath)
    #判断是否加载jq库
    if CONFIG['addjQuery']=="y":
        r=WD.execute_script("if (typeof(jQuery)=='function') {return true} else {return false}")
        if not r:
            tmpJs="var js = document.createElement('script');\n"
            tmpJs=tmpJs+"js.setAttribute('src', 'http://127.0.0.1:1414/jquery.min.js');\n"
            tmpJs=tmpJs+"js.setAttribute('type', 'text/javascript');\n"
            tmpJs=tmpJs+"document.getElementsByTagName('head')[0].appendChild(js);\n"
            WD.execute_script(tmpJs)
            i=1
            while not r:
                time.sleep(1)
                r=WD.execute_script("if (typeof(jQuery)=='function') {return true} else {return false}")
                logging.log(15,"waiting for jQuery loaded,"+str(i))
                i=i+1
                if i>10:
                    logging.warn("jQuery cannot add to webpage!")
                    break
#     if "document.querySelectorAll" in inScript:
#         inV.append(WD.execute_script(tmpJs))
    try:
        r=WD.execute_script(inScript)
    except TimeoutException,e:
        logging.exception(e)
    inV.append(r)
    return r


@log
def exeSql(inputParam,oVal={}):
    #首次执行获取sqlplus路径
    
    if CONFIG["executeMode"]==1:
        print 'not support!'
        return
    tmpPath=CONFIG['path']+'\\temp\\tmp.sql'
    preStr='''set echo off
set linesize 500
set pagesize 100
set numwidth 14
set trimout on
set trimspool on
set colsep |
set newpage none
set heading on
set feedback off
set verify off'''
    with open(tmpPath,'w') as f1:
        f1.write(preStr+'\n')
    with open(tmpPath,'a') as f2:
        f2.write(inputParam+'\n'+'quit;')
    cmd="sqlplus -S "+CONFIG['ConStr']+" @"+tmpPath
    r=os.popen(cmd)
    lines=r.readlines()
    #return ''.join(lines)
    #print type(lines)
    if lines==[]:
        #没有查出结果，无论有无入参都不返回
        logging.log(15,"query with no result")
        return {}
    elif lines[0][0:5]=='ERROR':
        raise Exception(''.join(lines))
    else:
        #有输出但是不用返回，输出个日志信息
        if type(oVal)!=dict:
            logging.warn("exeSql's input param must be dict,now return {}")
            return {}
        ColName=lines[0].strip().split('|')
        ColData=[]
        for i in lines[2:]:
            #print i.strip().split('|')
            ColData.append(i.strip().split('|'))
        ColData=zip(*ColData)
        #print ColData
        for i in range(0,len(ColName)):
            oVal[ColName[i].strip().lower()]=list(ColData[i])
        return oVal


@log
def getPic(*inputParam):
    global WD,Cnt
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    if len(innerParam)>0:
        savPath=CONFIG['path'] + '\\pic\\' + innerParam[0] + '.png'
    else:
        pname=(3-len(str(Cnt)))*'0'+str(Cnt)
        pname=(3-len(str(CONFIG['CaseNumber'])))*'0'+str(CONFIG['CaseNumber'])+pname
        savPath=CONFIG['path'] + '\\pic\\' + pname + '.png'
    WD.save_screenshot(savPath)
    Cnt+=1


@log
def openUrl(url,timeout=-1):
    global WD,EX
    EX=ExecuteDb()
    WD=webdriver.Ie(executable_path=CONFIG['path']+'\\IEDriverServer.exe')
    if CONFIG["executeMode"]==1:
        raise Exception('not suppurt!')
    else:
        try:
            if timeout>0:
                WD.set_page_load_timeout(timeout)
                WD.set_script_timeout(timeout)
            WD.get(url)
            WD.delete_all_cookies()
            WD.refresh()
        except:
            logging.exception("page loading over "+str(timeout))
    #time.sleep(1)
    #WD.switch_to_winddow(WD.window_handles[0])


@log
def resetUrl(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        WD.get(inputParam[0][0])
    else:
        WD.get(inputParam[0])


@log
def refresh():
    global WD
    try:
        WD.refresh()
    except TimeoutException,e:
        logging.exception(e)

@log
def closeUrl():
    global WD
    #WD.execute_script("alert('测试结束，浏览器将在3秒后关闭')")
    time.sleep(1)
    WD.execute_script("window.opener=null;window.open('','_self');window.close();")
    #time.sleep(1)
    try:
        WD.switch_to_alert().accept()
    except Exception,e:
        if type(e)==NoSuchWindowException or type(e)==NoAlertPresentException:
            pass
    WD.quit()
    

@log
def clickElement_v(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    _waitElement(innerParam[0])
    try:
        if innerParam[0][0]=="/":
            logging.log(15,"element disabled status is "+str(WD.find_element_by_xpath(innerParam[0]).get_attribute("disabled")))
            WD.find_element_by_xpath(innerParam[0]).click()
        else:
            logging.log(15,"element disabled status is "+str(WD.find_element_by_css_selector(innerParam[0]).get_attribute("disabled")))
            WD.find_element_by_css_selector(innerParam[0]).click()
        return True
    except UnexpectedAlertPresentException:
        WD.switch_to_alert().accept()
        logging.log(15,'这里要重新考虑下元素事件里面会弹出小窗的情况')
    except TimeoutException:
        logging.log(15,"page load timeout,try click again")
        return True

#这个基本不需要了
#0-元素id或xpath,1-属性名称,2-期望值
@log
def checkValue(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    _waitElement(innerParam[0])
    #这里要支持id，xpath查找，并支持所有属性和innerHTML文本比对
    if innerParam[0][0]=="/":
        if innerParam[1]=="html":
            tmp=WD.find_element_by_xpath(innerParam[0]).text
            #print tmp
        else:
            tmp=WD.find_element_by_xpath(innerParam[0]).get_attribute(innerParam[1])
    else:
        if innerParam[1]=="html":
            tmp=WD.find_element_by_css_selector(innerParam[0]).text
        else:
            tmp=WD.find_element_by_css_selector(innerParam[0]).get_attribute(innerParam[1])
    if tmp!=innerParam[2]:
        CONFIG["CaseStatus"]="fail"


@log 
def closeWindow(*inputParam):
    #关闭当前窗口，要关闭指定窗口，用到后期再增加
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    if len(innerParam)==0:
        try:
            WD.close()
        except:
            logging.info('no driver or driver with no window')
    else:
        tmpStr=innerParam[0].decode('utf-8')
        for j in WD.window_handles:
            WD.switch_to_window(j)
            if WD.title==tmpStr:
                WD.close()

@log
def inputText_v(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    _waitElement(innerParam[0])
    try:
        if len(innerParam)==1:
            #通过输入框手工获取值，这里以后要考虑下如果是textarea的情况，不能使用value输入
            WD.execute_script("document.getElementById('"+innerParam[0]+"').value=prompt('input a value')")
        else:
            #print innerParam[1].decode('utf-8')
            if innerParam[0][0]=="/":
                WD.find_element_by_xpath(innerParam[0]).send_keys(innerParam[1].decode('utf-8'))
            else:
                WD.find_element_by_css_selector(innerParam[0]).send_keys(innerParam[1].decode('utf-8'))
        return True
    except NoSuchElementException,e:
        logging.exception(e)
        return False
    except TimeoutException:
        logging.log(15,"page load timeout,try input again")
        return True
    
#等待一个元素加载完成，不建议使用
@log
def waitElement(*inputParam):
    global WD
    tmps=CONFIG['TimeOut']
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    while tmps>0:
        try:
            if innerParam[0][0]=="/":
                if WD.find_element_by_xpath(innerParam[0]):
                    return True
            else:
                if WD.find_element_by_css_selector(innerParam[0]):
                    return True
        except Exception,e:
            time.sleep(1)
            tmps=tmps-1
    tmpstr='wait over time for '+str(CONFIG['TimeOut'])+'s'+': \n'+str(e)
    raise NoSuchElementException(tmpstr)


#等待一个元素加载，内部调用，不考虑编码转换
def _waitElement(inputParam,tag=False):
    global WD
    tmps=CONFIG['TimeOut']
    while tmps>0:
        try:
            if inputParam[0]=="/":
                e=WD.find_element_by_xpath(inputParam)
                if e.is_enabled() and (e.is_displayed() or tag==True):
                    return
                else:
                    time.sleep(1)
                    tmps=tmps-1
            else:
                e=WD.find_element_by_css_selector(inputParam)
                if e.is_enabled() and (e.is_displayed() or tag==True):
                    return
                else:
                    time.sleep(1)
                    tmps=tmps-1
        except Exception,e:
            if type(e)!=NoSuchElementException and type(e)!=NoSuchFrameException:
                logging.exception(e)
                break
            time.sleep(1)
            tmps=tmps-1
    tmpstr='wait over time for '+str(CONFIG['TimeOut'])+'s'+':\n'+str(e)
    raise NoSuchElementException(tmpstr)


@log
def setConfig_v(ParamName,inputStr):
    if ParamName=="CaseStatus":
        if inputStr=="fail":
            CONFIG["CaseStatus"]="fail"
        if inputStr=="break":
            CONFIG["CaseStatus"]="fail"
            CONFIG["output"]="-break"+CONFIG["output"]
            logging.warn("CaseStatus is break,exit!")
            endCase(CONFIG["CaseNumber"],1)
            closeUrl()
            raise SystemExit
    if ParamName=="ConStr":
        CONFIG["ConStr"]=inputStr


@log
def switchAlert(Chs=""):
    global WD
    if CONFIG["executeMode"]==1:
        print 'not support!'
        raise SystemExit
    i=0
    while i<CONFIG['TimeOut']:
        try:
            if Chs=="":
                WD.switch_to_alert().accept()
            elif Chs=="dismiss":
                WD.switch_to_alert().dismiss()
            return
        except NoAlertPresentException:
            #i=i+1
            return
        except UnexpectedAlertPresentException:
            return
        except NoSuchWindowException:
            WD.switch_to_window(WD.window_handles[0])
            i=i+1
           

#尝试切换一个frame直到超时，30s
@log
def switchFrame(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    if len(innerParam)==0:
        logging.log(15,"准备切入default_content".decode('utf-8').encode('gbk'))
        WD.switch_to_default_content()
    else:
        _waitElement(innerParam[0],True)
        if innerParam[0][0]=="/":
            logging.log(15,"准备切入frame by xpath:".decode('utf-8').encode('gbk')+innerParam[0])
            WD.switch_to_frame(WD.find_element_by_xpath(innerParam[0]))
        else:
            logging.log(15,"准备切入frame by css selector:".decode('utf-8').encode('gbk')+innerParam[0])
            WD.switch_to_frame(WD.find_element_by_css_selector(innerParam[0]))


@log
def switchWindow(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    i=0
    while i<CONFIG['TimeOut']:
        try:
            if len(innerParam)==0:
                WD.switch_to_window(WD.window_handles[0])
                return True
            else:
                print len(WD.window_handles)
                tmpStr=innerParam[0].decode('utf-8')
                for j in WD.window_handles:
                    WD.switch_to_window(j)
                    print WD.execute_script("return document.title")
                    if WD.title==tmpStr:
                        return True
                return False
        except Exception,e:
            if e==UnexpectedAlertPresentException:
                logging.log(15,"Alert window exist,close and wait 1 seconds")
            if e==NoSuchWindowException:
                logging.log(15,"window not found,wait 1 seconds")
            i=i+1
            time.sleep(1)
    return False


@log 
def selectList(*inputParam):
    #改造使用js操作选择select，selenium原生方法太慢 
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    _waitElement(innerParam[0])
    logging.log(15,"select value is able to be operated")
    if innerParam[0][0]=="/":
        childPath=innerParam[0]+"/option[@value='"+innerParam[1]+"']"
        logging.log(15,("find value ok,real path is "+childPath))
        WD.find_element_by_xpath(childPath).click()
    else:
        childPath=innerParam[0]+" > option[value*='"+innerParam[1]+"']"
        logging.log(15,("find value ok,real path is "+childPath))
        WD.find_element_by_css_selector(childPath).click()
    

@log 
def getConfig(keyStr):
    tmp=''
    if keyStr in CONFIG.keys():
        tmp=CONFIG[keyStr]
    return tmp


@log 
def getTitles(oVal=[]):
    global WD
    if CONFIG["executeMode"]==1:
        print 'not support!'
        raise SystemExit
    try:
        tmpT=WD.title
        print tmpT
        tmpH=WD.current_window_handle
        if len(WD.window_handles)==1:
            oVal.append(tmpT)
            return tmpT
        for j in WD.window_handles:
            WD.switch_to_window(j)
            oVal.append(WD.title.encode('utf-8'))
        WD.switch_to_window(tmpH)
    except Exception,e:
        logging.info('no driver or driver with no window')
        
@log
def getValue_v(Loc,Attr,InV=[]):
    global WD
    _waitElement(Loc)
    tmp=''
    if Loc[0]=="/":
        if Attr=="html":
            tmp=WD.find_element_by_xpath(Loc).text
            if type(tmp)==unicode:
                tmp=tmp.encode('utf-8')
            InV.append(tmp)
        else:
            tmp=WD.find_element_by_xpath(Loc).get_attribute(Attr)
            if type(tmp)==unicode:
                tmp=tmp.encode('utf-8')
            InV.append(tmp)
    else:
        if Attr=="html":
            tmp=WD.find_element_by_css_selector(Loc).text
            if type(tmp)==unicode:
                tmp=tmp.encode('utf-8')
            InV.append(tmp)
        else:
            tmp=WD.find_element_by_css_selector(Loc).get_attribute(Attr)
            if type(tmp)==unicode:
                tmp=tmp.encode('utf-8')
            InV.append(tmp)
    return tmp.strip()


@log
def getAlertText(oVal=[]):
    global WD
    if CONFIG["executeMode"]==1:
        print 'not support!'
        raise SystemExit
    i=0
    while i<CONFIG['TimeOut']:
        try:
            tmpStr=WD.switch_to_alert().text.encode('utf-8')
            oVal.append(tmpStr.strip())
            return tmpStr.strip()
        except NoAlertPresentException:
            return ''
        except UnexpectedAlertPresentException:
            return ''
        except NoSuchWindowException:
            WD.switch_to_window(WD.window_handles[0])
            i=i+1


@log
def inputAuthCode(img='',input='',ex=0,ey=0,ew=0,eh=0):
    global WD
    innerParam=[img,input]
    _waitElement(innerParam[0])
    #获取整个页面的截图
    savPath=CONFIG['path'] + '\\ocr'
    if os.path.isfile(savPath+'\\tmp_page.png'):
        os.system('del '+savPath+'\\*.png')
    WD.save_screenshot(savPath+'\\tmp_page.png')
    #通过传入的xywh坐标和宽长，使用nconvert抠出验证码图片并存为result.png
    if innerParam[0][0]=="/":
        e=WD.find_element_by_xpath(innerParam[0])
    else:
        e=WD.find_element_by_css_selector(innerParam[0])
    tmpCmd=savPath+"\\nconvert -quiet -o "+savPath+"\\result.png -crop "
    tmpCmd=tmpCmd+str(e.location.get('x')+ex)+' '+str(e.location.get('y')+ey)+' '+str(e.size.get('width')+ew)+' '+str(e.size.get('height')+eh)
    tmpCmd=tmpCmd+' '+savPath+"\\tmp_page.png"
    #print tmpCmd
    os.system(tmpCmd)
    
    #返回的string写入web元素内
    authCode=getChr(savPath).strip()
    if innerParam[0][0]=="/":
        WD.find_element_by_xpath(innerParam[1]).clear()
        WD.find_element_by_xpath(innerParam[1]).send_keys(authCode)
    else:
        WD.find_element_by_css_selector(innerParam[1]).clear()
        WD.find_element_by_css_selector(innerParam[1]).send_keys(authCode)
    if getSplitLenth()>0:
        logging.warn("the split length of bitmap file is <"+str(getSplitLenth())+">,check OcrMod if not correct")
        logging.log(15,"the auth code is:"+authCode)


def retFunc(rList='noCall'):
    #print sys._getframe().f_code.co_name
    f1=eval(rList)
    return f1


def endVideo():
    if CONFIG['capScreen']=="y":
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("127.0.0.1",1415))
            s.send("end")
            buf=[]
            d=s.recv(1024)
            buf.append(d)
            if ''.join(buf).strip()=="stoped":
                logging.info("Screen captured success,check file at video\\temp.cap")
            else:
                logging.warn("录制屏幕进程有异常，请检查!")
            #print ''.join(buf)
        except Exception,e:
            #logging.error(e)
            logging.error("no capture run")
        finally:
            s.close()


def setOutput(inputParam):
    #logging.log(15,inputParam.decode('utf-8'))
    if type(inputParam)==gbk:
        inputParam=inputParam.decode('gbk')
    if type(inputParam)==unicode:
        inputParam=inputParam.encode('utf-8')
    inputParam=inputParam.replace('\n','|')
    if CONFIG['output']=="":
        CONFIG['output']=inputParam
    else:
        CONFIG['output']=CONFIG['output']+"|"+inputParam



#新函数-----------------------------------------------------------------------
#_autoSwitchFrames函数比Js版本的慢，作废不用
def _autoSwitchFrames(inPath):
    #inPath must be css path
    global WD,ar
    tmpLen=len(WD.find_elements_by_css_selector(inPath))
    if tmpLen>=1:
        #true代表找到元素
        ar=True
        return
    tmpLen=len(WD.find_elements_by_css_selector('frame,iframe'))
    if tmpLen==0:
        return
    tmpFrame=range(0,tmpLen)
    #print tmpFrame
    for i in tmpFrame:
        try:
            print WD.find_elements_by_tag_name("iframe")[i].get_attribute("id")
            WD.switch_to_frame(i)
        except:
            print 'aa'
        CONFIG['curFrames'].append(i)
        _autoSwitchFrames(inPath)
        if ar:
            return
        WD.switch_to_default_content()
        CONFIG['curFrames'].pop()
        for j in CONFIG['curFrames']:
            WD.switch_to_frame(j)
        ar=False


def _autoSwitchFramesByJs(inPath,keystr=''):
    global WD,TmpCnt
    #为ie7以下浏览器添加tag
#     if TmpCnt==0:
#         #ie7以下添加xqsa属性
#         tmpJs='''
#  
#         '''
#         tmpJs=tmpJs.replace('XXXX',inPath)
#         WD.execute_script(tmpJs)
    tmpJs='''
function getFrames() {
  var getFlag=false;
  var arr=[];
  var arrid=[];
  var curWindow=window;
  var bver=0;
  var ts="function addQueryForCss(){if(!document.querySelectorAll){"
  ts=ts+"document.querySelectorAll = function (selectors){var telements=[];var elements=[];"
  ts=ts+"telements=document.body.getElementsByTagName('*');for (var i=0;i<telements.length;i++)"
  ts=ts+"{if (telements[i].xqsa=='0'){telements[i].removeAttribute('xqsa');elements.push(telements[i]);}}return elements;}}}"
  findElements=function (csspath,wd,keystr) {
    if (wd.document.readyState!='complete'){
        return;
    }
    if (bver==6 && !wd.document.getElementById('seleniumaddquery')){
          var jss = wd.document.createElement('script');
          jss.setAttribute('id', 'seleniumaddquery');
          jss.setAttribute('type', 'text/javascript');
          wd.document.getElementsByTagName('head')[0].appendChild(jss);
          wd.document.getElementById('seleniumaddquery').text=ts;
          wd.addQueryForCss();
      }
    var ecnt=wd.document.querySelectorAll(csspath);
    if (ecnt.length>0) {
        if(keystr==undefined || keystr==''){
          getFlag=true;
          return;
      }else{
          for(var i=0;i<ecnt.length;i++){
              if (ecnt[i].innerText==keystr){
                  getFlag=true;
                  return;
              }
          }
      }
    }
    if (wd.frames.length>0) {
        var j="";
        for (var i=0;i<wd.frames.length;i++) {
          //find frames down
          arr.push(i);
          j=wd.document.getElementsByTagName('iframe')[i].getAttribute('id');
          if (j==null) { j=i; }
          arrid.push(j);
          //alert("j:"+j);
          findElements(csspath,wd.frames[i]);
          //alert('return from find'+j);
          if (getFlag) {
              return;
          } else { arr.pop(); arrid.pop();}
        }
    } else { return; }
  }
    if (curWindow.frames.length>0) {
        if (navigator.appVersion.indexOf('MSIE 6.0')>0 || navigator.appVersion.indexOf('MSIE 7.0')>0){
            bver=6;
        }
      findElements("XXXX",curWindow);
      return arr.join()+'|'+arrid.join();
    } else { return '||'; }
}
return getFrames();
'''
    tmpJs=tmpJs.replace('XXXX',inPath)
    tmpJs=tmpJs.replace('YYYY',keystr)
#     if inPath=="#selectCustomer_btnText":
#         WD.switch_to_default_content()
#         WD.switch_to_frame("mainFrame")
#         WD.switch_to_frame("tab_desktop_100036")
#         WD.switch_to_frame("ID_72254")
#         tmpS="var style=document.createElement('style');"
#         tmpS=tmpS+"document._qsa = [];document._qsa.push('a');document.documentElement.firstChild.appendChild(style);"
#         tmpS=tmpS+"style.styleSheet.cssText=\"#selectCustomer_btnText {x-qsa:expression(this.style.mzoom=='1'?0:function(e){e.style.mzoom='1';alert(e.id);alert(document._qsa.length);var aaaa=e;}(this))}\";"
#         tmpS=tmpS+"scrollBy(0, 0);alert(document._qsa.length);alert(typeof(aaaa));"
#         print tmpS
#         WD.execute_script(tmpS)
#         pass
    tmpStr=tmpJs.decode('utf-8')
    #print tmpStr
    arrseq=WD.execute_script(tmpStr)
    #print arrseq
    if arrseq[0]=="|":
        logging.log(15,"element not exists in any frames or hidden!")
        TmpCnt+=1
        return "|"
    TmpCnt=0
    arr,arrid=arrseq.split("|")
    for i in arr.split(','):
        WD.switch_to_frame(int(i))
    logging.log(15,'frames id sequence is ['+arrid+']')
    return arr


@log
def csInput_v(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    j=0
    while j<CONFIG['TimeOut']:
        try:
            e=WD.find_element_by_css_selector(innerParam[0])
            if e.is_displayed() and e.is_enabled():
                e.clear()
                e.send_keys(innerParam[1].decode('utf-8'))
                return True
            else:
                raise ElementNotVisibleException('css selector:"'+innerParam[0]+'" not visible')
        except Exception,e:
            WD.switch_to_default_content()
            j=j+1
            time.sleep(1)
            if type(e)==NoSuchElementException or type(e)==ElementNotVisibleException:
                _autoSwitchFramesByJs(innerParam[0])
            if type(e)==TimeoutException:
                logging.log(15,"page load timeout,try input again")
                return True
    raise NoSuchElementException('wait over time for '+str(CONFIG['TimeOut'])+'s'+':\n'+str(e))


@log
def csClick_v(Loc,Keystr=''):
    global WD
    if CONFIG["executeMode"]==1:
        print 'not support!!'
    j=0
    while j<CONFIG['TimeOut']:
        try:
            e=WD.find_elements_by_css_selector(Loc)
            if Keystr=='':
                if len(e)>0 and e[0].is_displayed() and e[0].is_enabled():
                    e[0].click()
                    return True
                raise ElementNotVisibleException('css selector:"'+Loc+'" not visible')
            else:
                if len(e)>0:
                    for i in e:
                        if i.text.strip()==Keystr and i.is_displayed() and i.is_enabled():
                            i.click()
                            return True
                raise NoSuchElementException('css selector:"'+Loc+'" no such element')
        except Exception,e:
            #print str(j)+"times"
            #print 'switch to default_content'
            WD.switch_to_default_content()
            time.sleep(1)
            j=j+1
            if type(e)==NoSuchElementException or type(e)==ElementNotVisibleException:
                _autoSwitchFramesByJs(Loc,Keystr)
            if type(e)==TimeoutException:
                logging.log(15,"page load timeout,try click again")
                return True
    raise NoSuchElementException('wait over time for '+str(CONFIG['TimeOut'])+'s'+':\n'+str(e))

@log
def csValue_v(Loc,Attr,InV=[]):
    global WD
    tmp=''
    j=0
    while j<CONFIG['TimeOut']:
        try:
            if Attr=="html":
                tmp=WD.find_element_by_css_selector(Loc).text.encode('utf-8')
                InV.append(tmp)
            else:
                tmp=WD.find_element_by_css_selector(Loc).get_attribute(Attr).encode('utf-8')
                InV.append(tmp)
            return tmp.strip()
        except Exception,e:
            WD.switch_to_default_content()
            time.sleep(1)
            j=j+1
            if type(e)==NoSuchElementException or type(e)==ElementNotVisibleException:
                _autoSwitchFramesByJs(Loc)
            if type(e)==TimeoutException:
                logging.log(15,"page load timeout,try get value again")
                return True
    raise NoSuchElementException('wait over time for '+str(CONFIG['TimeOut'])+'s'+':\n'+str(e))


@log
def csSelect(Loc,InV):
    global WD
    j=0
    while j<CONFIG['TimeOut']:
        try:
            childPath=Loc+" > option[value='"+InV+"']"
            WD.find_element_by_css_selector(childPath).click()
            return True
        except Exception,e:
            WD.switch_to_default_content()
            time.sleep(1)
            j=j+1
            if type(e)==NoSuchElementException or type(e)==ElementNotVisibleException:
                _autoSwitchFramesByJs(Loc)
    raise NoSuchElementException('wait over time for '+str(CONFIG['TimeOut'])+'s'+':\n'+str(e))


@log 
def csDbClick(*inputParam):
    global WD
    if CONFIG["executeMode"]==1:
        innerParam=[] if len(inputParam)==0 else inputParam[0]
    else:
        innerParam=list(inputParam)
    j=0
    while j<CONFIG['TimeOut']:
        try:
            e=WD.find_element_by_css_selector(innerParam[0])
            if e.is_displayed() and e.is_enabled():
                ActionChains(WD).double_click(e).perform()
                return True
            else:
                raise ElementNotVisibleException('css selector:"'+innerParam[0]+'" not visible')
        except Exception,e:
            #print str(j)+"times"
            #print 'switch to default_content'
            WD.switch_to_default_content()
            time.sleep(1)
            j=j+1
            if type(e)==NoSuchElementException or type(e)==ElementNotVisibleException:
                _autoSwitchFramesByJs(innerParam[0])
            if type(e)==TimeoutException:
                logging.log(15,"page load timeout,try double click again")
                return True
    raise NoSuchElementException('wait over time for '+str(CONFIG['TimeOut'])+'s'+':\n'+str(e))
    
    
@log
def getAuthCode(Loc='',ex=0,ey=0,ew=0,eh=0):
    global WD
    if CONFIG["executeMode"]==1:
        print 'not support'
        return
    #获取元素在iframe中的绝对位置
    WD.switch_to_default_content()
    frames=_autoSwitchFramesByJs(Loc)
    WD.switch_to_default_content()
    ifX=ex
    ifY=ey
    if len(frames)>0 and frames!="|":
        tmpF=frames.split(",")
        for i in tmpF:
            e=WD.find_elements_by_css_selector('iframe')[int(i)]
            ifX=ifX+e.location.get('x')
            ifY=ifY+e.location.get('y')
            WD.switch_to_frame(int(i))
        print ifX,ifY
        
    #获取整个页面的截图
    savPath=CONFIG['path'] + '\\ocr'
    if os.path.isfile(savPath+'\\tmp_page.png'):
        os.system('del '+savPath+'\\*.png')
    WD.save_screenshot(savPath+'\\tmp_page.png')
    #通过传入的xywh坐标和宽长，使用nconvert抠出验证码图片并存为result.png
    if Loc[0]=="/":
        e=WD.find_element_by_xpath(Loc)
    else:
        e=WD.find_element_by_css_selector(Loc)
    tmpCmd=savPath+"\\nconvert -quiet -o "+savPath+"\\result.png -crop "
    tmpCmd=tmpCmd+str(e.location.get('x')+ifX)+' '+str(e.location.get('y')+ifY)+' '+str(e.size.get('width')+ew)+' '+str(e.size.get('height')+eh)
    tmpCmd=tmpCmd+' '+savPath+"\\tmp_page.png"
    #print tmpCmd
    os.system(tmpCmd)
    
    #返回的string写入web元素内
    authCode=getChr(savPath)
    if getSplitLenth()>0:
        logging.warn("the split length of bitmap file is <"+str(getSplitLenth())+">,check OcrMod if not correct")
        logging.log(15,"the auth code is:"+authCode)
    return authCode


@log 
def isEnable(Loc,oVal=[]):
    global WD
    try:
        if Loc[0]=="/":
            e=WD.find_element_by_xpath(Loc)
        else:
            e=WD.find_element_by_css_selector(Loc)                    
        if e.is_enabled() and e.is_displayed():
            logging.log(15,"element is ok to oper")
            oVal.append(True)
            return True
        else:
            oVal.append(False)
            return False
    except Exception,e:
        logging.log(15,"element not exist")
        return False

@log 
def isDisplay(Loc,oVal=[]):
    global WD
    try:
        if Loc[0]=="/":
            e=WD.find_element_by_xpath(Loc)
        else:
            e=WD.find_element_by_css_selector(Loc)                    
        if e.is_displayed():
            logging.log(15,"element is ok to oper")
            oVal.append(True)
            return True
        else:
            oVal.append(False)
            return False
    except Exception,e:
        logging.log(15,"element not exist")
        return False

@log 
def csWait(Loc):
    global WD
    i=0
    tmpStr=""
    we=WD.find_elements_by_css_selector(Loc)
    if len(we)>0:
        return True
    while i<CONFIG['TimeOut']:
        WD.switch_to_default_content()
        tmpStr=_autoSwitchFramesByJs(Loc)
        #print tmpStr
        if len(tmpStr)>0 and tmpStr[0]!="|":
            return True
        i+=1
        time.sleep(1)
    return False


#接口函数---------------------------------------------------
@log
def sendPost(url,sdata,sheader={}):
    global cookie
    if cookie==None:
        cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    req=urllib2.Request(url)
    #默认的header
    req.add_header('User-Agent', 'ATtester')
    req.add_header('Accept', 'text/plain')
    #自动以文件头不为空，则加入
    if sheader!={}:
        for i in sheader.keys():
            req.add_header(i, sheader[i])
    rep=opener.open(fullurl=req,data=sdata)
    return rep.read()


@log
def sendGet(url,sheader={}):
    global cookie
    if cookie==None:
        cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    req=urllib2.Request(url)
    #默认的header
    req.add_header('User-Agent', 'ATtester')
    req.add_header('Accept', 'text/plain')
    #自动以文件头不为空，则加入
    if sheader!={}:
        for i in sheader.keys():
            req.add_header(i, sheader[i])
    rep=opener.open(req)
    tmp=rep.read()
    #print tmp
    return tmp

def sendMail(inputParam={}):
    content=inputParam['content']
    msg=MIMEMultipart()
    msg.attach(MIMEText(content, 'html', 'utf-8'))
    smtp_server=inputParam['smtp_server']
    from_addr = inputParam['from_addr'].decode('utf-8')
    password = inputParam['password']
    to_addr=inputParam['to_addr']
    cc_addr=''
    if 'cc_addr' in inputParam.keys():
        cc_addr=inputParam['cc_addr']
    title=inputParam['title']
    if 'attach' in inputParam.keys():
        attachFile=inputParam['attach']
        #add attachment start
        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(file(CONFIG['path']+'temp\\'+attachFile, 'rb').read())
        encode_base64(attach)
        attach.add_header('Content-Disposition', 'attachment', filename=attachFile)
        msg.attach(attach)
        #add attachment end
    msg['From']= from_addr
    msg['To'] = to_addr.decode('utf-8')
    if cc_addr!='':
        msg['Cc'] = cc_addr.decode('utf-8')
        to_addr=to_addr+","+cc_addr
    #join Cc and To
    
    msg['Subject'] = Header(title.decode('utf-8'))
    try:
        server = smtplib.SMTP(smtp_server, 25)
        #server.set_debuglevel(1)
        server.login(from_addr,password)
        tmpMap=server.sendmail(from_addr, to_addr.split(','), msg.as_string())
        #print tmpMap
        print 'send ok,quit later'
        server.quit()
        if tmpMap=={}:
            r='ok'
        else:
            r=str(tmpMap)
        return r
    except Exception,e:
        #server.quit()
        logging.exception(e)
        return 'send mail error'

@log 
def clearCookie():
    global cookie
    cookie=None

def getDriver():
    global WD
    return WD

@log
def csScrollToElement(Loc,Keystr=''):
    global WD
    if CONFIG["executeMode"]==1:
        print 'not support!!'
    j=0
    while j<CONFIG['TimeOut']:
        try:
            e=WD.find_elements_by_css_selector(Loc)
            if Keystr=='':
                if len(e)>0 and e[0].is_enabled(): 
                    WD.execute_script("arguments[0].focus();",e[0])
                    return True
                raise ElementNotVisibleException('css selector:"'+Loc+'" not visible')
            else:
                if len(e)>0:
                    for i in e:
                        if i.text.strip()==Keystr and i.is_displayed() and i.is_enabled():
                            i.click()
                            return True
                raise NoSuchElementException('css selector:"'+Loc+'" no such element')
        except Exception,e:
            #print str(j)+"times"
            #print 'switch to default_content'
            WD.switch_to_default_content()
            time.sleep(1)
            j=j+1
            if type(e)==NoSuchElementException or type(e)==ElementNotVisibleException:
                _autoSwitchFramesByJs(Loc,Keystr)
            if type(e)==TimeoutException:
                logging.log(15,"page load timeout,try click again")
                return True
    raise NoSuchElementException('wait over time for '+str(CONFIG['TimeOut'])+'s'+':\n'+str(e))

@log
def dragAndDrop(srcLoc,dstLoc):
    global WD
    _waitElement(srcLoc)
    _waitElement(dstLoc)
    try:
        if srcLoc[0]=="/" and dstLoc[0]=="/" :
            e=WD.find_element_by_xpath(srcLoc)
            t=WD.find_element_by_xpath(dstLoc)
            logging.log(15,"element disabled status is "+str(WD.find_element_by_xpath(srcLoc).get_attribute("disabled")))
            logging.log(15,"element disabled status is "+str(WD.find_element_by_xpath(dstLoc).get_attribute("disabled")))
            ActionChains(WD).drag_and_drop(e,t).perform()

        else: 
            e=WD.find_element_by_css_selector(srcLoc)
            t=WD.find_element_by_css_selector(dstLoc)
            logging.log(15,"element disabled status is "+str(WD.find_element_by_css_selector(srcLoc).get_attribute("disabled")))
            logging.log(15,"element disabled status is "+str(WD.find_element_by_css_selector(dstLoc).get_attribute("disabled")))
            ActionChains(WD).drag_and_drop(e,t).perform()
        return True
    except UnexpectedAlertPresentException:
        WD.switch_to_alert().accept()
        logging.log(15,'这里要重新考虑下元素事件里面会弹出小窗的情况')
    except TimeoutException:
        logging.log(15,"page load timeout,try click again")
        return True


#new search frame
def csClick_p(Loc,Keystr=''):
    global WD
    frames = WD.FindElements(WD.By.TagName("frame"))
    for frame in frames:
        print frame
    
    # foreach (var frame in frames)
    # {
    #     if (frame.GetAttribute("name") == "ControlPanelFrame")
    #     {
    #         controlPanelFrame = frame;
    #         break;
    #     }
    # }
    # 
    # if (controlPanelFrame != null)
    # {
    #     driver.SwitchTo().Frame(controlPanelFrame);
    # }        
    # 
    # // find the spane by id in frame "ControlPanelFrame"
    # Se.IWebElement spanElement = driver.FindElement(Se.By.Id("testcategory"));