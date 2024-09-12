import sys,time,datetime,json
sys.path.append("./framework/component")
from component import *

component = Component()
redis = component.TESTING_REDIS()
# redis.set('aa','11')

print(redis.get('TESTING_mysql'))