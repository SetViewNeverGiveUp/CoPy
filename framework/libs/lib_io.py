#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 0.3
# @Update: 2021/8/10
# @Python-Version: 3.x
# @Desc: 支持读取文件

import os


class LibIO:


	def __init__(self):
		return

	def output(self, content, file_path):
		with open(file_path, 'w') as file_object:
			file_object.write(content)

	def read_file(self, file_path):
		try:
			fp = open(file_path, 'r')
			content = fp.read()
			fp.close()
			return content
		except IOError:
			print('打开文件失败')
		return

	def walk_file(self, file, is_folder=False):
		file_list = []
		folder_list = []
		for root, dirs, files in os.walk(file):
			# root 表示当前正在访问的文件夹路径
			# dirs 表示该文件夹下的子目录名list
			# files 表示该文件夹下的文件list
			# 遍历文件
			for f in files:
				file_list.append(os.path.join(root, f))

			# 遍历所有的文件夹
			for d in dirs:
				if is_folder == True:
					folder_list.append(os.path.join(root, d))

			if is_folder == True:
				return folder_list
			else:
				return file_list
