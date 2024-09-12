import sys,time,datetime,json
sys.path.append("./framework/component")
from component import *

class CloudExample:
    def __init__(self):
        component = Component()
        self.cloud_api = component.TESTING_API_IOT()
        self.mysql = component.TESTING_MYSQL()
        self.es = component.TESTING_ELASTICSEARCH()
        
        self.did = 'xxxxxxxxxx'
        self.model = 'xxxxx'

    def get_iot_info(self):
        data = {}
        data['did'] = self.did
        data['keys'] = 'field1, field2'
        response_data = self.cloud_api.pull_data('get_info', data)
        print(response_data)

    def get_iot_history(self):
        data = {}
        data['did'] = self.did
        data['type'] = 'prop'
        data['keys'] = 'xxxxxx,xxxxxx'
        data['begin_time'] = int(time.mktime( \
            time.strptime('2020-6-13', '%Y-%m-%d')))*1000
        data['last_time'] = int(time.mktime( \
            time.strptime('2020-6-14', '%Y-%m-%d')))*1000
        result =  self.cloud_api.pull_data('get_iot_history', data, 'get')
        self.output(self.cloud_api.debug_info(), True)

    def output(self, response_data, write_file=False):
        print(response_data)
        if write_file == True:
            filename = './'+str(int(time.time()))+".txt"
            with open(filename, 'w') as file_object:
                file_object.write(json.dumps(response_data))


if __name__=='__main__':
    example = CloudExample()
    method = sys.argv[1:][0]
    if method == "" or method == None:
        method = 'get_iot'
    eval('example.'+str(method))()
