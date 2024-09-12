# -*- coding: UTF-8 -*-
import random,json,sys,os
import json,random
import time,datetime
import hashlib
sys.path.append("./framework/component")
from component import *

class ExportS3:

	def __init__(self):
		component = Component()
		self.es = component.TESTING_ELASTICSEARCH()
		self.common = component.LIB_COMMON()
		self.s3 = component.LIB_S3()
		self.TIME_FIELDS = ['create_time', 'update_time', 'ttl_time']
		self.SCHEDULE_FIELDS = ['SUN','MON','THU','WED','TUE','FRI','SAT']
		self.PATH_ROOT = './source/export/s3/ttt/'
		self.test_start_scope = '1627257600000'
		self.test_end_scope = '1623456000000'
		self.io = component.LIB_IO()
		self.ALL = "ALL"
		device_id = 'xxxxxxxx'
		copyt = self.download_file('xxxxxxx', '1623888000000', '1623974933')
		# files = self.read_list(', )

	def download_file(self, device_id, day_time, second_time):
		file_path = device_id + "/" + str(day_time) + "/" + str(second_time) + ".txt"
		ret = self.s3.download_file("/" + file_path, self.PATH_ROOT + file_path)
		print(ret)
		exit()

	# 从S3获取目录
	def get_timestamp_from_s3(self, device_id):
		read_data.sort(key=lambda item: (item.get('create_time', 0)), reverse=False)
		return 

	

	# 从本地获取文件时间列表
	def get_time_by_stoage_day(self, device_id, day_timestamp):
		time_index = []
		file_list = self.walk_file(self.PATH_ROOT + device_id + "/", True)
		for time_path in file_list:
			time_split = time_path.split('/')
			print(time_split)
			exit()
			timestamp = day_split[-1]
			if (self.common.is_number(timestamp)) :
				time_index.append(timestamp)
		return day_index


	def read_list(self, file_path):
		start_time = '1626821000000'
		end_time = '1627862500000'
		current_time = int(time.time() * 1000)
		device_id = 'xxxxxxxx'
		collection_index = {}
		object_day = self.s3.get_all_objects(Delimiter="/", Prefix=device_id+'/')
		list_day = []
		for file in object_day:
			day = file['Prefix'].split('/')[-2]
			print(day)
			list_day.append(day)
		list_day.sort()

		if len(list_day) > 0:
			swich_ending = (current_time - int(list_day[-1])) > 86400000
			for day in list_day:
				path_point = device_id + "/" + day + "/"
				object_point = self.s3.get_all_objects(Prefix=path_point)

				for point in object_point:
					if day not in collection_index:
						if swich_ending == True:
							index_day = self.ALL + "_" + str(day)
							collection_index[index_day] = []
					collection_index[index_day].append(point["Key"])
			print(collection_index)
			exit()

		# list_point = self.s3.get_all_objects(Prefix=file['Prefix'])
		# 	for point_collection in list_point:
		# 		point_collection['Key']

		return 



	def get_timestamps(self, device_id):
		self.walk_file(self.PATH_ROOT + "/" + device_id)



	# 查询数据
	def query_data(self, device_id=None, between=None, _source=None, timezone=None):
		if(_source != None):
			self._source = _source
		else:
			self._source = ["create_time_text", "temperature", "device_id", "heat_sp"]
		json_exist = self.get_json_exist(self._source[:], "create_time")
		body = self.json_struct(self._source[:], json_exist, device_id, between)
		timestamp_field = 'create_time'
		split_array = device_id.split('_')
		if (len(split_array) == 3) :
			model = split_array[1]
			index_name = "batch_"+model.lower()+"*"
		dataset =  self.es.fetch_index(index_name, body, timestamp_field="create_time", timezone=timezone)
		return dataset


export_s3 = ExportS3()

