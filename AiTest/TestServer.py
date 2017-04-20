#-*-coding:utf-8-*-

from wsgiref.simple_server import make_server
from BasicFunction import *
import subprocess
import sys
import os
import urllib
import json

Port=1414
Host='0.0.0.0'
RestartTimes=0

def AppFunction(environ, start_response):
    global RestartTimes
    method = environ.get('REQUEST_METHOD')
    path = environ.get('PATH_INFO')
    #*****************/改造增加部分/******************
    #增加读取body
    #body=json.load(environ.get('REQUEST_BODY'))
    #接收post请求并解析执行参数
    if method=="POST" and path=="/test":
        start_response('200 OK', [('Content-Type', 'text/html'),('Access-Control-Allow-Origin','*')])
        print 'post ok'
        tmpbody=environ.get('wsgi.input').read(int(environ['CONTENT_LENGTH']))
        print tmpbody
        body=json.loads(tmpbody)
        print body
        CONFIG['plan_id']=str(body.get('plan_id'))
        CONFIG['group_id']=str(body.get('group_id'))
        CONFIG['pre_planbatchid']=str(body.get('pre_planbatchid'))
        print sys.argv[1]
        tmpPath=sys.argv[1] + '\\config.ini'
        print tmpPath
        fp=file(tmpPath)    
        lines=[]
        for line in fp:
            lines.append(line)
        fp.close()
        lines[2]='plan_id='+CONFIG['plan_id']+'\n'
        lines[5]='group_id='+CONFIG['group_id']+'\n'
        lines[8]='pre_planbatchid='+CONFIG['pre_planbatchid']+'\n'
        s=''.join(lines)
        fp=file(tmpPath,'w')
        fp.write(s)
        fp.close()
        if CONFIG['pre_planbatchid']=="":
            print "本次执行判定为:首次执行; 执行计划号:".decode('utf-8').encode('gbk')+CONFIG['plan_id']+", 组号:".decode('utf-8').encode('gbk')+CONFIG['group_id']+", 请关注执行情况".decode('utf-8').encode('gbk')
        else:
            print "本次执行判定为:失败重执行执行; 重执行计划批次号:".decode('utf-8').encode('gbk')+CONFIG['pre_planbatchid']+", 组号:".decode('utf-8').encode('gbk')+CONFIG['group_id']+", 请关注重执行情况".decode('utf-8').encode('gbk')
        if 'HTTP_USER_AGENT' in environ:
            print 'start from web'
            tmpPath=CONFIG['path'] + '\\TestServer.bat start web'
        else:
            tmpPath=CONFIG['path'] + '\\TestServer.bat start'
        tmpStr=os.popen('tasklist |findstr "RunWeb" |find /v "" /c').read().strip()
        print tmpStr
        if tmpStr=='0':
            subprocess.Popen(tmpPath,shell=True)
        return ['start once']      
    #*****************/改造增加部分/******************
    #post请求是重新开始测试
    elif method=="POST" and path=="/testpost":
        print 'post ok'
        #获取web传入参数
        tmpStr=environ.get('wsgi.input').read(int(environ['CONTENT_LENGTH']))
        tmpScripts=tmpStr[:-1].split('|')
        for i in tmpScripts:
            nid,script=i.split('&')
            sid='0'*(4-len(nid))+nid
            script='#-*-coding:utf-8-*-\nstartCase('+str(nid)+')\n'+urllib.unquote(script)+'\nendCase('+str(nid)+')'
            #GenActionList
            tmpPath=CONFIG['path'] + '\\temp\\AT_SCRIPT_'+sid+'.py'
            with open(tmpPath,'w') as f1:
                f1.write(script)
        start_response('200 OK', [('Content-Type', 'text/html'),('Access-Control-Allow-Origin','*')])
        return []
    elif method=="POST" and path=="/tasklist":
        start_response('200 OK', [('Content-Type', 'text/html')])
        tmpStr=environ.get('wsgi.input').read(int(environ['CONTENT_LENGTH']))
        if tmpStr[4:]==str(CONFIG['tlPWD']):
            tmpStr=os.popen('tasklist |findstr "RunWeb" |find /v "" /c').read().strip()
            if tmpStr=='0':
                tmpStr=CONFIG['path'] + '\\TestServer.bat start'
                subprocess.Popen(tmpStr,shell=True)
                tmpStr='''
<!DOCTYPE html>
<html><head><meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
<script></script>
</head><body><p>测试启动成功</p>
</body><html>
                '''
                return [tmpStr]
            else:
                return ['already run,do not refresh']
        else:
            return ['password error']
    elif method=="POST" and path=="/outputFile":
        start_response('200 OK', [('Content-Type', 'text/html'),('Access-Control-Allow-Origin','*')])
        try:
            tmpStr=environ.get('wsgi.input').read(int(environ['CONTENT_LENGTH']))
            tmpStr=tmpStr.replace('\n', '\r\n')
            f1=open(CONFIG['path'] + '\\ScriptsOuput.txt','wb')
            f1.write(tmpStr.decode('utf-8').encode('gbk'))
            f1.close()
        except Exception,e:
            print e
        return ['']
        
    #get指令
    elif method=="GET":
        if path!="/selenium.log":
            start_response('200 OK', [('Content-Type', 'text/html'),('Access-Control-Allow-Origin','*')])
        if path[0:8]=="/restart":
            #将上次未测试的结果
            if path=='/restart?force=1':
                #获取测试脚本总数
                tmpPath=CONFIG['path'] + '\\temp\\'
                tmpRun=os.listdir(tmpPath)
                runList=[]
                for i in range(0,len(tmpRun)):
                    if 'AT_SCRIPT_' in tmpRun[i]:
                        runList.append(tmpRun[i])
                f1=open(CONFIG['path'] + '\\result.txt','rb')
                resultContent=''
                for i in f1.readlines():
                    if i.strip()!='' and i[0:4]=='pass':
                        resultContent+=i+'\r\n'
                    elif i.strip()!='' and i[0:4]!='pass':
                        resultContent+='wait|0:00:00|\r\n'
                    else:
                        pass
                f1.close()
                #判断测试脚本总数与测试结果是否相等，不等则补充到相等为止
                tmpCnt=len(runList)-resultContent.count('\n')
                for i in range(tmpCnt):
                    resultContent+='notRun|0:00:00|\r\n'
                #完成复测处理，保存结果文件
                f1.open(CONFIG['path'] + '\\last_result.txt','wb')
                f1.write(resultContent)
                f1.close()
            tmpPath=CONFIG['path'] + '\\TestServer.bat restart'
            tmpStr=os.popen('tasklist |findstr "RunWeb" |find /v "" /c').read().strip()
            if tmpStr=='0':
                subprocess.Popen(tmpPath,shell=True)
                return ['restart ok']
            else:
                return ['running']
        elif path=="/test":
            print 'get ok'
            if 'HTTP_USER_AGENT' in environ:
                print 'start from web'
                tmpPath=CONFIG['path'] + '\\TestServer.bat start web'
            else:
                tmpPath=CONFIG['path'] + '\\TestServer.bat start'
            tmpStr=os.popen('tasklist |findstr "RunWeb" |find /v "" /c').read().strip()
            if tmpStr=='0':
                subprocess.Popen(tmpPath,shell=True)
            return ['start once']
        elif path=="/jquery.min.js":
            f=open(CONFIG['path'] + '\\temp\\jquery.min.js','rb')
            return f
        elif path=="/selenium.log":
            start_response('200 OK', [('Content-Type', 'application/force-download'),('Content-Disposition','attachment;filename=selenium.log')])
            f=open(CONFIG['path'] + '\\selenium.log','rb')
            return f
        elif '/GetTempFileStream/' in path:
            tempFile=path.split('/')[-1]
            
            tmpPath=CONFIG['path'] + '\\temp\\'+tempFile
            if os.path.exists(tmpPath):
                f=open(tmpPath,'rb')
                return f
            else:
                return ['']
        #开始录制脚本
        elif "GetTempFileStream" in path:
            
            return ['ok']
        #停止录制脚本
        elif "/forceStop"==path:
            os.system("taskkill -f /im RunWeb.exe")
            return ['ok']
        elif path=="/getStatus":
            tmpStr=os.popen('tasklist |findstr "RunWeb" |find /v "" /c').read().strip()
            if tmpStr=='0':
                f=open(CONFIG['path'] + '\\result.txt','rb')
                return f
            else:
                return ['running']
        elif path=="/cleanTempFile":
            os.popen('del '+CONFIG['path']+'\\temp\\AT_SCRIPT_*')
            return ['ok']
        elif path=="/tasklist":
            tmpR='''
<!DOCTYPE html>
<html><head><title>测试执行</title><meta http-equiv='Content-Type' content='text/html; charset=utf-8'></head><body>
<form method='post' action='/tasklist' name='login'><span>请输入口令启动测试：</span><input name='pwd' type='text'>
<button onclick='submit()'>确定</button></form>
</body><html>
            '''
            return [tmpR.decode('gbk').encode('utf-8')]
        else:
            return ['']
            
try:
    initConfig(sys.argv[1])
    #判断请求来源，默认是excel发起
    print 'path-->'+CONFIG['path']
    httpd=make_server(Host, Port, AppFunction)
    httpd.serve_forever()
except Exception,e:
    print e
