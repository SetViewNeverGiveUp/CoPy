#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 0.3
# @Update: 2021/8/10
# @Python-Version: 3.x
# @Desc: 支持数字判断


class LibCommon:

	def __init__(self):
		return

	def is_number(self, s):
		try:
			float(s)
			return True
		except ValueError:
			pass
	 
		try:
			import unicodedata
			unicodedata.numeric(s)
			return True
		except (TypeError, ValueError):
			pass
		return False

