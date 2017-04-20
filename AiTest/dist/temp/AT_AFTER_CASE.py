#-*-coding:utf-8-*-
#run after each case
logging.info('run after case begin...')
#检查测试结束后是否有多余tab页
#setOutput(getConfig('curCaseFile'))
RunTag=1

if RunTag==1:
    #关掉分页避免后续运行出错
    switchFrame()
    try:
        tabCount=exeJs_v("return document.querySelectorAll('#tab_ct_ul>li').length")
    except:
        #由于页面刷新有bug，先不用
        #refresh()
        #time.sleep(3)
        tabCount=exeJs_v("return document.querySelectorAll('#tab_ct_ul>li').length")
    print "***********all opened "+str(tabCount)+" tabs,and now begin close.***********"
    if tabCount>0:
        for i in range(tabCount):
            time.sleep(2)
            j=str(tabCount-i)
            csWait("#tab_ct_ul")
            #clickElement("//ul[@id='tab_ct_ul']/li["+j+"]/div[2]/div[2]","","关闭第"+j+"层分页")
            clickElement_v("//ul[@id='tab_ct_ul']/li["+j+"]/div[1]")
            clickElement_v("//ul[@id='tab_ct_ul']/li["+j+"]/div[2]/div[2]")
            time.sleep(1)
            
logging.info('run after case end...')


'''
#关闭所有分页
for i in range(1,5):
    i=str(i)   
    if isEnable("div[id^='navtab_close']"): 
        try: 
            clickElement("//ul[@id='tab_ct_ul']/li[last]/div[2]/div[2]","","关闭第"+i+"层分页")    
        except Exception,e:
            print e
    else:
        switchFrame()
        if isEnable("div[id^='navtab_close']"): 
            try:
                clickElement("//ul[@id='tab_ct_ul']/li[last]/div[2]/div[2]","","关闭第"+i+"层分页")
            except Exception,e:
                print e  
        else:    
            break
'''   
