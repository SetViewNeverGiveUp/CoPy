import warnings
warnings.filterwarnings("ignore")
# 环境变量
ENV_PATH = './framework/'
# 配置文件夹名称，决定选择哪个配置生效
# ENV_CONF_NAME = 'confs/aws_us'
ENV_CONF_NAME = 'confs/aliyun'



# 配置文件路径
ENV_CONF_PATH = ENV_PATH + ENV_CONF_NAME
# 引用库路径
ENV_LIB_PATH = ENV_PATH+'libs'

# 全局变量

# 调试开关
GLOBAL_VAR_DEBUG = False
INDEX_BATCH_DATA = 'TESTING_batch_data_*'
EXPORT_BATCH_DATA = INDEX_BATCH_DATA

# 载入模块变量
try:
    from _env import *
except:
    if GLOBAL_VAR_DEBUG == True:
        print('not found module variable file')
# export项目使用
