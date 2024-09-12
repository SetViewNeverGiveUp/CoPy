#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 0.1
# @Update: 2020/9/15
# @Python-Version: 3.x
# @Desc: 获取安全机密信息

import boto3,redis,json
from botocore.exceptions import ClientError
from TESTING_redis_conf import *
class SecretsManager:

	def __init__(self, region_name='us-west-2'):
		pool = redis.ConnectionPool(host=TESTING_REDIS_HOST, port=TESTING_REDIS_PORT, db=TESTING_REDIS_SELECT, password=None, encoding='utf-8', decode_responses=True)
		self.redis = redis.Redis(connection_pool=pool)
		self.region_name = region_name
		return None

	def getAWSSecretValue(self, secret_name):
		session = boto3.session.Session()
		client = session.client(
		    service_name='secretsmanager',
		    region_name=self.region_name,
		)
		try:
		    get_secret_value_response = client.get_secret_value(
		        SecretId=secret_name
		    )
		except ClientError as e:
		    if e.response['Error']['Code'] == 'ResourceNotFoundException':
		        print("The requested secret " + secret_name + " was not found")
		    elif e.response['Error']['Code'] == 'InvalidRequestException':
		        print("The request was invalid due to:", e)
		    elif e.response['Error']['Code'] == 'InvalidParameterException':
		        print("The request had invalid params:", e)
		else:
		    if 'SecretString' in get_secret_value_response:
		        return get_secret_value_response['SecretString']
		    else:
		        return get_secret_value_response['SecretBinary']
		
	def getSecretValue(self, secret_name, prefix='TESTING_'):
		secret_name = prefix + secret_name
		if self.redis.exists(secret_name):
			content = self.redis.get(secret_name)
		else:
			content = self.getAWSSecretValue(secret_name)
			if content != None:
				self.redis.set(secret_name, content)
				self.redis.expire(secret_name, TESTING_REDIS_EXPIRE)
		content = json.loads(content)
		if isinstance(content,str):
			content = json.loads(content)
		return content
