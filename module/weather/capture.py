import platform,sys,os,time,datetime,json
sys.path.append("./framework/component")
import pytz
from decimal import Decimal

from component import *

# 室外天气
class Capture:

    def __init__(self):
        component = Component()
        self.es = component.TESTING_ELASTICSEARCH()
        self.mysql = component.TESTING_MYSQL()
        self.api_weather = component.TESTING_API_WEATHER()
        return

    # 入口
    def main(self):
        # 测试数据
        # data = {'coord': {'lon': -122.33, 'lat': 47.61}, 'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'base': 'stations', 'main': {'temp': 283.78, 'feels_like': 283.04, 'temp_min': 282.59, 'temp_max': 284.82, 'pressure': 1016, 'humidity': 92}, 'wind': {'speed': 0.89, 'deg': 101, 'gust': 3.13}, 'rain': {'3h': 0.92}, 'clouds': {'all': 100}, 'dt': 1587613862, 'sys': {'type': 3, 'id': 2004026, 'country': 'US', 'sunrise': 1587560774, 'sunset': 1587611327}, 'timezone': -25200, 'name': 'Seattle', 'cod': 200, 'city_id': 5809844}
        # self.storage(data)
        # exit()
        city_list = self.get_city_list()
        if len(city_list) <= 0:
            print('not found city list')
            exit()
        for city_info in city_list:
            self.error_log = city_info.copy()
            self.error_log['log_time'] = int(time.time())
            self.error_log.pop('timezone')
            if self.error_log['update_time'] == None:
                self.error_log['update_time'] = 0
            try :
                response_data = self.api_weather.pull_data(
                    'get_current_weather_by_city',
                    {'city': city_info['city_id']}
                )
            except Exception as e:
                self.error_log['message'] = str(e)
                self.mysql.insert(TABLE_WEATHER_ERROR, self.error_log)
            if response_data['status'] != False:
                print(response_data['response'])
                if response_data['response']['dt'] > city_info['dt']:
                    data = self.trim_data(response_data['response'])
                    self.storage(data, city_info)
            else:
                self.error_log['message'] = 'data null'
                self.mysql.insert(TABLE_WEATHER_ERROR, self.error_log)
                continue
        return

    # 存储数据
    def storage(self, data, city_info):
        print(city_info)
        # 开尔文转摄氏度
        temp_field = ['temp', 'feels_like', 'temp_min', 'temp_max']
        for field_text in temp_field:
            data['main'][field_text] -= 273.15
            data['main'][field_text] = round(data['main'][field_text],2)
        data['update_time'] = int(time.time())
        result = self.es.insert_index(
            self.get_utc_table_name(data['dt'])
            , str(data['city_id']) + '_' + str(data['dt']), data)
        if result['_shards']['failed'] == 0:
            update_data = {}
            try:
                if "visibility" in data:
                    update_data['visibility'] = data['visibility']
                else:
                    update_data['visibility'] = "0"
                update_data['update_time'] = int(time.time())
                update_data['city_name'] = data['name']
                update_data['state'] = data['sys']['country']
                update_data['timezone'] = data['timezone']
                update_data['latitude'] = data['coord']['lat']
                update_data['longitude'] = data['coord']['lon']
                update_data['dt'] = str(data['dt'])
                update_data['main'] = data['weather'][0]['main']
                update_data['description'] = data['weather'][0]['description']
                update_data['temp'] = data['main']['temp']
                update_data['feels_like'] = data['main']['feels_like']
                update_data['temp_min'] = data['main']['temp_min']
                update_data['temp_max'] = data['main']['temp_max']
                update_data['pressure'] = data['main']['pressure']
                update_data['humidity'] = data['main']['humidity']
                update_data['wind_speed'] = data['wind']['speed']
                if "deg" in data['wind']:
                    update_data['wind_deg'] = data['wind']['deg']
                else:
                    update_data['wind_deg'] = "0"
                update_data['sunrise'] = data['sys']['sunrise']
                update_data['sunset'] = data['sys']['sunset']
            except Exception as e:
                self.error_log['message'] = 'find field error '+str(e)
                self.mysql.insert(TABLE_WEATHER_ERROR, self.error_log)
                print('find field error')
            pop_field = list(city_info.keys())
            pop_field.remove('dt')
            pop_field.remove('update_time')
            data_field = ['main', 'description', 'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure',
                          'humidity', 'wind_speed', 'wind_deg', 'wind_gust', 'sunrise', 'sunset']
            for field in list(update_data.keys()):
                if field in pop_field:
                    if city_info[field] != None:
                        update_data.pop(field)
                if field in data_field:
                    if update_data[field] == None:
                        update_data[field] = '-'
            print(update_data)
            self.mysql.update(TABLE_CITY_LIST, update_data, {'city_id':data['city_id']})
        return


    # 获取表名
    def get_utc_table_name(self, timestamp):
        tz = pytz.timezone('UTC')
        dt = pytz.datetime.datetime.fromtimestamp(timestamp, tz)
        return TABLE_PREFIX + str(dt.year) + dt.strftime('%m')

    # 获取城市ID列表
    # 5分钟内没有更新过的有效城市列表
    def get_city_list(self):
        # time_expire = int(time.time()) - 5*60
        field = 'city_id,state, city_name,timezone,update_time,create_time, dt'
        # sql = "select %s from %s where is_valid=1 and dt <= %d" % (field, TABLE_CITY_LIST, time_expire)
        sql = "select %s from %s where is_valid=1" % (field, TABLE_CITY_LIST)
        return self.mysql.query(sql)

    # 修剪数据
    def trim_data(self, data):
        content = data.copy()
        content['city_id'] = data['id']
        content.pop('id')
        return content



capture = Capture()
city_list = capture.main()
print(city_list)