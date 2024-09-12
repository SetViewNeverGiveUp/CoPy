#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 1.2
# @Update: 2021-6-8
# @Python-Version: 3.x
# @Desc: 支持Redis日志

import pytz, random, string, hashlib, time, sys, json
from datetime import datetime

class InstanceLog:

    # 实例ID
    def get_instance_id(self):
        str_rand = ['{}'.format(''.join([random.choice(string.ascii_letters.lower()) for _ in range(32)])) for i in range(1)][0]
        md5 = hashlib.md5()
        md5code = str(str_rand) + str(int(round(time.time() * 1000)))
        md5code = md5code.encode("utf8")
        md5.update(md5code)
        return md5.hexdigest()

    # 记录日志
    def write(self, message, level=0, send_mail=False, track=2):
        self.instance_id = self.get_instance_id()
        data_log = {}
        data_log['instance_id'] = self.instance_id
        data_log['level'] = level
        if isinstance(message, dict):
            if self.storage['engine'] in ['elasticsearch']:
                data_log = dict(data_log, **message)
            else:
                message = json.dumps(message)
                data_log['message'] = message
        else:
            data_log['message'] = message

        data_log['cli_target'] = sys._getframe(track).f_code.co_filename
        data_log['cli_target'] += '('+ sys._getframe(track).f_code.co_name
        data_log['cli_target'] += ':'+ str(sys._getframe(track).f_lineno) +')'
        data_log['project'] = self.project
        data_log['time'] = str(int(round(time.time() * 1000)))
        data_log['datetime'] = self.format_datetime_by_zone(time.time())
        return getattr(self, 'write_' + self.storage['engine'], None)(data_log)
        # exit()

    # 记录并输出日志
    def println(self, message, level=0, send_mail=False, track=2):
        return self.write(message, level, send_mail, track)

    # 写入文件
    def write_file(self, data_log):
        str_datetime = data_log['datetime']
        str_level = self.TYPE_TEXT[data_log['level']]
        data_log.pop('datetime')
        data_log.pop('level')
        data_log = json.dumps(data_log)
        with open(self.storage['index'], 'a+') as f:
            f.write(str_datetime + ' ' + str_level + '\n')
            f.write(data_log + '\n\n')

    # 写入控制台
    def write_console(self, data_log):
        str_datetime = data_log['datetime']
        str_level = self.TYPE_TEXT[data_log['level']]
        print(str_datetime + ' '+str_level+ ' ' + data_log['message'])

    # 写入Elasticsearch
    def write_elasticsearch(self, data_log):
        data_log['create_time'] = int(data_log['time'])
        return self.storage['component'].insert_index(
            self.storage['index'], 
            None,
            data_log    
        )   

    # 写入Redis
    def write_redis(self, data_log):
        tz = pytz.timezone('UTC')
        dt = pytz.datetime.datetime.fromtimestamp(int(time.time()), tz)
        sorted_name = str(dt.year) +"-"+ dt.strftime('%m') +"-"+ dt.strftime('%d') + " 0:0:0"
        dd = datetime.strptime(sorted_name, "%Y-%m-%d %H:%M:%S")
        sorted_index = self.storage['index'] + str((int)(time.mktime(dd.timetuple())))
        self.storage['component'].zadd(sorted_index, {json.dumps(data_log): int(time.time()*1000)})
        self.storage['component'].expire(sorted_index, 86400)
        return True

    # 写入MySQL
    def write_mysql(self, data_log):
        try:
            return self.storage['component'].insert(
                self.storage['index'],
                data_log
            )
        except Exception as e:
            print('instance error:'+str(e))
            if 'exist' in str(e):
                sql = "CREATE TABLE IF NOT EXISTS %s (" % self.storage['index']
                sql += "`instance_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,"
                sql += "`project` varchar(50) DEFAULT NULL,"
                sql += "`message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,"
                sql += "`cli_target` varchar(100) DEFAULT NULL,"
                sql += "`level` tinyint(1) DEFAULT '0',"
                sql += "`time` bigint(15) DEFAULT NULL,"
                sql += "`datetime` datetime DEFAULT NULL,"
                sql += "PRIMARY KEY (`instance_id`)"
                sql += ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
                self.storage['component'].query(sql)
                self.write_mysql(data_log)
            else:
                return False

    # 按时区格式化时间戳
    def format_datetime_by_zone(self, timestamp):
        if timestamp > 1000000000000:
            timestamp = int(timestamp / 1000)
        tz = pytz.timezone(self.timezone)
        dt = pytz.datetime.datetime.fromtimestamp(timestamp, tz)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    # 初始化
    def __init__(self, project, connect, timezone="Asia/Shanghai"):
        self.TYPE_TEXT = ['', 'WARNING', 'ERROR']
        config = connect[0].split(':')
        self.project = project
        self.storage = {}
        self.storage['engine'] = config[0]
        if len(config) > 1 :
            self.storage['index'] = config[1]
        if len(connect) > 1:
            self.storage['component'] = connect[1]
        self.timezone = timezone
        return

