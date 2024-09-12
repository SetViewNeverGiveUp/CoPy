import boto3
import botocore
import os,json,time

import sys

class LibS3:

	def __init__(self, region, bucket):
		self.region = region
		self.bucket = bucket
		self.s3_client = boto3.client('s3', region_name=self.region)
		self.s3_res = boto3.resource('s3', region_name=self.region)

	def get_bucket_file_list(self):
		bucket = self.s3_res.Bucket(self.bucket)
		for key in bucket.objects.all():
			print(key.key)

	def get_all_file(self):
		bucket = self.s3_res.Bucket(self.bucket)
		file_list = []
		for obj in bucket.objects.all():
			key = obj.key
			body = obj.get()['Body'].read()
			file_list.append(key)
		self.output(file_list, True)

	
	def read_file(self, file_path):
		obj = self.s3_client.get_object(Bucket=self.bucket, Key=file_path)
		contents = obj['Body'].read()
		return contents 


	def get_root_objects(self, delimiter='/'):
		result = self.s3_client.list_objects(Bucket=self.bucket, Delimiter=delimiter)
		for o in result.get('CommonPrefixes'):
		   print(o.get('Prefix'))

	# 读取S3文件列表
	def get_all_objects(self, **base_kwargs):
		base_kwargs['Bucket'] = self.bucket
		continuation_token = None
		while True:
			list_kwargs = dict(MaxKeys=1000, **base_kwargs)
			if continuation_token:
				list_kwargs['ContinuationToken'] = continuation_token
			response = self.s3_client.list_objects_v2(**list_kwargs)
			if 'Delimiter' in base_kwargs:
				# folder
				yield from response.get("CommonPrefixes", [])
			else:
				# file
				yield from response.get("Contents", [])
			if not response.get('IsTruncated'):  # At the end of the list?
				break
			continuation_token = response.get('NextContinuationToken')

	def download_file(self, file_path, target_path='./s3'):
		file_name = str(os.path.basename(file_path))
		target_folder = os.path.dirname(target_path)
		try:
			os.makedirs(target_folder, mode=0o755)
		except Exception as e:
			if 'File exists' not in str(e):
				print(e)
				exit()
		if len(file_name) > 0:
			with open(target_path, 'wb') as f:
				self.s3_client.download_fileobj(self.bucket, file_path, f)


	def output(self, response_data, write_file=False):
		if write_file == True:
			filename = './'+str(int(time.time()))+".txt"
			with open(filename, 'w') as file_object:
				file_object.write(json.dumps(response_data))


