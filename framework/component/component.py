# -*- coding: UTF-8 -*-
import sys,redis
sys.path.append("./framework/")
from conf_env import *
# 驱动库
sys.path.append(ENV_LIB_PATH)
from lib_curl import *
from lib_mysql import *
from lib_TESTING_api import *
from lib_elasticsearch import *
from lib_instance_log import *
from lib_io import *
from lib_common import * 
from lib_S3 import *
# 配置信息
sys.path.append(ENV_CONF_PATH)
from TESTING_redis_conf import *
from TESTING_es_conf import *
from TESTING_mysql_conf import *
from TESTING_api_iot_conf import *
from TESTING_api_weather_conf import *
from TESTING_s3_conf import *
class Component:

    ################# 驱动组件 ################

    def LIB_CURL(self):
        return Curl()

    def LIB_IO(self):
        lib_io = LibIO()
        return lib_io

    def LIB_COMMON(self):
        lib_common = LibCommon()
        return lib_common

    def LIB_S3(self):
        lib_s3 = LibS3(REGION_NAME, BUCKET_NAME)
        return lib_s3


    ################# 配置组件 ################
    def TESTING_MYSQL(self):
        return MYSQL(
            dbhost   = TESTING_MYSQL_HOST,
            dbuser   = TESTING_MYSQL_USER,
            dbpwd    = TESTING_MYSQL_PWD,
            dbname   = TESTING_MYSQL_NAME,
            dbport   = TESTING_MYSQL_PORT,
            dbcharset= TESTING_MYSQL_CHARSET)

    def TESTING_ELASTICSEARCH(self):
        return ElasticsearchDB(
            {
                'host': TESTING_ES_HOST,
                'port': TESTING_ES_PORT,
                'scheme': TESTING_ES_SCHEME
            }
        )

    def TESTING_REDIS(self):
        pool = redis.ConnectionPool(host=TESTING_REDIS_HOST, port=TESTING_REDIS_PORT, db=TESTING_REDIS_SELECT, password=None, encoding='utf-8', decode_responses=True)
        return redis.Redis(connection_pool=pool) 

    
    def TESTING_API_IOT(self):
        return TESTINGAPI(
            TESTING_API_IOT_URL,
            TESTING_API_IOT_APP_ID,
            TESTING_API_IOT_APP_KEY,
            self.TESTING_LOG_REDIS()
        )

    def TESTING_API_WEATHER(self):
        return TESTINGAPI(
            TESTING_API_WEATHER_URL,
            TESTING_API_WEATHER_APP_ID,
            TESTING_API_WEATHER_APP_KEY,
            # self.TESTING_LOG_INTERFACE()
        )

    # 日志接口请求
    def TESTING_LOG_INTERFACE(self):
        tz = pytz.timezone('UTC')
        dt = pytz.datetime.datetime.fromtimestamp(int(time.time()), tz)
        table_name = 'TESTING_interface_request_' + str(dt.year) + dt.strftime('%m')
        return InstanceLog(
            'TESTING',
            ['elasticsearch:'+table_name, self.TESTING_ELASTICSEARCH()]
        )

    # Elasticsearch聚合请求
    def TESTING_LOG_QUERY(self):
        tz = pytz.timezone('UTC')
        dt = pytz.datetime.datetime.fromtimestamp(int(time.time()), tz)
        table_name = 'TESTING_log_unique_query' + str(dt.year) + dt.strftime('%m')
        return InstanceLog(
            'TESTING',
            ['mysql:'+table_name, self.TESTING_MYSQL()]
        )
        
    # 日志TESTING_LOG + 模块名称
    def TESTING_LOG(self):
        return InstanceLog(
            'TESTING',
            ['console'])


    # 控制台输出
    def CONSOLE_LOG(self):
        return InstanceLog(
            'common',
            ['console'])


    # Console
    def TESTING_LOG_DEVICE(self):
        return InstanceLog(
            'TESTING',
            ['console'])

    # RedisLog
    def TESTING_LOG_REDIS(self):
        tz = pytz.timezone('UTC')
        dt = pytz.datetime.datetime.fromtimestamp(int(time.time()), tz)
        collection_name = 'TESTING_interface_' + str(dt.year) + dt.strftime('%m') + dt.strftime('%d') + dt.strftime('%H')+"_"
        return InstanceLog(
            'TESTING',
            ['redis:'+collection_name, self.TESTING_REDIS()])


