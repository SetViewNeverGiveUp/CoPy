#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 0.3
# @Update: 2020/8/5
# @Python-Version: 3.x
# @Desc: 支持转换时间戳

import datetime,pytz

class DateTime:

    # 转换UTC Unix时间戳
    def convert_timestamp(datetime_object, timezone_text):
        time.mktime(pytz.timezone(timezone_text).localize(datetime_object).utctimetuple())

    # 格式化时间戳
    def format_date(self, str_time, str_format='%Y-%m-%d %H:%M:%S'):
        str_time = int(str_time)
        if str_time > 1000000000000:
            str_time = int(str_time / 1000)
        return time.strftime(str_format, time.localtime(str_time))

    # 按时区格式化时间戳
    def format_date_byzone(self, timestamp, timezone='Asia/Shanghai'):
        if timestamp > 1000000000000:
            timestamp = int(timestamp / 1000)
        tz = pytz.timezone(timezone)
        dt = pytz.datetime.datetime.fromtimestamp(timestamp, tz)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    # 按UTC时区格式化时间戳
    def format_date_utc2timezone(self, timestamp, timezone='+8'):
        # corver_timestamp_dateime_str
        if timestamp > 1000000000000:
            timestamp = int(timestamp / 1000)
        timestamp = datetime.utcfromtimestamp(timestamp)
        if timezone[0] == '+':
            timestamp += timedelta(hours=int(timezone[1:]))
        elif timezone[0] == '-':
            timestamp -= timedelta(hours=int(timezone[1:]))
        return str(timestamp)