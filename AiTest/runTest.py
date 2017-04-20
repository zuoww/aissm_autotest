#-*-coding:utf-8-*-
import sys
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect(('127.0.0.1', 1414))
    if len(sys.argv)==1:
        s.send("GET /test HTTP/1.1\r\nHost: 127.0.0.1:1414\r\nConnection: close\r\n\r\n")
    elif len(sys.argv)==2 and sys.argv[1]=="stop":
        s.send("GET /stop HTTP/1.1\r\nHost: 127.0.0.1:1414\r\nConnection: close\r\n\r\n")
    elif len(sys.argv)==2 and sys.argv[1]=="record":
        s.send("GET /record HTTP/1.1\r\nHost: 127.0.0.1:1414\r\nConnection: close\r\n\r\n")
    buf=[]
    while True:
        d=s.recv(1024)
        if d!="":
            buf.append(d)
        else:
            break
    print ''.join(buf)
except:
    print 'server not exists'
    s.close()
