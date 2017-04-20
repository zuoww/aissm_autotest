# -*-coding:utf-8-*-
import json
import sys
import socket
import socket
import time
import json
import httplib


def client(planId, groupid, pre_planbatchid, serverHost='127.0.0.1', port=1414):
    params = {"plan_id": planId, "group_id": groupid,"pre_planbatchid":pre_planbatchid}
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    print params
    print headers
    print serverHost
    try:
        httpClient = httplib.HTTPConnection(serverHost, port, timeout=30)
        httpClient.request("POST", "/test", json.dumps(params), headers)

        response = httpClient.getresponse()
        print response.status
        print response.reason
        print response.read()
        print response.getheaders()  # 获取头信息
    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()

if __name__ == "__main__":
    client(1,1,1)