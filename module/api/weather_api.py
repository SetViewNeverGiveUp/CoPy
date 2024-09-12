import sys
sys.path.append("./framework/component")
from component import *

class CloudWeatherExample:
    def __init__(self):
        component = Component()
        self.cloud_api = component.TESTING_API_WEATHER()

    # 热门城市
    def get_city_list_top100(self):
        self.output(self.cloud_api.pull_data('get_city_list_top100'))

    # 获取当前城市的天气
    def get_current_weather_by_city(self):
        self.output(self.cloud_api.pull_data('get_current_weather_by_city', {'city':'5809844'}))

    # 输出信息
    def output(self, response_data):
        print(response_data)


if __name__ == '__main__':
    example = CloudWeatherExample()
    method = sys.argv[1:][0]
    if method == "" or method == None:
        method = 'get_iot'
    eval('example.'+str(method))()
