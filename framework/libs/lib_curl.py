#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 1.1
# @Update: 2017/1/22
# @Python-Version: 3.x
# @Desc: 去掉调试信息

import pycurl
import io,json
from io import StringIO
import urllib.parse
import urllib.request

class Curl:

	def __init__(self):
		curl = pycurl.Curl()
		# proxy
		curl.setopt(pycurl.USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
		# timeout
		curl.setopt(pycurl.TIMEOUT, 300)
		curl.setopt(pycurl.CONNECTTIMEOUT,60)
		# cookies
		curl.setopt(pycurl.COOKIEFILE, "cookie_file_name")
		curl.setopt(pycurl.COOKIEJAR, "cookie_file_name")
		# config
		curl.setopt(pycurl.FOLLOWLOCATION, 1)
		curl.setopt(pycurl.MAXREDIRS,5)
		# curl.setopt(pycurl.VERBOSE, 1)
		self.curl = curl

	def setHeader(self, header):
		self.curl.setopt(pycurl.HTTPHEADER, header)

	def setopt(self, param, val):
		self.curl.setopt(param, val)

	def getCurl(self):
		return self.curl

	def postData(self, url, data, encode=True):
		curl = self.curl
		curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
		curl.setopt(pycurl.URL, url)
		fp = io.BytesIO()
		data = json.dumps(data)
		# if encode is True:
		# 	data = urllib.parse.urlencode(data)
		curl.setopt(pycurl.POSTFIELDS,data)
		curl.setopt(pycurl.WRITEFUNCTION, fp.write)
		curl.perform()
		return fp.getvalue()

	def getData(self, url):
		curl = self.curl
		curl.setopt(pycurl.URL, url)
		fp = io.BytesIO()
		curl.setopt(pycurl.WRITEFUNCTION, fp.write)
		curl.perform()
		return fp.getvalue()

	def deleteData(self, url, data):
		curl = self.curl
		curl.setopt(pycurl.URL, url)
		curl.setopt(pycurl.CUSTOMREQUEST, "DELETE")
		fp = io.BytesIO()
		curl.setopt(pycurl.POSTFIELDS, urllib.parse.urlencode(data))
		curl.setopt(pycurl.WRITEFUNCTION, fp.write)
		curl.perform()
		return fp.getvalue()




