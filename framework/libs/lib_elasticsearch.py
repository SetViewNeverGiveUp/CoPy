#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Di
# @Version: 1.3
# @Update: 2021-5-18
# @Python-Version: 3.x
# @Desc: Elasticsearch 支持切换协议

import csv,time,pytz
from elasticsearch import Elasticsearch
from datetime import datetime
from datetime import timedelta

class ElasticsearchDB:

    def __init__(self, config=None):
        self.body = ""
        self.connect = None
        self.host = ('localhost' if 'port' not in config else config['host'])
        self.port = (9200 if 'port' not in config else config['port'])
        self.user = (None if 'user' not in config else config['user'])
        self.password = (None if 'password' not in config else config['password'])
        if self.user is None and self.password is None:
            self.auth = None
        else :
            self.auth = (self.user, self.password)
        self.timeout = (3600 if 'timeout' not in config else config['timeout'])
        self.create_connect(config)

    # 创建连接
    def create_connect(self, config=None):
        if 'scheme' in config:
            scheme = config['scheme']
        else:
            scheme = 'https'
        self.connect = Elasticsearch(
            [
                {
                    'host':self.host,
                    'port':self.port
                }
            ],
            http_auth=self.auth,
            scheme=scheme,
            timeout=self.timeout
        )
        return self.connect


    # 读取查询行数
    def get_query_total(self, index, body=None):
        ret = self.connect.count(index=index, body=body)
        if ret != None:
            return ret['count']
        else :
            return None


    # 创建索引
    def create_indices(self, index, body=None):
        if self.connect.indices.exists(index=index) is not True:
            return self.connect.indices.create(index=index, body=body)

    # 插入数据
    def insert_index(self, index=None, doc_id=None, body=None):
        return self.connect.index(index=index, id=doc_id, body=body)
    # 删除数据
    def delete_index(self, index=None):
        return self.connect.indices.delete(index=index,ignore=[400, 404])

    def update_index(self, index=None, body=None, doc_type="_doc", id=None, params=None):
        # 必须有doc
        body = {'doc':body}
        return self.connect.update(index = index, id=id, body=body)

    def get_connect(self):
        return self.connect

    # 搜索
    def fetch(self, index=None, body={"query":{"match_all":{}}}):
        self.body = body
        return self.connect.search(index=index, body=body)

    # 初始化会话
    def scroll_init(self):
        self.scroll_id = None
        self.scroll_total = None

    def get_body(self):
        return self.body

    # 支持翻页
    def fetch_index(self, index=None, body={"query":{"match_all":{}}}, size=2000, scroll="2m",timestamp_field=None,timezone='+8'):
        self.scroll_init()
        data_ret = []
        self.body = body
        query = self.connect.search(index=index, body=body, scroll=scroll, size=size)
        if query is not None:
            data_ret = query['hits']['hits']
            self.scroll_total = query['hits']['total']['value']
            if self.scroll_total > 0:
                self.scroll_id = query['_scroll_id']
        if self.scroll_total > size:
            # 分页
            query_amount = self.scroll_total / size
            if self.scroll_total % size != 0:
                query_amount = query_amount
            else:
                query_amount = round(query_amount,0) - 1
            query_amount = int(query_amount)
            for page in range(0,query_amount):
                data_tmp = self.connect.scroll(scroll_id=self.scroll_id, scroll=scroll)
                data_ret = data_ret + data_tmp['hits']['hits']
        if self.scroll_total > 0:
            print('------ clean ----- ')
            ret = self.connect.clear_scroll(scroll_id=self.scroll_id)
            print(ret)
            print('------ finish clean -----')
        if len(data_ret) > 0:
            meta_ret = []
            for data_row in data_ret:
                row_source = data_row['_source']
                if timestamp_field != None and len(timestamp_field)>0:
                    if timestamp_field in row_source.keys():
                        row_value = {}
                        row_value[str(timestamp_field)+'_text'] = self.format_date_utc2timezone(int(row_source[timestamp_field]), timezone)
                        row_value['timezone'] = timezone
                        row_value = {**row_value, **row_source}
                meta_ret.append(row_value)
            return meta_ret
        else:
            return None

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
        if timestamp > 1000000000000:
            timestamp = int(timestamp / 1000)
        timestamp = datetime.utcfromtimestamp(timestamp)
        if timezone[0] == '+':
            timestamp += timedelta(hours=int(timezone[1:]))
        elif timezone[0] == '-':
            timestamp -= timedelta(hours=int(timezone[1:]))
        else:
            timestamp = timestamp.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz=pytz.timezone(timezone))
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    # 导出CSV
    def export_csv(self, file_path, data, fields):
        line = 0
        file_path = str(file_path)
        file_path = file_path.rstrip(".csv")
        file_path += ".csv"
        # a+追加
        with open(file_path, "w", newline='', encoding='utf-8') as flow:
            csv_writer = csv.writer(flow)
            if line == 0:
                csv_writer.writerow(fields)
            line += 1
            for row in data:
                align = {}
                for field in fields:
                    if field in row.keys():
                        align[field] = row[field]
                    else:
                        align[field] = None
                csv_writer.writerow(align.values())
            flow.flush()

    # 聚合查询唯一值
    def query_unifield(self, index, field):
        body = r"""
            {
                "aggs": {
                    "agg_%s": {
                        "terms": {
                            "field": "%s",
                            "size":5000000
                        }
                    }
                },
                "size": 0
            }
        """ % (field, field)
        return self.fetch(index, body)