# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frame3.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import re
import threading

from PyQt4 import QtCore, QtGui

from AiTest import socketClient
from DataDrawout import DataDrawout
from exebat import startExec, verExec, reportExec

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Autotest(QtGui.QWidget):
    def setupUi(self, Autotest):
        Autotest.setObjectName(_fromUtf8("Autotest"))
        Autotest.resize(471, 640)
        self.centralwidget = QtGui.QWidget(Autotest)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_data = QtGui.QWidget()
        self.tab_data.setObjectName(_fromUtf8("tab_data"))
        self.Button_getdata = QtGui.QPushButton(self.tab_data)
        self.Button_getdata.setGeometry(QtCore.QRect(160, 270, 101, 41))
        self.Button_getdata.setObjectName(_fromUtf8("Button_getdata"))
        self.label_4 = QtGui.QLabel(self.tab_data)
        self.label_4.setGeometry(QtCore.QRect(50, 66, 71, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.textEdit_4 = QtGui.QLineEdit(self.tab_data)
        self.textEdit_4.setGeometry(QtCore.QRect(126, 63, 256, 31))
        self.textEdit_4.setObjectName(_fromUtf8("textEdit_4"))
        self.radioButton_3 = QtGui.QRadioButton(self.tab_data)
        self.radioButton_3.setGeometry(QtCore.QRect(31, 36, 131, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.radioButton_4 = QtGui.QRadioButton(self.tab_data)
        self.radioButton_4.setGeometry(QtCore.QRect(31, 125, 171, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName(_fromUtf8("radioButton_4"))
        self.label_5 = QtGui.QLabel(self.tab_data)
        self.label_5.setGeometry(QtCore.QRect(50, 165, 71, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.textEdit_5 = QtGui.QLineEdit(self.tab_data)
        self.textEdit_5.setGeometry(QtCore.QRect(126, 162, 256, 31))
        self.textEdit_5.setObjectName(_fromUtf8("textEdit_5"))
        self.tabWidget.addTab(self.tab_data, _fromUtf8(""))
        self.tab_exec = QtGui.QWidget()
        self.tab_exec.setObjectName(_fromUtf8("tab_exec"))
        self.Button_exec = QtGui.QPushButton(self.tab_exec)
        self.Button_exec.setGeometry(QtCore.QRect(70, 270, 101, 41))
        self.Button_exec.setObjectName(_fromUtf8("Button_exec"))
        self.radioButton = QtGui.QRadioButton(self.tab_exec)
        self.radioButton.setGeometry(QtCore.QRect(40, 30, 89, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.tab_exec)
        self.radioButton_2.setGeometry(QtCore.QRect(40, 140, 89, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.label = QtGui.QLabel(self.tab_exec)
        self.label.setGeometry(QtCore.QRect(50, 62, 91, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.tab_exec)
        self.label_2.setGeometry(QtCore.QRect(50, 102, 91, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.tab_exec)
        self.label_3.setGeometry(QtCore.QRect(50, 170, 101, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.textEdit = QtGui.QLineEdit(self.tab_exec)
        self.textEdit.setGeometry(QtCore.QRect(150, 60, 231, 31))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit_2 = QtGui.QLineEdit(self.tab_exec)
        self.textEdit_2.setGeometry(QtCore.QRect(150, 100, 231, 31))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.textEdit_3 = QtGui.QLineEdit(self.tab_exec)
        self.textEdit_3.setEnabled(False)
        self.textEdit_3.setGeometry(QtCore.QRect(150, 170, 231, 31))
        self.textEdit_3.setObjectName(_fromUtf8("textEdit_3"))
        self.Button_exec_2 = QtGui.QPushButton(self.tab_exec)
        self.Button_exec_2.setGeometry(QtCore.QRect(240, 270, 101, 41))
        self.Button_exec_2.setObjectName(_fromUtf8("Button_exec_2"))
        self.label_11 = QtGui.QLabel(self.tab_exec)
        self.label_11.setGeometry(QtCore.QRect(50, 212, 91, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.textEdit_9 = QtGui.QLineEdit(self.tab_exec)
        self.textEdit_9.setGeometry(QtCore.QRect(150, 210, 231, 31))
        self.textEdit_9.setObjectName(_fromUtf8("textEdit_9"))
        self.tabWidget.addTab(self.tab_exec, _fromUtf8(""))
        self.tab_ver = QtGui.QWidget()
        self.tab_ver.setObjectName(_fromUtf8("tab_ver"))
        self.Button_ver = QtGui.QPushButton(self.tab_ver)
        self.Button_ver.setGeometry(QtCore.QRect(160, 260, 101, 41))
        self.Button_ver.setObjectName(_fromUtf8("Button_ver"))
        self.label_6 = QtGui.QLabel(self.tab_ver)
        self.label_6.setGeometry(QtCore.QRect(31, 58, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.tab_ver)
        self.label_7.setGeometry(QtCore.QRect(31, 120, 81, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.textEdit_6 = QtGui.QLineEdit(self.tab_ver)
        self.textEdit_6.setGeometry(QtCore.QRect(130, 58, 301, 31))
        self.textEdit_6.setObjectName(_fromUtf8("textEdit_6"))
        self.textEdit_7 = QtGui.QLineEdit(self.tab_ver)
        self.textEdit_7.setGeometry(QtCore.QRect(131, 120, 301, 31))
        self.textEdit_7.setObjectName(_fromUtf8("textEdit_7"))
        self.label_9 = QtGui.QLabel(self.tab_ver)
        self.label_9.setGeometry(QtCore.QRect(160, 150, 201, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.tabWidget.addTab(self.tab_ver, _fromUtf8(""))
        self.tab_report = QtGui.QWidget()
        self.tab_report.setObjectName(_fromUtf8("tab_report"))
        self.Button_report = QtGui.QPushButton(self.tab_report)
        self.Button_report.setGeometry(QtCore.QRect(160, 250, 101, 41))
        self.Button_report.setObjectName(_fromUtf8("Button_report"))
        self.label_8 = QtGui.QLabel(self.tab_report)
        self.label_8.setGeometry(QtCore.QRect(20, 100, 71, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("SimSun-ExtB"))
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.textEdit_8 = QtGui.QLineEdit(self.tab_report)
        self.textEdit_8.setGeometry(QtCore.QRect(110, 100, 291, 31))
        self.textEdit_8.setObjectName(_fromUtf8("textEdit_8"))
        self.tabWidget.addTab(self.tab_report, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 0, 0, 1, 1)
        Autotest.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Autotest)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Autotest.setStatusBar(self.statusbar)

        self.retranslateUi(Autotest)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),
                               self.textEdit_3.setEnabled)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.textEdit_3.setDisabled)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.textEdit_9.setEnabled)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),
                               self.textEdit_9.setDisabled)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.textEdit.setEnabled)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.textEdit_2.setEnabled)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),
                               self.textEdit_2.setDisabled)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.textEdit.setDisabled)
        QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),
                               self.textEdit_5.setDisabled)
        QtCore.QObject.connect(self.radioButton_4, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),
                               self.textEdit_4.setDisabled)
        QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),
                               self.textEdit_4.setEnabled)
        QtCore.QObject.connect(self.radioButton_4, QtCore.SIGNAL(_fromUtf8("clicked(bool)")),
                               self.textEdit_5.setEnabled)
        QtCore.QObject.connect(self.Button_exec, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ButtonExec)
        QtCore.QObject.connect(self.Button_exec_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.StartServer)
        QtCore.QObject.connect(self.Button_getdata, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ButtonGetData)
        QtCore.QObject.connect(self.Button_ver, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ButtonVer)
        QtCore.QObject.connect(self.Button_report, QtCore.SIGNAL(_fromUtf8("clicked()")), self.ButtonReport)
        QtCore.QMetaObject.connectSlotsByName(Autotest)
        Autotest.setTabOrder(self.Button_getdata, self.Button_exec)
        Autotest.setTabOrder(self.Button_exec, self.Button_ver)
        Autotest.setTabOrder(self.Button_ver, self.Button_report)

    def retranslateUi(self, Autotest):
        Autotest.setWindowTitle(_translate("Autotest", "MainWindow", None))
        self.label_10.setText(_translate("Autotest", "脚本路径/远程IP地址：", None))
        self.Button_getdata.setText(_translate("Autotest", "抽取数据", None))
        self.label_4.setText(_translate("Autotest", "Plan ID:", None))
        self.radioButton_3.setText(_translate("Autotest", "按计划捞取数据", None))
        self.radioButton_4.setText(_translate("Autotest", "按用例捞取数据", None))
        self.label_5.setText(_translate("Autotest", "Case ID:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_data), _translate("Autotest", "数据抽取", None))
        self.Button_exec.setText(_translate("Autotest", "开始执行", None))
        self.radioButton.setText(_translate("Autotest", "执行测试", None))
        self.radioButton_2.setText(_translate("Autotest", "重执行", None))
        self.label.setText(_translate("Autotest", "Plan ID:", None))
        self.label_2.setText(_translate("Autotest", "Group ID:", None))
        self.label_3.setText(_translate("Autotest", "Plan Batch ID:", None))
        self.Button_exec_2.setText(_translate("Autotest", "启动本地代理", None))
        self.label_11.setText(_translate("Autotest", "Group ID:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_exec), _translate("Autotest", "执行用例", None))
        self.Button_ver.setText(_translate("Autotest", "后台验证", None))
        self.label_6.setText(_translate("Autotest", "Plan Batch ID:", None))
        self.label_7.setText(_translate("Autotest", "Batch ID:", None))
        self.label_9.setText(_translate("Autotest", "Batch ID为空，默认全部执行", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ver), _translate("Autotest", "后台验证", None))
        self.Button_report.setText(_translate("Autotest", "生成报告", None))
        self.label_8.setText(_translate("Autotest", "Batch ID:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_report), _translate("Autotest", "生成报告", None))

    def StartServer(self):
        """
        启动
        :return:
        """
        startExec()
        return

    def ButtonExec(self):
        """
        执行，post方式，非线程
        :return:
        """
        ipaddr=unicode(self.lineEdit.text())
        planid = unicode(self.textEdit.text())
        groupid1 = unicode(self.textEdit_2.text())
        groupid2 = unicode(self.textEdit_9.text())
        pre_planbatchid = unicode(self.textEdit_3.text())
        if self.radioButton.isChecked():
            pre_planbatchid = ""
            groupid=groupid1
        elif self.radioButton_2.isChecked():
            planid = ""
            groupid =groupid2
        else:
            print "please checked the radio Button"
            return False
        print type(planid), type(groupid), type(pre_planbatchid)
        print ipaddr
        #验证IP地址，地址不正确则执行本地
        if re.match(r"^\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*$", ipaddr):
            print 'param:planid, groupid, pre_planbatchid,ipaddr'
            socketClient.client(planid, groupid, pre_planbatchid,ipaddr)
        else:
            print 'param:planid, groupid, pre_planbatchid'
            print "IP address is null or error"
            socketClient.client(planid, groupid, pre_planbatchid)
        # startExec()

    def ButtonGetData(self):
        """
        数据捞取，调用api方式，非线程
        :return:
        """
        button=QtGui.QMessageBox.question(self, 'Message', u'数据抽取需较长时间，请耐心等待\n抽取进度可查看log日志文件\n点击确定开始抽取', QtGui.QMessageBox.Ok , QtGui.QMessageBox.No)
        if button == QtGui.QMessageBox.Ok:
            doGet = DataDrawout()
            planid = str(self.textEdit_4.text())
            caseid = str(self.textEdit_5.text())
            path = str(self.lineEdit.text())
            if self.radioButton_3.isChecked():
                doGet.drawoutData('plan', planid)
            elif self.radioButton_4.isChecked():
                doGet.drawoutData('case', caseid)
        elif button == QtGui.QMessageBox.Cancel:
            return False
        else:
            return False

    def ButtonVer(self):
        """
        后台校验，执行命令行方式，线程
        :return:
        """
        planbatchid = str(self.textEdit_6.text())
        batchid = str(self.textEdit_7.text())
        path = str(self.lineEdit.text())
        print batchid
        if batchid =="":
            batchid = "all"
        ExecVer = threading.Thread(target=verExec, args=(path, planbatchid, batchid))
        ExecVer.setDaemon(False)
        ExecVer.start()

    def ButtonReport(self):
        """
        报告，执行命令行方式，线程
        :return:
        """
        batchid = str(self.textEdit_8.text())
        path = str(self.lineEdit.text())
        print batchid, path
        ExecReport = threading.Thread(target=reportExec, args=(path, batchid))
        ExecReport.setDaemon(False)
        ExecReport.start()


class SecondWindow(QtGui.QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(100, 150)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(90, 90, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 10, 201, 61))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton.setText(_translate("Dialog", "确定", None))
        self.label.setText(_translate("Dialog", "抽取数据时间较长请耐心等待。。。", None))

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    Autotest = QtGui.QMainWindow()
    ui = Ui_Autotest()
    ui.setupUi(Autotest)
    Autotest.show()
    sys.exit(app.exec_())
