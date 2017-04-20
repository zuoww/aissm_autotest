#-*-coding:utf-8-*-
#run after error
print 'run this when met error!'

#按照逻辑判断页面的错误信息并获取，遇到错误直接重新登录
if getDriver()!=None:
    #判断是否有弹出报错
    #switchFrame()
    errtag=True
    if csWait(".c_msg>div>div.info>div>div.content"):
        try:
            errmsg=csValue_v(".c_msg>div>div.info>div>div.content","html")
            if len(errmsg)>0:
                if len(errmsg)<300:
                    errmsg=csValue(".c_msg>div>div.info>div>div.content","html","stepname:异常捕获,outputkey:NULL,group:1")
                logging.info(errmsg)
            else:
                errtag=False            
        except Exception,e:
            print e
    if errtag=False & csWait("#wade_messagebox-2_ct"):
        try:
            errmsg=csValue_v("#wade_messagebox-2_ct","html")
            if len(errmsg)>0:
                errtag=True
                if len(errmsg)<300:
                    errmsg=csValue("#wade_messagebox-2_ct","html","stepname:异常捕获,outputkey:NULL,group:1")
                logging.info(errmsg)
        except Exception,e:
            print e
    if errtag=False & csWait("#wade_messagebox-2_detail_text"):
        try:
            errmsg=csValue_v("#wade_messagebox-2_detail_text","html")
            if len(errmsg)>0:
                errtag=True
                if len(errmsg)<300:
                    errmsg=csValue("#wade_messagebox-2_detail_text","html","stepname:异常捕获,outputkey:NULL,group:1")
                logging.info(errmsg)
        except Exception,e:
            print e
else:
    #******************/更新计划执行进度/*********************
    EX=ExecuteDb()
    EX.update_Plan_Exec(4)
    #******************/更新计划执行进度/*********************
    logging.info("plan exception out,result fail,please check!")
'''
if getDriver()!=None:
    try:
        #判断是否有弹出报错
        getPic()
        ErrMsg=''
        #switchFrame()
        #先判断有无遮罩popup_loading
        if isDisplay("#popup_loading") and isEnable("#popup_loading"):
            exeJs_v("AI.Ui.hidePopup('popup_loading')")
        if isEnable("#secondCheck"):
            exeJs_v("AI.Ui.hidePopup('secondCheck')")
        #先判断顶层判断有无报错窗口
        #if isEnable("#popup_error")
        if "block" == exeJs_v("return $('#popup_error').css('display')"):
            #clickElement_v("html/body/div[5][@id='popup_error']")
            #exeJs_v("document.getElementById('popup_error').class='ui-popup-wrap.fn-clear'")
            exeJs_v("document.getElementById('popup_error').style.visibility='visible'")
            exeJs_v("document.getElementById('popup_error').style.display='inline'")
            #csClick_v("#popup_error")
            #ErrMsg+=getValue("div.ui-tipbox.ui-tipbox-error.ui-tipbox-pop>div>h3.ui-tipbox-title","html","stepname:异常提示,outputkey:NULL,group:1")+"/"
            #print ErrMsg.decode('utf-8').encode('gbk')
            csClick_v("input[value='取 消']")
            #clickElement_v("//div[@id='popup_error']/div[1]/div[2]/p[1]/input[@class='ui-button ui-button-lcrm']")
            #ErrMsg+=csValue("#popup_error h3.ui-tipbox-title","html","stepname:异常提示-,outputkey:NULL,group:1")+"/"       
            #clickElement_v("#popup_error>input")
	    #csClick_v('#popup_error input')
            print ErrMsg.decode('utf-8')
        #切换到当前业务层frame下找报错窗口
        if exeJs_v("return $('div.ui-iframe-panel-current>iframe').length")==1:
            FrameId=csValue_v("div.ui-iframe-panel-current>iframe","id")
            switchFrame("#"+FrameId)
            if isEnable("#data_msg_id"):
                ErrMsg+=csValue("#data_msg_id p.ui-tipbox-explain","html","stepname:异常信息->,outputkey:NULL,group:1")+"/"
            #if isEnable("#popup_error"):
            if "block" == exeJs_v("return $('#popup_error').css('display')"):
                print '1 error'
                #ErrMsg+=csValue("#popup_error h3.ui-tipbox-title","html","stepname:异常信息->,outputkey:NULL,group:1")+"/"
		ErrMsg+=csValue_v("#popup_error h3.ui-tipbox-title","html")+"/"
		ListMsg_error=StepReport().getStepList()[-1].split(',')[2]
		StepReport().getStepList()[-1].split(',')[2]=ListMsg_error+"||"+ErrMsg			
                clickElement_v("div#popup_error>input.ui-button.ui-button-lcrm")
        #输出错误信息
        print ErrMsg.decode('utf-8')
        if ErrMsg!='':
            setOutput(ErrMsg)
    except Exception,e:
        print e
        #判断浏览器是否异常弹出
        try:
            cnt=[]
            getTitles(cnt)
            if len(cnt)==0:
                changeLogin(staff_id,passwd)
        except:
            logging.info('login error after exception,exit now!')
            raise SystemExit
'''
    
