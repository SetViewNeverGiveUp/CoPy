#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 1.3
# @Update: 2021/6/10 
# @Python-Version: 3.x
# @Desc: 支持Redis记录日志
import sys
sys.path.append('../component')
from component import *
import platform,sys,os,time,random,string,hmac,hashlib,json
from lib_curl import Curl as LIB_CURL

class TESTINGAPI:

    def __init__(self, api_url, app_id, app_key, request_log=None):
        if (request_log != None):
            self.REQUEST_LOG = request_log
        else:
            self.REQUEST_LOG = None
        self.API_URL = api_url
        self.APP_ID = app_id
        self.APP_KEY = app_key
        self.nonce = ""
        self.content = ""
        self.response_data = None

    # 文件头
    def get_header(self, signature):
        return ['appid:' + self.APP_ID,
                  'Signature:' + signature,
                  'nonce:' + self.nonce]

    # 签名
    def get_signature(self, content):
        return hmac.new(bytes(self.APP_KEY, 'utf-8'),
                             bytes(content, 'utf-8'),
                             hashlib.md5).hexdigest()
    # 随机噪声
    def get_nonce(self):
        return str(int(round(time.time() * 1000)))

    # 调用API
    def pull_data(self, request_uri, content={}, method='get'):
        # 记录日志
        if self.REQUEST_LOG != None:
            message = {}
            message['request_uri'] = request_uri
            message['content'] = content
            self.REQUEST_LOG.println(message, track=3)
        response_data = None
        url = self.API_URL + request_uri
        curl = LIB_CURL()
        content['nonce'] = self.get_nonce()
        node_start_time = time.time() * 1000
        print(" ------------- start %s ----------->"%(request_uri))
        try:
            if content is not None:
                content_sorted = {}
                for index in sorted(content.keys(),reverse=False):
                    content_sorted[index] = content[index]
                if method == 'get':
                    query_string = self.get_request_string(content_sorted)
                    signature = self.get_signature(query_string)
                    header = self.get_header(signature)
                    curl.setHeader(header)
                    self.url = url
                    response_data = curl.getData(url + "?" + query_string)
                elif method == 'post':
                    signature = self.get_signature(json.dumps(content_sorted))
                    header = self.get_header(signature)
                    content_type = 'Content-Type: application/json;charset=UTF-8'
                    header.append(content_type)
                    curl.setHeader(header)
                    self.url = url
                    response_data = curl.postData(url, content_sorted, False)
            data = json.loads(response_data)
            self.response_data = data
            node_end_time = time.time() * 1000
            print("interval: %s"%(node_end_time - node_start_time))
            print(" <------------- end %s -----------"%(request_uri))
            if str(data['code']) == str(1) and 'data' in data:
                if data['data'] is not None:
                    pull_status = True
                else :
                    if 'set_iot_prop' in url:
                        pull_status = True
                        return {'status': pull_status, 'response':data['message']}
                    else:
                        pull_status = False
                return {'status': pull_status, 'response':data['data']}
            else:
                return {'status':False, 'response': data}
        except Exception as e:
            print(e)
            print('find error')
            return {'status':False, 'response':e}            


    def debug_info(self):
        return [self.response_data, self.url]


    # 拼接参数
    def get_request_string(self, args, operator=None):
        if operator is None:
            operator = '&'
        strData = ''
        for key in args:
            if(isinstance(args[key],list)):
                subStr = ','.join(args[key])
            else:
                subStr = args[key]
            strData += '%s'%key + '=' + '%s'%subStr + operator
        strData = strData.strip('&')
        return strData
