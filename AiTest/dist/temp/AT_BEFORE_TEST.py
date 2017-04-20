#-*-coding:utf-8-*-
#前置处理器

#环境参数，干掉上次打开的ie
os.system("taskkill -f /im iexplore.exe")

#-------------------------------login-----
#测试环境 0准生产 1测试2准发布
TestEnv=2

#测试地址
if TestEnv==0:
    url='http://test-yy.crm.nm.cmcc/crmweb'
elif TestEnv==1:
    url='http://test-yy.crm.nm.cmcc/ngboss'
else:
    url='http://fb-yy.crm.nm.cmcc/ngboss'
    
#工号#可改成自己的工号
STAFF_ID='TEST71'
#密码
PASSWORD='11111111'

#打开链接，输入工号密码1
openUrl(url,20)
#switchAlert()
UserAccount=STAFF_ID
UserPwd=PASSWORD

if TestEnv==1:
    csInput_v("#UserAccount",UserAccount)
    csInput_v("#UserPwd",UserPwd)
    clickElement_v("//*[@id='fm_locallogin']/ul/li[4]/input")
    csClick_v("#loginBtn")
else:
    csInput_v("#STAFF_ID",STAFF_ID)
    csInput_v("#PASSWORD",PASSWORD)
    csClick_v("#loginBtn")
    switchWindow()

#switchWindow()
#屏蔽提示框
#exeJs_v("document.getElementById('helpNavPerson').style.overflow='hidden'")
def hideHelp():
    for i in range(3):
        try:
            exeJs_v("document.getElementById('helpNavPerson').style.display='none'")
            break
        except:
            time.sleep(1)
            pass
			
#号码登录认证
def loginAuth(phonenum='',password='1'):
    if phonenum=='':
        logging.info('phonenum is null,please check!')
        return
    for i in range(3):
        try:
            if csWait("#logoutButton") & isDisplay("#logoutButton"):
                #csClick_v("#logoutButton","","注销")注销暂不写入日志方便统计
                csClick_v("#logoutButton")
            csInput_v("#LOGIN_NUM","",phonenum)
            csInput("#LOGIN_NUM","",phonenum,"stepname:手机号码,outputkey:NULL,group:1")
            csInput("#LOGIN_VAL","",password,"stepname:服务密码,outputkey:NULL,group:1")
            csClick("#LOGIN_BTN","","登录")
            time.sleep(4)
            break
        except:
            refresh()
            time.sleep(2)
            hideHelp()

hideHelp()            
#csClick_v("#LOGIN_NUM")


#*******************/模板funs/*******************
#智能搜索，直至打开业务菜单开始受理
def searchMenu(menu_search='开户',menubar='',searchkeyWord='',submenu='1'):
    for i in range(3):#经测试，如果第一次不能打开，第三次一般可成功打开主菜单
        try:
            if i==0:
                csInput("#searchSpan>input","",menu_search,"stepname:菜单/商品名称搜索框,outputkey:NULL,group:1")
                if csWait("#button_search"):
                    clickElement("//span[@id='searchSpan']/button[@id='button_search']","","主菜单查询")
            else:
                csInput_v("#searchSpan>input",menu_search)
                if csWait("#button_search"):
                    clickElement_v("//span[@id='searchSpan']/button[@id='button_search']")
            if csWait(".link[ontap*="+menu_search+"]"):
                csClick(".link[ontap*="+menu_search+"]>div.main>div.title","",menu_search)
                break
        except:
            #由于页面刷新有bug，先不用
            #refresh()
            #clickElement_v("//*[@id='pageReload']")
            time.sleep(3)                                
    time.sleep(3)
    if menubar!='':
        for i in range(1,10):
            i=str(i)
            menu0=csValue_v("#CategoryPart_tab_li_"+i,"html")
            if menu0==menubar:
                csClick("#CategoryPart_tab_li_"+i,"",menubar)
                break
    time.sleep(3)
    if searchkeyWord!='':
        csInput("#searchkeyWord","",searchkeyWord,"stepname:菜单/商品名称搜索框,outputkey:NULL,group:1")
        csClick("#searchsearchButton","","子菜单搜索")
        time.sleep(3)
        #点击打开业务菜单，开始受理
        csWait("#wordOfferList")
        clickElement("//*[@id='wordOfferList']/div[1]/ul/li["+submenu+"]/div[1]","",searchkeyWord)
        time.sleep(2)

#进入我的业务子菜单
def clickMenu(menu0='个人促销类商品类',menu1='亲情',action='变更'):
    csWait("#myMoblie")
    csClick("#myMoblie","","我的移动")
    time.sleep(30)
    csWait(".c_list.c_list-s.c_list-hideSide")
    csClick(".c_list.c_list-s.c_list-hideSide>ul>li[value='5']","","我的业务")
    time.sleep(3)
    csWait("#serviceInfo_tab_li_0")
    for i in range(6):
        name=csValue_v("#serviceInfo_tab_li_"+str(i),"html")
        if name==menu0:
            csClick("#serviceInfo_tab_li_"+str(i),"",menu0)
            break
    time.sleep(1)
    csClick("#serviceInfo_page>div[title='"+menu0+"']>div.c_list>ul>li.group>div.main>div[tip*='"+menu1+"']>span.e_select","","选择")
    for i in range(3):#尝试处理action被浮标遮挡
        if i>0:
            clickElement("//*[@class=[c_float c_float-show]/div[2]/div/div/ul/li[1]","","选择")
            clickElement("//*[@class=[c_float c_float-show]/div[2]/div/div/ul/li[1]","","选择")
        else:
            try:
                csClick(".c_float.c_float-show>div>div>div>ul>li[title='"+action+"']","",action)
                break
            except:
                try:
                    if action=='变更' or action=='业务恢复':
                        csClick(".c_float.c_float-show","",action)
                    else:
                        clickElement("//*[@class=[c_float c_float-show]/div[2]/div/div/ul/li[3]","",action)
                    break
                except:
                    pass
    time.sleep(2)

#填充经办人信息    
def aggentInfo(id='护照',id_switch=1):
    '''
    检查点：15
    新增经办人信息,这里考虑了两种模式 
    id_switch=0:页面证件类型下拉被屏蔽
    id_switch=1:页面证件类型下拉未被屏蔽
    '''
    time.sleep(2)
    csWait(".link[ontap*=gentInfo]")
    csClick(".link[ontap*=gentInfo]","","经办人信息")
    csWait("#AggentInfoPart_editInfoButton")
    if isEnable("#AggentInfoPart_editInfoButton"):
        csClick("#AggentInfoPart_editInfoButton","","手工输入")
    if id='护照':
        csInput("#AggentInfoPart_NAME","","ZIDONGHUA","stepname:经办人,outputkey:NULL,group:1")
    elif id='身份证':
        csInput("#AggentInfoPart_NAME","","自动化","stepname:经办人,outputkey:NULL,group:1")
    csClick("#AggentInfoPart_CITY_span","","地市")
    csWait("#AggentInfoPart_CITY_list_ul")
    #time.sleep(1)
    exeJs_v("document.getElementById('AggentInfoPart_CITY_scroll').scrollTop=1000")
    #滑动下拉菜单使预选经办城市可见
    csClick("#AggentInfoPart_CITY_list_ul>li[val='471']>div","","呼和浩特市")
    if id=='身份证':
        AggentInfoPart_ID_NUM=str(makeNewregID())
    elif id=='护照':
        #护照号码要求6位以上不连续号码
        AggentInfoPart_ID_NUM=str(random.randint(0000000,9999999))
    elif id=='单位证件':
        #单位证件，要求长度=15
        AggentInfoPart_ID_NUM=str(random.randint(000000000000000,999999999999999))
    if id_switch==1:
        csClick("#AggentInfoPart_ID_TYPE_span","","证件类型")
        csClick("#AggentInfoPart_ID_TYPE_list_ul>li[title='"+id+"']","",id)
    else:
        pass
    csInput("#AggentInfoPart_ID_NUM","",AggentInfoPart_ID_NUM,"stepname:证件号码,outputkey:NULL,group:1")
    csInput("#AggentInfoPart_ADDR","","内蒙古省呼和浩特市自动化测试地址","stepname:联系地址,outputkey:NULL,group:1")
    csInput("#AggentInfoPart_PHONE","","13947186602","stepname:联系电话,outputkey:NULL,group:1")
    csInput("#AggentInfoPart_EAMIL","","13947186602@139.com","stepname:email,outputkey:NULL,group:1")
    csScrollToElement("#submitAggentInfo")
    csInput("#AggentInfoPart_DISTR","","内蒙古自动化测试备注填写信息","stepname:经办描述,outputkey:NULL,group:1")     
    csInput("#AggentInfoPart_REMARK","","自动化测试","stepname:备注,outputkey:NULL,group:1")
    csClick("#submitAggentInfo","","确定")
    time.sleep(2)
    
#等待订单生成，并打印和返回订单号
def getFlowId():
    order_id=''
    for i in range(2):        
        if csWait("#flowId"):
            try:
                order_id=getValue_v("#flowId","html")
            except:
                order_id=''
            if order_id!='':
                order_id=getValue("#flowId","html","stepname:订单号,outputkey:NULL,group:1")
                print order_id
                break
    if order_id=='':
        order_id=getValue("#flowId","html","stepname:订单号,outputkey:NULL,group:1")
    return order_id

#生成的号码资源入资源池
def dataGiveNext(next_case_id,data_value):
    """
    将本次使用数据源给下一条指定用例使用
    param：next_case_id 下一用例号
           data_value   插入的数据信息。
    格式：dataGiveNext(2,"ACCESS_NUM:"+PHONENUM)
    """
    dataname="DP_%s" % next_case_id
    sql='''INSERT INTO `autotest`.`tbl_case_datapool` (
	`plan_id`,`case_id`,`data_key`,`data_name`,`data_value`,`sys_env`,`region_id`,`project_id`,`eparchy_code`)
    VALUES ('0','%s','%s','LastCase','%s','test','471','0','0471');''' % (next_case_id,dataname,data_value)
    
    print sql
    DB=DBSql(CONFIG['mysql_conStr'])
    DB.dbwSql(sql)
    DB.close()
    
#客管中心等各个中心业务
def centerMore(submenu='实名制信息录入',menu='客户信息管理',subcenter='客户管理',center='客户中心'):
    csClick("#welTab_tab_li_3","","更多")
    for i in range(10):
        i=str(i)
        temp_center=csValue_v("#menus_tab_li_"+i,"html")
        if temp_center==center:
            csClick("#menus_tab_li_"+i,"",center)
            break
    for j in range(1,10):
        j=str(j)
        k=str(int(i)+1)
        temp_subcenter=getValue_v("//*[@id='navMenu_L1_"+k+"']/div/ul/li["+j+"]/div","html")
        if temp_subcenter==subcenter:
            clickElement("//*[@id='navMenu_L1_"+k+"']/div/ul/li["+j+"]/div","",subcenter)
            break
    for m in range(1,20):
        m=str(m)
        temp_menu=getValue_v("//*[@id='content_"+i+"']/div[2]/div["+str(int(j)*2)+"]/div/ul/li["+m+"]/div","html")
        if temp_menu==menu:
            clickElement("//*[@id='content_"+i+"']/div[2]/div["+str(int(j)*2)+"]/div/ul/li["+m+"]/div","",menu)
            break
    for n in range(1,20):
        n=str(n)
        temp_submenu=getValue_v("//*[@id='content_"+i+"']/div[2]/div[@class='l_colItem']/div[2]/div/div/ul/li["+n+"]","html")
        print temp_submenu.decode('utf-8').encode('gbk')
        print type(temp_submenu)
        print submenu.decode('utf-8').encode('gbk')
        print type(submenu)
        if temp_submenu==submenu:
            clickElement("//*[@id='content_"+i+"']/div[2]/div[@class='l_colItem']/div[2]/div/div/ul/li["+n+"]","",submenu)
            break
    time.sleep(2)

#密码解密
def decipher_nm(inputString):
    result=[]
    nOffSet=int(inputString[0:2],16)
    nKeyIndex=0
    tmpRange=[x for x in range(2, len(inputString),2)]
    for i in tmpRange:
        nBaseChar=int(inputString[i:i+2],16)
        nBitKey=int(ord('NM Mobile Password'[nKeyIndex]))
        nCodeChar=nBaseChar^nBitKey
        if nCodeChar<=nOffSet:
            nCodeChar = 255 + nCodeChar - nOffSet
        else:
            nCodeChar -= nOffSet
        result.append(chr(nCodeChar))
        nOffSet = nBaseChar
        if nKeyIndex>=len('NM Mobile Password'):
            nKeyIndex=0
        else:
            nKeyIndex+=1
    return ''.join(result)

#*******************开户封装模块**********************
'''
author:zuoww
date:20161105
'''
def selectNum(PHONENUM,i=1):
    '''
    选择未使用号码页面
    '''
    csWait("#newAccessNumLi>div[class='more']")
    csClick("#newAccessNumLi>div[class='more']","","选择号码")
    csInput("#resNumPopItem_ACCESS_NUMBER_S","",PHONENUM,"stepname:起始号码,outputkey:NULL,group:1")
    csInput("#resNumPopItem_ACCESS_NUMBER_E","",PHONENUM,"stepname:结束号码,outputkey:NULL,group:1")
    time.sleep(1)
    clickElement("//div[@class='submit']/button[@ontap='resNumPopItem.getSelectNum()']","","查询")
    time.sleep(2)
    csClick("#resNumPopItem_numList>li[ontap*='selNum(this)']>div.main>div.title","","号码")
    csClick("#resNumPopItem_SearchArea>div.submit>button.e_button-green","","确定")
    #等待号码预占成功提示_点击确定
    csWait("#wade_messagebox-"+str(i)+"_ct")
    csClick("#wade_messagebox-"+str(i)+"_btns>button[tag='ok']","","确定")
    
def querySimNum(SIM,i=3):
    '''
    选择未使用SIM卡页面
    SIM:SIM卡号
    i:SIM占用提示，显示的确定按钮中的id中数字
    '''
    csWait("#ICC_ID")
    csClick("#ICC_ID","","请输入SIM卡号")
    csInput("#resSimPopItem_ICC_ID_S","",SIM,"stepname:起始SIM号,outputkey:NULL,group:1")
    csInput("#resSimPopItem_ICC_ID_E","",SIM,"stepname:终止SIM号,outputkey:NULL,group:1")
    clickElement("//div[@class='submit']/button[@ontap='resSimPopItem.querySimNum()']","","查询")
    time.sleep(2)
    csClick("#resSimPopItem_simUl>li[ontap*='selSimNum(this)']>div.main","","SIM卡号")
    clickElement("//div[@class='submit']/button[@ontap='resSimPopItem.occupySimNum()']","","确定")
    #等待SIM号预占成功提示_点击确定
    csWait("#wade_messagebox-"+str(i)+"_ct")
    csClick("#wade_messagebox-"+str(i)+"_btns>button[tag='ok']","","确定")
    
def addCustInfo(id='护照',i=4):
    '''
    作用：
    目前适用开户新增客户信息
    id:证件类型
    i:客户信息提交后，显示的确定按钮id中数字
    '''
    csWait("li[ontap*='CustInfoAreaPop']>div[class='more']")
    csClick("li[ontap*='CustInfoAreaPop']>div[class='more']","","客户信息")
    csClick("#IDEN_TYPE_CODE_span","","证件下拉按钮")
    csClick("#IDEN_TYPE_CODE_list_ul>li[title='"+id+"']>div[class='main']","",id)
    csClick("#editInfoButton","","手工输入")
    if id=='身份证':
        AggentInfoPart_ID_NUM=str(makeNewregID())
        party_name='可汗'
    elif id=='护照':
        #护照号码要求6位以上不连续号码
        party_name='ZUOLUO'
        AggentInfoPart_ID_NUM=str(random.randint(0000000,9999999))
    elif id=='单位证件':
        #单位证件，要求长度=15
        AggentInfoPart_ID_NUM=str(random.randint(000000000000000,999999999999999))
    csInput("#PARTY_NAME","",party_name,"stepname:客户名称,outputkey:NULL,group:1")
    csInput("#IDEN_NR","",AggentInfoPart_ID_NUM,"stepname:证件号码,outputkey:NULL,group:1")
    csInput("#IDEN_ADDRESS","","内蒙古呼和浩特市第二中学收发室","stepname:地址,outputkey:NULL,group:1")
    time.sleep(2)
    #如果是护照，需要填写出生日期
    if id=='护照':
        csScrollToElement("#BIRTH_DATE")  
        csClick("#BIRTH_DATE","","出生日期下拉按钮")
        csClick("#birthDate_btn_select","","出生日期")
        csClick("#birthDate_select_y_prev","","年份")
        csClick("#birthDate_select_y_list>li","","2001")
        csClick("#birthDate_select_m_list>li","","1月")
        csClick("#birthDate_btn_ok","","确定")
        time.sleep(2)
    csScrollToElement("#submitButton")
    #填写职业（旧，直接填写）
    #csInput("#PROFESSION","","IT民工","stepname:`,outputkey:NULL,group:1")
    #填写职业（新，目前页面已经变化，已修改）
    csClick("#PROFESSION_span","","职业")
    csClick("#PROFESSION_list_ul>li[title='未知']>div.main","","未知")
    csClick("#OtherInfo>div[class='main']","","其他信息下拉按钮")
    csInput("#CONTACTS_NAME","","易子协","stepname:联系人姓名,outputkey:NULL,group:1")
    csInput("#CONTACTS_PHONE","","15951675079","stepname:联系人电话,outputkey:NULL,group:1")
    csInput("#ADDR_DETAIL_NAME","","内蒙古呼和浩特市第二中学收发室","stepname:收件地址,outputkey:NULL,group:1")
    csInput("#POSTAL_CODE","","224700","stepname:邮政编码,outputkey:NULL,group:1")
    clickElement("//div[@id='CustOtherInfoPart']/div[1]/div[8]/button[@class='e_button-blue e_button-l e_button-r']","","确定")
    csClick("#submitButton","","确定")
    #等待客户信息操作成功！校验提示_点击确定
    csWait("#wade_messagebox-"+str(i)+"_btns>button[tag='ok']")
    csClick("#wade_messagebox-"+str(i)+"_btns>button[tag='ok']","","确定")

    
def addAcctInfo(acct_type=0):
    '''
    目前适用开户新增账户信息
    acct_type=0:账户类型必选，具体请参考页面情况
    acct_type=1:账户类型可选，具体请参考页面情况
    '''
    csClick("#POP_ACCT_ID","","账户信息")
    csInput("#acct_ACCT_NAME","","师和怡","stepname:账户名称,outputkey:NULL,group:1")
    csClick("#acct_ACCT_CLASS_text","","账户级别下拉按钮")
    csClick("#acct_ACCT_CLASS_list_ul>li[title='普通个人帐户']>div","","普通个人帐户")
    if acct_type==0:
        pass
    elif acct_type==1:  
        csClick("#acct_ACCT_TYPE_text","","账户类型下拉按钮")
        csClick("#acct_ACCT_TYPE_list_ul>li[title='预付费账户']>div.main","","预付费账户")
    csClick("#acct_PAY_TYPE_text","","付费方式下拉按钮")
    csClick("#acct_PAY_TYPE_list_ul>li[title='现金']>div","","现金")
    clickElement("//div[@id='editAcctInfoPopupItem']/div[2]/div[1]/div[3]/button[@ontap='confirmAcct();']","","确定")
def addSocreAcct():
    '''
    目前适用开户新增积分信息
    '''
    csClick("li[ontap*='showSocreAcctPop']>div.more","","积分账户信息")
    csInput("#SCORE_SC_ACCT_NAME","","沈英杰","stepname:积分账户名称,outputkey:NULL,group:1")
    csInput("#SCORE_SC_ACCT_PASSWORD","","234512","stepname:密码,outputkey:NULL,group:1")
    clickElement("//div[@id='SCORE_ScorePopupItem']/div[2]/div[1]/div[3]/button[@ontap='SCORE.hiddenScore(this);']","","确定")
def searchOfferkeyWord(keyword,offer='',search_switch=1):    
    csClick("li[ontap='openOffer()']","","套餐")
    if search_switch==1:
        csInput("#searchOfferkeyWord","",keyword,"stepname:套餐搜索栏,outputkey:NULL,group:1")
        csClick("#searchOffersearchButton","","搜索")
        time.sleep(1)
    elif search_switch==0 and offer in ('全球通套餐','IMS固话套餐','4G套餐','不限','动感地带套餐'):
        tmptime=getConfig('TimeOut')
        if offer=='全球通套餐':
            csClick("#li50001001004","",offer)
            time.sleep(5)            
            while tmptime>0:
                 if isEnable("#offerName_100040000555"):
                     csWait("#offerName_100040000555")
                     csClick("#offerName_100040000555","",keyword)
                     break
                 else:
                     #time.sleep(1)
                     csScrollToElement("#navbar1_next")
                     csClick("#navbar1_next","","下一页")
                     tmptime=tmptime-1
                     time.sleep(2)
        elif offer=='IMS固话套餐':
            csClick("#li50001002","",offer)
            time.sleep(3)
            while tmptime>0:
                 if isEnable("#offerName_100040000965"):
                     csWait("#offerName_100040000965")
                     csClick("#offerName_100040000965","",keyword)
                     break
                 else:
                     #time.sleep(1)
                     csScrollToElement("#navbar1_next")
                     csClick("#navbar1_next","","下一页")
                     tmptime=tmptime-1
                     time.sleep(2)
        elif offer=='4G套餐':
            csClick("#li50001001001","",offer)
            time.sleep(3)
            while tmptime>0:
                if isEnable("#offerName_100040000520"):
                    csWait("#offerName_100040000520")
                    csClick("#offerName_100040000520","",keyword)
                    break
                else:
                    csScrollToElement("#navbar1_next")
                    csClick("#navbar1_next","","下一页")
                    tmptime=tmptime-1
                    time.sleep(2)
        elif offer=='不限':
            csClick("#li50001001","",offer)
            time.sleep(3)
            while tmptime>0:
                if isEnable("#offerName_100040000585"):
                    csWait("#offerName_100040000585")
                    csClick("#offerName_100040000585","",keyword)
                    break
                else:
                    csScrollToElement("#navbar1_next")
                    csClick("#navbar1_next","","下一页")
                    tmptime=tmptime-1
                    time.sleep(2)
        elif offer=='动感地带套餐':
            csClick("#li50001001003","",offer)
            time.sleep(3)
            while tmptime>0:
                if isEnable("#offerName_100040000582"):
                    csWait("#offerName_100040000582")
                    csClick("#offerName_100040000582","",keyword)
                    break
                else:
                    csScrollToElement("#navbar1_next")
                    csClick("#navbar1_next","","下一页")
                    tmptime=tmptime-1
                    time.sleep(2)
            

#陈晨-----------------------------------------------------
#变更失效时间
def changeExpireDate(date='次月末日'):
    csClick("#offerExpireDate","","失效时间")
    time.sleep(6)
    csClick("#calendar_btn_quicksel","","快速选择")
    time.sleep(3)
    csWait("#calendar_quicksel_fn")
    clickElement("//*[@id='calendar_quicksel_fn']/ul/li[6]","",date)
    
def selectNum(phonenum=''):
    csClick("#newAccessNumLi>div[class='more']","","选择号码")
    if phonenum:
        csInput("#resNumPopItem_ACCESS_NUMBER_S","",phonenum,"stepname:起始号码,outputkey:NULL,group:1")
        csInput("#resNumPopItem_ACCESS_NUMBER_E","",phonenum,"stepname:结束号码,outputkey:NULL,group:1")
        #clickElement("//div[@class='submit']/button[@ontap='resNumPopItem.getSelectNum()']","","查询")
        csClick(".e_button-blue[ontap='resNumPopItem.getSelectNum()']","","查询")
        time.sleep(3)
        csClick("#resNumPopItem_numList>li[ontap*='selNum(this)']>div.main>div.title","",phonenum)
        if message=='号码选占成功！':
            csClick("#wade_messagebox-"+2+"_btns>button[tag='ok']","","确定")
            csClick("#resNumPopItem>div.c_header>div[ontap='hidePopup(this)']","","选择号码返回")
    else:
        for i in range(2,4):
            j=i-1
            phonenum=getValue_v("//ul[@id='resNumPopItem_numList']/li["+j+"]/div/div[1]","html")
            clickElement("//ul[@id='resNumPopItem_numList']/li["+j+"]/div/div[1]","",phonenum)
            csClick("#resNumPopItem_SearchArea>div>button[ontap='resNumPopItem.occupyAccessNum()']","","确定")
            # csClick("#resNumPopItem_SearchArea>div.submit>button.e_button-green","","确定")
            #等待号码预占成功提示_点击确定
            csWait("#wade_messagebox-"+i)
            message=csValue("#wade_messagebox-"+i+"_ct","html","stepname:号码预占提示信息,outputkey:NULL,group:1")
            if message=='号码选占成功！':
                csClick("#wade_messagebox-"+i+"_btns>button[tag='ok']","","确定")
                csClick("#resNumPopItem>div.c_header>div[ontap='hidePopup(this)']","","选择号码返回")
                break
            else:
                csClick("#wade_messagebox-"+i+"_btns>button[tag='cancel']","","取消")
    return phonenum

def selectSIM(iccid=''):
    csClick("#simResLi","","SIM卡号")
    if iccid:
        csInput("#resSimPopItem_ICC_ID_S","",iccid,"stepname:起始SIM号,outputkey:NULL,group:1")
        csInput("#resSimPopItem_ICC_ID_E","",iccid,"stepname:终止SIM号,outputkey:NULL,group:1")
        clickElement("//div[@class='submit']/button[@ontap='resSimPopItem.querySimNum()']","","查询")
        time.sleep(2)
        csClick("#resSimPopItem_simUl>li[ontap*='selSimNum(this)']>div.main","","SIM卡号")
        #等待SIM号预占成功提示_点击确定
        message=csValue("#wade_messagebox-3_ct","html","stepname:预占sim卡结果,outputkey:NULL,group:1")
        if message=='SIM卡选占成功！':
            csClick("#wade_messagebox-3_btns>button[tag='ok']","","确定")
            csClick("#resSimPopItem>div>div.back")
    else:
        for i in range(3,5):
            j=i-2
            iccid=getValue("//div[@id='resSimPopItem_QryResultPart']/div/div/div/ul/li["+i+"]","iccid","stepname:iccid,outputkey:NULL,group:1")
            print iccid
            clickElement("//div[@id='resSimPopItem_QryResultPart']/div/div/div/ul/li["+i+"]","",iccid)
            csClick("#resSimPopItem_SearchArea>div.submit>button","","确定")
            #等待SIM号预占成功提示_点击确定
            message=csValue("#wade_messagebox-"+i+"_ct","html","stepname:预占sim卡结果,outputkey:NULL,group:1")
            if message=='SIM卡选占成功！':
                csClick("#wade_messagebox-"+i+"_btns>button[tag='ok']","","确定")
                csClick("#resSimPopItem>div>div.back")
                break
            else:
                csClick("#wade_messagebox-"+i+"_btns>button[tag='cancel']","","取消")
    return iccid
