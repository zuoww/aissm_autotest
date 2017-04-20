# coding=utf-8
import os
import subprocess
import traceback
from time import sleep


def verExec(Path, planBatchId='-1_20160824000000', batchId="all", eparchyCode="0471"):
    if Path != "":
        os.chdir(Path)
    print os.getcwd()
    # subprocess.Popen(['java', '-classpath',
    #                   'serverlib\ver_report.jar;serverlib\commons-collections-3.2.jar;serverlib\commons-configuration-1.5.jar;serverlib\commons-dbcp-1.2.2.jar;serverlib\commons-io-1.3.2.jar;serverlib\commons-jxpath-1.2.jar;serverlib\commons-lang-2.4.jar;serverlib\commons-logging-1.1.1.jar;serverlib\commons-pool-1.3.jar;serverlib\ibatis-2.3.4.726.jar;serverlib\log4j-1.2.12.jar;serverlib\mysql-connector-java-5.1.21-bin.jar;serverlib\ojdbc14.jar com.ailk.cuc.autotestbg.bootstrap.Bootstrap',
    #                   'client', '-1_20160824000000', 'all', '0010'],
    #                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    os.system("java -classpath serverlib\\ver_report.jar;"
              "serverlib\commons-collections-3.2.jar;"
              "serverlib\commons-configuration-1.5.jar;"
              "serverlib\commons-dbcp-1.2.2.jar;"
              "serverlib\commons-io-1.3.2.jar;"
              "serverlib\commons-jxpath-1.2.jar;"
              "serverlib\commons-lang-2.4.jar;"
              "serverlib\commons-logging-1.1.1.jar;"
              "serverlib\commons-pool-1.3.jar;"
              "serverlib\ibatis-2.3.4.726.jar;"
              "serverlib\log4j-1.2.12.jar;"
              "serverlib\mysql-connector-java-5.1.21-bin.jar;"
              "serverlib\ojdbc14.jar com.ailk.cuc.autotestbg.bootstrap.Bootstrap"
              " client  %s %s %s && pause" % (planBatchId, batchId, eparchyCode))
    # os.system('start_Case.bat')


def reportExec(Path="",batchId="all", eparchyCode="0471"):
    if Path != "":
        os.chdir(Path)
    print os.getcwd()
    os.system('java -classpath serverlib\\ver_report.jar;'
              'serverlib\commons-jexl-2.1.1.jar;'
              'serverlib\commons-configuration-1.5.jar;'
              'serverlib\commons-dbcp-1.2.2.jar;'
              'serverlib\commons-io-1.3.2.jar;'
              'serverlib\commons-jxpath-1.2.jar;'
              'serverlib\commons-lang-2.4.jar;'
              'serverlib\commons-logging-1.1.1.jar;'
              'serverlib\commons-pool-1.3.jar;'
              'serverlib\ibatis-2.3.4.726.jar;'
              'serverlib\log4j-1.2.12.jar;'
              'serverlib\mysql-connector-java-5.1.21-bin.jar;'
              'serverlib\ojdbc14.jar com.ailk.cuc.autotestbg.report.Bootstrap '
              'client %s %s && pause' % (batchId,eparchyCode))
    #os.system('start_Report.bat')


def startExec(Path=""):
    if Path != "":
        os.chdir(Path)
    print os.getcwd()
    os.startfile('TestServer.bat')
    sleep(5)
    # subprocess.Popen('TestServer.bat', creationflags=subprocess.CREATE_NEW_CONSOLE, stdout=subprocess.PIPE,
    #                 stderr=subprocess.PIPE, shell=True)


if __name__ == '__main__':
    verExec("C:\server", '-4_20161024164722')
    # reportExec('C:\server')
