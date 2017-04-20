# -*-coding:utf-8-*-
import ConfigParser
import logging
from email.header import Header
from email.utils import parseaddr, formataddr
import os
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='./logs/log',
                filemode='w')
CONFIG = {}


class myconf(ConfigParser.ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


def initConfig2(inPath):
    global CONFIG
    tmpPath = inPath + '\\config.txt'
    with open(tmpPath, 'rb') as f2:
        for line in f2.readlines():
            if len(line.strip()) > 0:
                print line.strip()[0]
                if line.strip()[0] != "[":
                    print "111111111111111111"
                    tmpV = line.strip().split('=')
                    print tmpV
                    CONFIG[tmpV[0]] = tmpV[1]
    CONFIG['path'] = inPath  # 锟斤拷�?�锟斤拷锟斤�?
    CONFIG['curFrames'] = []
    CONFIG['curCaseFile'] = ''
    for (d, v) in CONFIG.items():
        try:
            CONFIG[d] = int(v)
        except:
            pass


def format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def initConfig(inPath):
    logging.info(inPath)
    global CONFIG
    tmpPath = inPath + '\\config.ini'
    cf = myconf()
    cf.read(tmpPath)
    for i in cf.sections():
        datas = cf.items(i)
        for tmpV in datas:
            CONFIG[tmpV[0]] = tmpV[1]
    CONFIG['path'] = inPath 
    CONFIG['curFrames'] = []
    CONFIG['curCaseFile'] = ''
    for (d, v) in CONFIG.items():
        try:
            CONFIG[d] = int(v)
        except:
            pass

    tmpPath = CONFIG['ora_path'] + '\\oraocci11.dll'
    if os.path.exists(tmpPath):
        print 'cx_Oracle add success!'
        #logging.info(os.environ)
        os.environ['PATH'] = CONFIG['ora_path'] + ';'+CONFIG['ora_path'] + '\\bin;' + os.environ['PATH']
        os.environ['TNS_ADMIN'] = CONFIG['ora_path']
        os.environ['ORACLE_HOME'] = CONFIG['ora_path']
        os.environ['NLA_LANG'] = "SIMPLIFIED CHINESE_CHINA.UTF8"
        # os.environ['NLA_LANG']="SIMPLIFIED CHINESE_CHINA.ZHS16GBK"
        # time.sleep(1)
        #logging.info(os.environ)
        import cx_Oracle
    else:
        print 'cx_Oracle not added'

#initConfig("./")
