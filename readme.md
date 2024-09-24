# 简介
这是一套将需要的中间件进行二次加工，并快速封装成自己需要样子的脚手架。使用方法如下：

# 自带的组件，后续可以根据需求自行封装：
lib_common // 通用组件 <br />
lib_curl // 网络请求 <br />
lib_datetime // 时间相关操作<br />
lib_elasticsearch // ES操作<br />
lib_earth // 演示调用某三方API平台<br />
lib_mysql // MySQL操作<br />
lib_S3 // AWS S3操作<br />
# 组件使用演示
```angular2html
# 每个文件前3行载入框架依赖
import sys,json
sys.path.append("./framework/component")
from component import *

    def __init__(self):
        # 构造方法声明组件引用
        component = Component()
        # 声明MySQL组件
        self.mysql_conn = component.TESTING_MYSQL()
        # 声明Elasticsearch组件
    self.es = component.TESTING_ELASTICSEARCH()
        # 声明通用组件
    self.common = component.LIB_COMMON()
        # 声明S3组件
    self.s3 = component.LIB_S3()
        # 天气API         
        self.api_weather = component.TESTING_API_WEATHER()
        return
    
    def count_mysql_data(self):
        # 使用MySQl组件查询数据
        sql = 'select count(*) as t from TESTING_fcode'
        return self.mysql_conn.query(sql)[0]['t']
        
    def query_table_data(self):
        # 查询ES数据
        return self.es.fetch_index(index_name, body, timestamp_field="create_time", timezone=timezone)

    def read_city_info(self, city_ids):
        for city_id in city_ids:
            # 演示调用定制调用三方API组件
            response_data = self.api_weather.pull_data(
                'get_current_weather_by_city',
                {'city': city_id}
            )
            if response_data['status'] != False:
                self.save_city_content(response_data['response'])
            else:
                continue
        return

    def download_file(self, device_id, day_time, second_time):
        file_path = device_id + "/" + str(day_time) + "/" + str(second_time) + ".txt"
        # S3下载文件
        ret = self.s3.download_file("/" + file_path, self.PATH_ROOT + file_path)
        print(ret)
        exit()
```

# 目录结构
├── framework // 框架目录<br />
│  ├── component <br />
│  │  └── component.py // 组件声明<br />
│  ├── conf_env.py // 环境变量<br />
│  ├── confs // 配置文件<br />
│  │  ├── aliyun // 配置目录1<br />
│  │  ├── aws_us // 配置目录2<br />
│  │  └── local // 配置目录3<br />
│  └── libs 组件库 <br />
│      ├── lib_S3.py // AWS S3操作<br />
│      ├── lib_common.py // 通用组件<br />
│      ├── lib_curl.py // 网络请求<br />
│      ├── lib_datetime.py // 时间相关<br />
│      ├── lib_earth_api.py // 某平台API调用<br />
│      ├── lib_elasticsearch.py // ES<br />
│      ├── lib_instance_log.py <br />
│      ├── lib_io.py // 文件处理<br />
│      └── lib_mysql.py // MySQL操作<br />
├── module // 模块目录<br />
│  ├── api // 演示模块1<br />
│  │  ├── debug.py <br />
│  │  └── weather_api.py <br />
│  ├── encode // 演示模块2<br />
│  │  └── import_config.py <br />
│  ├── export // 演示模块3<br />
│  │  └── sync_s3.py <br />
│  ├── redis // 演示模块4<br />
│  │  └── debug.py <br />
│  └── weather // 演示模块5<br />
│      ├── _env.py // 环境变量<br />
│      ├── capture.py <br />
│      └── city_list.py<br />
└── readme.md<br />



