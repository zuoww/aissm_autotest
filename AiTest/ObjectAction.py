#-*-coding:utf-8-*-
from  PackFunction import *
from  StepReport import *



def csInput(inObj, checkType, inTxt, inActionMsg):
    """
    WEB操作，文本框输入
    :param inObj:对象
    :param checkType:检查点
    :param inTxt:输入内容
    :param inActionMsg:步骤信息
    :return:
    """
    # 解析当前步骤的配置信息
    vCfg = StepReport.AI_GetStepConfig(inActionMsg)
    # 步骤输出开始
    StepReport.AI_PrintAtStepBegin("在[" + vCfg["stepname"] + "]中输入[" + inTxt + "]")
    # self.RegistObservers()
    #self.setSubjectState(inObj)  # 对象
    # Notify()
    csInput_v(inObj, inTxt)
    # inputVal = csInput(inObj, inTxt)
    inputVal=inTxt
    # 步骤输出结束
    StepReport.AI_PrintAtStepEnd_E("输入[" + inputVal + "]")

    # 将值加入到输出列表中
    # DataPool.AI_SetOutputData(vCfg.get("outputkey"), inputVal, vCfg.get("group"))
    return inputVal

def inputText(inObj, checkType, inTxt, inActionMsg):
    """
    WEB操作，文本框输入
    :param inObj:对象
    :param checkType:检查点
    :param inTxt:输入内容
    :param inActionMsg:步骤信息
    :return:
    """
    # 解析当前步骤的配置信息
    vCfg = StepReport.AI_GetStepConfig(inActionMsg)
    # 步骤输出开始
    StepReport.AI_PrintAtStepBegin("在[" + vCfg["stepname"] + "]中输入[" + inTxt + "]")
    # self.RegistObservers()
    #self.setSubjectState(inObj)  # 对象
    # Notify()
    inputText_v(inObj, inTxt)
    # inputVal = csInput(inObj, inTxt)
    inputVal=inTxt
    # 步骤输出结束
    StepReport.AI_PrintAtStepEnd_E("输入[" + inputVal + "]")

    # 将值加入到输出列表中
    # DataPool.AI_SetOutputData(vCfg.get("outputkey"), inputVal, vCfg.get("group"))
    return inputVal

def csClick(inObj, checkType, inActionMsg, Keystr=''):
    """
    /**
     * 点击 按钮、link、其他需要点击的对象,同时整合报告输出
     *
     * @param inObj
     *            对象
     * @param inActionMsg
     *            说明，用于打印输出,这里为对象的名称
     * @return 1 or 0
    */
    """
    # 步骤输出开始
    StepReport.AI_PrintAtStepBegin("点击[" + inActionMsg + "]")
    # self.RegistObservers()
    #self.setSubjectState(inObj)  # 对象
    # Notify()
    csClick_v(inObj, Keystr)
    # 步骤输出结束
    StepReport.AI_PrintAtStepEnd_E("成功点击[" + inActionMsg  + "]")

    # 将值加入到输出列表中
    # DataPool.AI_SetOutputData(vCfg.get("outputkey"), inputVal, vCfg.get("group"))
    return 1

def clickElement(inObj, checkType, inActionMsg):
    # 步骤输出开始
    StepReport.AI_PrintAtStepBegin("点击[" + inActionMsg + "]")

    clickElement_v(inObj)
    # 步骤输出结束
    StepReport.AI_PrintAtStepEnd_E("成功点击[" + inActionMsg  + "]")

    # self.RegistObservers()
    #self.setSubjectState(inObj)  # 对象
    # Notify()
    return 1

def csValue(inObj, inAttrName, inActionMsg,InV=[]):
    """
    /**
     * 返回对象指定的属性值
     *
     * @param inObj
     *            对象
     * @param inAttrName
     *            属性名
     * @param inActionMsg
     *            说明，用于打印输出,这里: 对象的名称;分组;输出关键字 或则 "NULL" "1:2,3:4"
     * @return 返回对象的属性值
     * @author wangsq
     */
     """
    if (inActionMsg !="NULL" and inActionMsg !=""):
        # 解析当前步骤的配置信息
        vCfg = StepReport.AI_GetStepConfig(inActionMsg)
        # 步骤输出开始
        StepReport.AI_PrintAtStepBegin("得到[" + vCfg["stepname"]+"]的[" + inAttrName + "]属性值")
        #执行
        attrVal=csValue_v(inObj,inAttrName,InV)
        #步骤输出结束
        StepReport.AI_PrintAtStepEnd_E("得到的属性值为[" + attrVal + "]")
        #将值加入到输出列表中
        #DataPool.AI_SetOutputData(vCfg.get("outputkey"), attrVal, Integer.parseInt(vCfg.get("group")))
    else:
        attrVal=csValue_v(inObj,inAttrName,InV)
    return attrVal

def getValue(inObj, inAttrName, inActionMsg, InV=[]):
    """
    /**
     * 返回对象指定的属性值
     *
     * @param inObj
     *            对象
     * @param inAttrName
     *            属性名
     * @param inActionMsg
     *            说明，用于打印输出,这里: 对象的名称;分组;输出关键字 或则 "NULL" "1:2,3:4"
     * @return 返回对象的属性值
     * @author wangsq
     */
     """
    if (inActionMsg != "NULL" and inActionMsg !=""):
        # 解析当前步骤的配置信息
        vCfg = StepReport.AI_GetStepConfig(inActionMsg)
        # 步骤输出开始
        StepReport.AI_PrintAtStepBegin("得到[" + vCfg["stepname"]+"]的[" + inAttrName + "]属性值")
        #执行
        attrVal=getValue_v(inObj,inAttrName,InV)
        #步骤输出结束
        StepReport.AI_PrintAtStepEnd_E("得到的属性值为[" + attrVal + "]")
        #将值加入到输出列表中
        #DataPool.AI_SetOutputData(vCfg.get("outputkey"), attrVal, Integer.parseInt(vCfg.get("group")))
    else:
        attrVal=getValue_v(inObj,inAttrName,InV)
    return attrVal

def exeJs(inScript,inActionMsg="",inV=[],fpath=""):
    if inActionMsg!="":
        # 步骤输出开始
        StepReport.AI_PrintAtStepBegin("[" + inActionMsg + "]")

        exeJs_v(inScript,inV=[],fpath="")
    
        # 步骤输出结束
        StepReport.AI_PrintAtStepEnd_E("成功[" + inActionMsg  + "]")

    else:
        exeJs_v(inScript,inV=[],fpath="")
    return 1

def setConfig(ParamName,inputStr):
    #setConfig_v(ParamName, inputStr)
    if ParamName=="CaseStatus":
        if inputStr=="fail":
            StepReport.AI_PrintAtStepBegin("开始判断该用例执行结果状态")
            CONFIG["CaseStatus"]="fail"
            StepReport.AI_PrintAtStepEnd_E("该用例执行结果判断为<失败>")
        if inputStr=="break":
            CONFIG["CaseStatus"]="fail"
            CONFIG["output"]="-break"+CONFIG["output"]
            logging.warn("CaseStatus is break,exit!")
            endCase(CONFIG["CaseNumber"],1)
            closeUrl()
            raise SystemExit
    if ParamName=="ConStr":
        CONFIG["ConStr"]=inputStr
        
        
def makeNewregID(province=45, city=01, district=03):
    """
            随机生成新的18为身份证号码
   :param province:省代码
   :param city:市代码
   :param district:区县代码
   :return:18位身份证号
    """
    ARR = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)  # 校验权重
    LAST = ('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2')
    t = time.localtime()[0]
    # 450103 199001012062
    x = '%02d%02d%02d%04d%02d%02d%03d' % (province,
                                         city,
                                         district,
                                         random.randint(t - 25, t - 18),
                                         random.randint(1, 12),
                                         random.randint(1, 28),
                                         random.randint(1, 999))
    y = 0
    for i in range(17):
        y += int(x[i]) * ARR[i]
    print '%s%s' % (x, LAST[y % 11])
    return '%s%s' % (x, LAST[y % 11])

def decipher(inputString):
    """
    密码解密
    :param inputString: 整数字符串
    :return:
    """
    result = []
    nOffSet = int(inputString[0:2], 16)
    nKeyIndex = 0
    tmpRange = [x for x in range(2, len(inputString)) if x % 2 == 1]
    for i in tmpRange:
        nBaseChar = int(inputString[i - 1:i + 1], 16)
        nBitKey = int(ord('Tom Lee'[nKeyIndex]))
        nCodeChar = nBaseChar ^ nBitKey
        if nCodeChar <= nOffSet:
            nCodeChar = 255 + nCodeChar - nOffSet
        else:
            nCodeChar -= nOffSet
        result.append(chr(nCodeChar))
        nOffSet = nBaseChar
        if nKeyIndex >= len('Tom Lee'):
            nKeyIndex = 0
        else:
            nKeyIndex += 1
    return ''.join(result)


           
        
makeNewregID()



