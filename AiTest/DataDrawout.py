#coding=utf-8
import datetime
import os
import time
import logging
import codecs

import sys
import threadpool
from PackFunction import *

from BasicFunction import *
from DBpool import *
#import chardet
import os

__author__ = 'chenchen'

#测试数据准备
class DataDrawout():
    """
    #抽取类型type，按计划或用例
    #抽取id，对应计划ID或caseid
    #抽取数据数量maxNum
    #测试系统的测试环境sys_env：test/uat
    #测试的区域id：region_id
    """
    @log
    def getMaxNum(self):
        return self.maxNum

    @log
    def setMaxNum(self):
        self.maxNum=CONFIG['maxNum']

    @log
    def getSysEnv(self):
        return self.sys_env

    @log
    def setSysEnv(self):
        self.sys_env=CONFIG['sys_env']

    @log
    def getRegionId(self):
        return self.maxNum

    @log
    def setRegionId(self):
        self.region_id=CONFIG['region_id']

    @log
    def getyMoth(self):
        return self.yMoth

    @log
    def setyMoth(self):
        self.yMoth=time.strftime("%Y%m")

    def getlastMoth(self):
        return self.lastMoth

    def setlastMoth(self):
        year =datetime.datetime.now().year
        month =datetime.datetime.now().month
        if month == 1 :
            month = 12
            year -= 1
        else :
            month -= 1
        result = datetime.datetime.strptime('%s%s'%(year, month), '%Y%m')
        self.lastMoth=result.strftime("%Y%m")

    def getnextMoth(self):
        return self.nextMoth

    def setnextMoth(self):
        year =datetime.datetime.now().year
        month =datetime.datetime.now().month
        if month == 12 :
            month = 1
            year += 1
        else :
            month += 1
        result = datetime.datetime.strptime('%s%s'%(year, month), '%Y%m')
        self.nextMoth=result.strftime("%Y%m")


    def __init__(self):
        #initConfig(sys.path[0])
        #print os.path.split(os.path.realpath(__file__))[0]
        #initConfig(os.path.split(os.path.realpath(__file__))[0])
        #print os.path.split(os.path.abspath(sys.argv[0]))[0]
        #initConfig(os.path.split(os.path.abspath(sys.argv[0]))[0])

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        elif __file__:
            path = os.path.dirname(__file__)
        print "@@@@@@@@@@@@@@@@@"+path
        initConfig(path)
        #初始化
        if CONFIG['logFile']=="y":
            logging.basicConfig(level=CONFIG["logLevel"],format='%(asctime)s %(levelname)s %(thread)s %(threadName)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',filename=CONFIG["path"]+"\\selenium.log",filemode="a")
        else:
            logging.basicConfig(level=CONFIG["logLevel"],format='%(asctime)s %(levelname)s %(thread)s %(threadName)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

        self.insert_sql = []
        self.setMaxNum()
        self.setRegionId()
        self.setSysEnv()
        self.setyMoth()
        self.setlastMoth()
        self.setnextMoth()
        try:
            self.dbmanage=DBSql(CONFIG['mysql_conStr'])
        except Exception,e:
            print e
            logging.info(e)

    @log
    def queryTblCaseDatapoolRelByPlanId(self,planid):
        """
        根据planid查询该计划下的用例测试数据查询sql
        :param planid: 计划id
        :return:list
        """
        if planid==None:
            return ''
        #print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" queryTblCaseDatapoolRelByPlanId  start"
        logging.info("queryTblCaseDatapoolRelByPlanId  start")
        sql="""SELECT rel.case_id,rel.datapool_keyword,rel.sql_code,rel.sql_type,rel.db_name,rel.sql_desc,
               rel.project_id,rel.eparchy_code,rel.ref_id
	        FROM tbl_case_datapool_rel rel, tbl_plan_case_rel plan
	        where rel.status=1 and plan.case_id = rel.case_id and plan.status = 1 and rel.sql_type='Get' and rel.sql_code!='' and plan.plan_id ="""+str(planid)
        print sql
        caseSqlTuple=self.dbmanage.getSqlList(sql)
        if len(caseSqlTuple)==0:
            print 'no plandata'
            return False
        #print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" queryTblCaseDatapoolRelByPlanId  end"
        logging.info(" queryTblCaseDatapoolRelByPlanId  end")
        return map(list,caseSqlTuple)#list<tuple>

    @log
    def queryTblCaseDatapoolRelByCaseId(self,caseid):
        """
        获取caseid对应的测试数据查询sql
        :param caseid:用例ID，可以是一个或多个,类型str
        :return:
        """
        sqllist=[]
        if caseid==None:
            return ''
        elif len(caseid.split(','))>=1:
            caselist=caseid.split(',')
            print type(caselist)
            for id in caselist:
                sql="""SELECT rel.case_id,rel.datapool_keyword,rel.sql_code,rel.sql_type,rel.db_name,rel.sql_desc,
               rel.project_id,rel.eparchy_code,rel.ref_id  FROM tbl_case_datapool_rel rel where rel.status=1 and sql_type='Get' and rel.sql_code!=''  and case_id in("""+id+")or FIND_IN_SET('"+id+"',ref_id)"
                logging.info("queryTblCaseDatapoolRelByCaseId  start")
                caseSqlTuple=self.dbmanage.getSqlList(sql)
                if caseSqlTuple and len(caseSqlTuple)==0:
                    logging.info('case'+id+'has no sqlcode')
                    return ''
                else:
                    for i in range(len(caseSqlTuple)):
                        sqllist.append(caseSqlTuple[i])
            sqllist=list(set(sqllist))
            print sqllist
        logging.info(" queryTblCaseDatapoolRelByCaseId  end")
        print type(sqllist)
        return map(list,sqllist)

    @log
    def cleanData(self,type,id):
        """
        按计划或用例清除测试数据
        :param type: 类型，按计划或用例
        :param id: 计划ID或用例id，以逗号分隔
        :param sys_env: 自动化测试系统环境
        :param region_id 区域id，如771
        :return:True/False
        """
        #idstr=','.join([str(v) for v in list(id)])
        idlist=id.split(',')
        if type=="plan":
            #print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" deleteAutoTestResByPlanId  start"
            logging.info(" deleteAutoTestResByPlanId  start")
            sql="delete FROM tbl_case_datapool where sys_env='"+self.sys_env+"' and region_id='"+str(self.region_id)+"' and case_id in (select case_id from tbl_plan_case_rel where status=1 and plan_id in("+id+"))"
            #print sql
        elif type=="case":
            sql=[]
            #print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+" deleteAutoTestResByCaseId  start"
            logging.info(" deleteAutoTestResByCaseId  start")
            sql1="delete FROM tbl_case_datapool where sys_env='"+self.sys_env+"' and region_id='"+str(self.region_id)+"' and case_id in ("+id+")"
            sql.append(sql1)
            tmpsql="SELECT rel.case_id FROM tbl_case_datapool_rel rel where status=1 and "
            tmpsql1="select rel.ref_id from tbl_case_datapool_rel rel where status=1 and "
            for caseid in idlist:
                tmpsql2=tmpsql+"ref_id in("+caseid+")"
                tmpsql3=tmpsql1+"case_id="+caseid
                caseSqlTuple=self.dbmanage.getSqlList(tmpsql2)
                if caseSqlTuple:
                    sql2="delete from tbl_case_datapool where sys_env='"+self.sys_env+"' and region_id='"+str(self.region_id)+"' and case_id="+str(caseSqlTuple[0][0])
                    sql.append(sql2)
                caseSqlTuple2=self.dbmanage.getSqlList(tmpsql3)
                if caseSqlTuple2 and caseSqlTuple2[0][0]:
                    sql3="delete from tbl_case_datapool where sys_env='"+self.sys_env+"' and region_id='"+str(self.region_id)+"' and case_id in("+str(caseSqlTuple2[0][0])+")"
                    sql.append(sql3)
                #print sql
        try:
            print sql
            self.dbmanage.dbwSql(sql)
            logging.info("deleteAutoTestRes  end")
            return True
        except Exception, e:
            print e
            logging.info(e)
            logging.debug("execute:" + str(sql) + "  ,ERROR")
            return False

    def getfullsqlcode(self,sql_code):
        sql2=sql_code.replace('&reg_id',str(self.region_id))
        sql2=sql2.replace('&yMoth',self.yMoth)
        sql2=sql2.replace("&lastMoth",self.lastMoth)
        sql2=sql2.replace("&nextMoth",self.nextMoth)
        return sql2

    @log
    def listselect(self, sql):
        """
        将sql查询语句通过线程执行
        :param sql:
        :return:
        """
        #print "sql:",sql
        case_id = sql[0]
        # 测试资源名称
        data_key = sql[1].encode("utf-8")
        # 数据准备sql
        sql_code = sql[2].encode("utf-8")
        if not sql_code:
            logging.info("case"+str(case_id)+" has no sqlcode")
            return
        sql_type = sql[3]
        data_name = " by DataDrawout"
        project_id = sql[6]
        eparchy_code = sql[7].encode("utf-8")
        ref_id=sql[8]
        sqlstring = self.getfullsqlcode(sql_code)
        sqlstring=sqlstring.decode('utf-8')
        tmpSql="insert into tbl_case_datapool(case_id,data_key,data_name,data_value,sys_env,region_id,data_type,datavalue_active,data_module,project_id,eparchy_code,insert_time) values ("
        if ref_id==''or ref_id==None:
            logging.info("case "+str(case_id)+' '+data_key+" execute sql start")
            start_time=datetime.datetime.now()
            dataResult=self.dbmanage2.getSqlList(sqlstring,self.maxNum)

            end_time=datetime.datetime.now()
            time=end_time-start_time
            logging.info("case "+str(case_id)+' '+data_key+" execute sql end")
            #print "case "+str(case_id)+" sql查询耗时:".decode('utf-8')+str(time)
            logging.info("case "+str(case_id)+' '+data_key+" sql查询耗时:".decode('utf-8')+str(time))

            if dataResult:
                for j in range(len(dataResult)):
                    #print "datavalue type:",type(dataResult[j][0])#str
                    if isinstance(dataResult[j][0], unicode):
                        #print "unicode----"
                        data_value=dataResult[j][0].encode("utf-8")
                    else:
                        #print "str-----"
                        data_value=dataResult[j][0]
                    sql=tmpSql + str(case_id)+",'"+data_key+"','"+data_name+"','"+data_value+"','"+self.sys_env+"','"+str(self.region_id)+"','Fixed',1,1,"+str(project_id)+",'"+eparchy_code+"',NOW())"
                    #print type(sql)
                    #sql=sql.decode("utf-8")
                    self.insert_sql.append(sql)
            else:
                logging.info("case "+str(case_id)+" no test resources")
                print "case"+str(case_id)+" no test resources"
        else:
            #print type(ref_id)
            caselist=ref_id.encode('utf-8').split(',')
            caselist.append(str(case_id))
            totalnum=self.maxNum * len(caselist)
            dataResult=self.dbmanage2.getSqlList(sqlstring,totalnum)
            print "查询结果总数".decode('utf-8')
            #print len(dataResult)
            if not dataResult:
                print "case"+','.join([str(v) for v in caselist])+" no test resources"
                return self.insert_sql
            elif len(dataResult)<totalnum:
                totalnum=len(dataResult)
            print totalnum
            id=0
            for j in range(totalnum):
                ref_data_key=data_key.replace('_'+str(case_id),'_'+str(caselist[id]))
                #print ref_data_key
                if isinstance(dataResult[j][0], unicode):
                    #print "unicode----"
                    ref_data_value=dataResult[j][0].encode("utf-8")
                else:
                    #print "str-----"
                    ref_data_value=dataResult[j][0]

                sql=tmpSql + str(caselist[id])+",'"+ref_data_key+"','"+data_name+"','"+ref_data_value+"','"+self.sys_env+"','"+str(self.region_id)+"','Fixed',1,1,"+str(project_id)+",'"+eparchy_code+"',NOW())"
                #sql=sql.decode("utf-8")
                self.insert_sql.append(sql)
                id+=1
                if id==len(caselist):
                    id=0
        return self.insert_sql

    @log
    def threadSelect(self,filepath, sqllist):
        """
        开启线程执行查询
        :param filepath:
        :param sqllist:
        :return:
        """
        poolsize=CONFIG['poolsize']
        pool = threadpool.ThreadPool(poolsize)
        requests = threadpool.makeRequests(self.listselect, sqllist)
        [pool.putRequest(req) for req in requests]
        pool.wait()
        f = open(filepath, 'w')
        #print self.insert_sql
        for sql in self.insert_sql:
            f.write(sql + '\n')
        f.write('commit;\n')
        f.close()

    @log
    def getInsertSql(self,filepath,sqllist):
        f=open(filepath,'w')
        #连接被测系统数据库，查询测试数据
        self.dbmanage2=DBSql(CONFIG['ora_conStr2'])
        self.threadSelect(filepath,sqllist)
        self.dbmanage2.close()

    @log
    def addData(self,filepath):
        print filepath
        count=0
        #f = open(filepath,'r')
        #fencoding=chardet.detect(f.read())
        #print fencoding

        with open(filepath, 'r') as g:
            for line in g:
                #print type(line.decode('gbk'))
                line=line.decode('gbk')
                self.dbmanage.insertSql(line)
                count=count+1
        self.dbmanage.close()
        count=count-1
        logging.info (("添加"+str(count)+"条测试数据成功！").decode('utf-8'))

    #@log
    #def updateData(self,case_id,datavalue):
        #updateSql="update tbl_case_datapool set datavalue_active=0 where case_id= %s and data_value= %s"
        #param=(case_id,datavalue)
    #    updateSql="update tbl_case_datapool set datavalue_active=0 where case_id='"+str(case_id)+"' and data_value='"+datavalue+"'"
        #cursor=self.conn.cursor()
        #n=cursor.execute(updateSql,param)
    #    n=self.dbmanage.dbwSql(updateSql)
    #    print n
        #self.conn.commit()
        #cursor.close()
    #    return n

    @log
    def drawoutData(self,idtype,id):
        start_time=datetime.datetime.now()
        #print type(id)
        if type(id)==list:
            id=','.join([str(v) for v in id])
            #print id
        if idtype=="plan":
            plansql="select 1 from  tbl_plan_exec where status=2 and plan_id="+id
            if len(self.dbmanage.getSqlList(plansql))>0:
                #print "plan"+str(id)+"正在执行中，不能抽取数据".decode('utf-8')
                logging.info("plan"+str(id)+"正在执行中，不能抽取数据".decode('utf-8'))
                #raise Exception(("计划正在执行中，不能抽取数据！").decode('utf-8'))
                return False
            #print start_time.strftime('%Y-%m-%d %H:%M:%S')+" datadrawout start"
            logging.info("datadrawout start")
            sqllist=self.queryTblCaseDatapoolRelByPlanId(id)
            #filepath="d:/out_sql/plan_"+str(id)+"_"+self.sys_env+"_"+str(self.region_id)+".sql"
        elif idtype=="case":
            sqllist=self.queryTblCaseDatapoolRelByCaseId(id)
            
        #判断sqllist为空时直接退出
        if sqllist == False:
            print 'Can not get Case'
            return False
        
        filepath=CONFIG['filepath']
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filepath=os.path.join(filepath,idtype+"_"+id+"_"+self.sys_env+"_"+str(self.region_id)+".sql")
        #print filepath
        self.getInsertSql(filepath,sqllist)
        self.cleanData(idtype,id)
        self.addData(filepath)
        end_time=datetime.datetime.now()
        #print end_time.strftime('%Y-%m-%d %H:%M:%S')+" datadrawout end"
        logging.info("datadrawout end")
        #print "抽取数据耗时:".decode('utf-8')+str((end_time-start_time))
        logging.info("抽取数据耗时:".decode('utf-8')+str((end_time-start_time)))
        return True

if __name__ == '__main__':
    dd=DataDrawout()
    dd.drawoutData('case','999')
    #dd.drawoutData('plan','662')


