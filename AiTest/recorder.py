#-*-coding:utf-8-*-
from PackFunction import *

from Tkinter import *
import tkMessageBox
top = Tk()
var = StringVar()
sTag=False

def _getScripts():
    global rWD,sTag
    while True:
        if sTag==True and rWD!=None:
            if rWD.current_url!='res://ieframe.dll/navcancl.htm':
                rWD.switch_to_default_content()
                #print 'get script run'
                ss=rWD.execute_script("if(document.rCode && document.rCode!=''){var rCode=document.rCode;document.rCode='';return rCode;}else{return ''}")
                if ss!='':
                    txt.insert(END,ss)
        time.sleep(1)

#add monitor for record
def callbtn1():
    global sTag
    btn1.configure(state=DISABLED)
    btn2.configure(state=NORMAL)
    jsListener2='''
if (!window.addMonitor){
    function addMonitor(vWindow){
        if (vWindow.document.documentMode>7 && !vWindow.document.querySelector('script[tag="monitor"]')){
            var jss = vWindow.document.createElement('script');
            jss.setAttribute('tag', 'monitor');
            vWindow.document.getElementsByTagName('head')[0].appendChild(jss);
            var ts='function getCssPath(targ,iStr){var tstr="";var tmpS="";if(targ.tagName==="BODY"){return "body"}if(targ.getAttribute("id")){tstr="#"+targ.getAttribute("id");if(iStr!=""){tstr=tstr+">"+iStr}return tstr}if(targ.getAttribute("class")){tstr=tstr+targ.getAttribute("class").replace(/\\\\s+/g,".");tstr=targ.tagName.toLowerCase()+"."+tstr;if(tstr.substr(tstr.length-1,tstr.length)==="."){tstr=tstr.substr(0,tstr.length-1);};iStr===""?tmpS=tstr:tmpS=tstr+">"+iStr;if(document.querySelectorAll(tmpS).length===1){return tmpS}}var tarray=["name","value","title","href"];for(var j in tarray){if(targ.getAttribute(tarray[j])){tstr=tstr+"["+tarray[j]+"=\\'"+targ.getAttribute(tarray[j])+"\\']"}}if(tstr===""){tstr=targ.tagName.toLowerCase()}iStr===""?tmpS=tstr:tmpS=tstr+">"+iStr;if(tmpS.length>0 && document.querySelectorAll(tmpS).length===1){return tmpS};var p1=targ.parentNode;if(p1.tagName!="BODY"){tstr=getCssPath(p1,tmpS);if(iStr==="" && document.querySelectorAll(tstr).length>1){for(var i=0;i<targ.attributes.length;i++){if("name,value,title,href,id,class,style".indexOf(targ.attributes[i].name)===-1 && targ.attributes[i].name.length<18){tstr=tstr+"["+targ.attributes[i].name+"=\\'"+targ.attributes[i].value+"\\']"}}}}else{tstr=tmpS;if(document.querySelectorAll(tstr).length>2){tstr="BODY>"+tstr;}}return tstr;}';
            ts+='function recordForInput(){var e=window.event||event;var te=e.target||e.srcElement;if(te.inputable!=undefined){if(te.inputable==te.value){return}var tStr=getCssPath(te,"");if(tStr.indexOf("BODY>")>0){tStr="csInput(\\\\""+tStr+"\\\\",\\\\""+te.value+"\\\\") #element>2"}else{tStr="csInput(\\\\""+tStr+"\\\\",\\\\""+te.value+"\\\\")";}var recDoc=window.top.document;recDoc.rCode=recDoc.rCode+"|"+tStr;te.removeAttribute("inputable");te.detachEvent("onblur",recordForInput);}};';
            ts+='function recordForSelect(){var e = window.event || event;var te = e.target || e.srcElement;var tStr=te.selectable+">option[value=\\'"+te.value+"\\']";te.selectable=false;te.detachEvent("onmouseup",recordForSelect);window.top.document.rTmpCode="csClick(\\\\""+tStr+"\\\\")";setTimeout("window.top.document.rCode+=window.top.document.rTmpCode;",50);};';
            ts+='function recordForClick(){var e=window.event||event;var te=e.target||e.srcElement;var tStr=getCssPath(te,"");var tStr2=tStr;if(tStr.indexOf("BODY>")>0){tStr="csClick(\\\\""+tStr+"\\\\") #element>2"}else{tStr="csClick(\\\\""+tStr+"\\\\")";}if((te.tagName=="INPUT" && (te.type=="text" || te.type=="password")) || te.tagName=="TEXTAREA"){te.inputable=te.value;te.attachEvent("onblur",recordForInput);}if(te.tagName=="SELECT" && tStr.indexOf("##>2")<0){if(!te.selectable){te.selectable=true;}else{te.selectable=tStr2;te.attachEvent("onmouseup",recordForSelect);}return;}var recDoc=window.top.document;recDoc.rTmpCode="|"+tStr;setTimeout("window.top.document.rCode+=window.top.document.rTmpCode;",50);};';
            vWindow.document.querySelector('script[tag="monitor"]').text=ts;
            if (vWindow===window.top){document.rCode='';document.rTmpCode='';}
        }
        if(vWindow.document.documentMode>7){vWindow.document.body.attachEvent("onmousedown",vWindow.recordForClick);}
        if (vWindow.frames.length>0){
            for (var i=0;i<vWindow.frames.length;i++){
                addMonitor(vWindow.frames[i]);
            }
        }
    }
}
document.rCode='';
//document.recPid=setInterval("addMonitor(window.top)",3000);
addMonitor(window);
'''
    #���д��ڶ�������js
    switchWindow()
    vTitle=[]
    getTitles(vTitle)
    for i in vTitle:
        switchWindow(i.encode('utf-8'))
        switchFrame()
        exeJs_v(jsListener2)
    sTag=True

#stop record and get scripts
def callbtn2():
    btn2.configure(state=DISABLED)
    btn1.configure(state=NORMAL)
    #cancel monitor
    global sTag
    jsListener2='''
if (!window.palMonitor){
    function palMonitor(vWindow){
        if(vWindow.document.documentMode>7){
            if(vWindow.recordForClick){
                vWindow.document.body.detachEvent("onmousedown",vWindow.recordForClick);
            }
        }
        for (var i=0;i<vWindow.frames.length;i++){
            if(vWindow.frames[i].document.documentMode>7 ){
                palMonitor(vWindow.frames[i]);
            }
        }
        return window.top.document.rCode;
    }
}
return palMonitor(window);
'''
    vTitle=[]
    switchWindow()
    getTitles(vTitle)
    for i in vTitle:
        switchWindow(i.encode('utf-8'))
        switchFrame()
        r1=exeJs_v(jsListener2)
        r1=r1.replace("|","\n")+"\n"
        txt.insert(END,r1)
    sTag=False

#start IE
def callbtn3():
    #change btn state
    btn3.configure(state=DISABLED)
    btn1.configure(state=NORMAL)
    btn4.configure(state=NORMAL)
    btn5.configure(state=NORMAL)
    #start selenium
    openUrl('about:bank')
    tmpS=entry1.get()
    if entry1.get()!='' and os.path.exists(tmpS):
        execfile(tmpS)

#end process
def callbtn4():
    pass

#run script
def callbtn5():
    script=txt2.get('0.0',END).strip()
    exec(script)

#shutdown process
def closeMe():
    print 'close ok'
    wd=getDriver()
    if wd!=None:
        if wd.current_url=='res://ieframe.dll/navcancl.htm':
            wd.quit()
        else:
            closeUrl()
    top.quit()

#��ȡ������Ϊ���·��
rPath=sys.path[0]
if 'library.zip' in rPath:
    rPath=rPath[0:-12]
else:
    rPath=rPath+'\\dist'
print rPath
initConfig(rPath)  #�������������ȡ����
os.system("taskkill -f /im IEDriverServer.exe")

top.geometry('700x500')
top.resizable(width=True, height=False)
#title
frame1=Frame(top)
frame1.pack()
label1=Label(frame1,textvariable=var)
var.set("---recorder for selenium---")
label1.pack()
#buttons
frame2=Frame(top)
frame2.pack()
btn1=Button(frame2,text="record",width=10,state=DISABLED,command=callbtn1)
btn1.grid(row=0,column=1)
btn2=Button(frame2,text="pause",width=10,state=DISABLED,command=callbtn2)
btn2.grid(row=0,column=2)
btn3=Button(frame2,text="startIE",width=10,command=callbtn3)
btn3.grid(row=0,column=0)
btn4=Button(frame2,text="end",width=10,state=DISABLED,command=callbtn4)
btn4.grid(row=0,column=4)

#text result
tmpStr=''
if os.path.exists('rm.txt'):
    with open ('rm.txt','rb') as f1:
        tf1=f1.readlines()
        if len(tf1)>0:
            tmpStr=tf1[0].strip()
frame3=Frame(top)
frame3.pack()
label2=Label(frame3, text="script auto run after start IE:")
label2.pack(side=LEFT)
entry1=Entry(frame3,width=50)
entry1.pack(side=RIGHT)
if tmpStr!='':
    entry1.insert(0,tmpStr)
txt=Text(height=20,width=80)
txt.pack(expand=YES, fill='both')

frame4=Frame(top)
frame4.pack()
label3=Label(frame4, text="console:")
label3.pack(side=LEFT)
btn5=Button(frame4,text="Run",width=10,command=callbtn5)
btn5.pack(side=LEFT)
txt2=Text(height=20,width=40)
txt2.pack(expand=YES, fill='both')
#sb=Scrollbar(frame3,orient='horizontal')
#sb.grid(row=1, column=0,sticky='ew')
#txt.configure(xscrollcommand=sb.set)
#sb.configure(command=txt.xview)

#click x btn
top.protocol("WM_DELETE_WINDOW",closeMe)

# t1=threading.Thread(target=_getScripts,name="getScript")
# t1.setDaemon(True)
# t1.start()

top.mainloop()
tmpStr=entry1.get()
with open ('rm.txt','wb') as f1:
    f1.write(tmpStr)
print 'haha'
