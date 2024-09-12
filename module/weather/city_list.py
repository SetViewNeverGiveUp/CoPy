import sys
sys.path.append("./framework/component")
from component import *

# 设备信息更新
class CityList:

    def __init__(self):
        component = Component()
        self.mysql = component.TESTING_MYSQL()
        self.api_weather = component.TESTING_API_WEATHER()
        return

    def main(self):
        sql = 'select distinct(city_id) from %s where city_id is not null and city_id>1000000' % TABLE_DEVICE_LIST
        city_list = self.mysql.query(sql)
        if len(city_list) > 0:
            city_ids = []
            for item in city_list:
                city_ids.append(item['city_id'])
            sql = 'select city_id from %s where city_id in ("%s")' \
                  % (TABLE_CITY_LIST , '","'.join(city_ids))
            exist_city_list = self.mysql.query(sql)
            exist_city_ids = []
            for city_item in exist_city_list:
                exist_city_ids.append(city_item['city_id'])
            if len(exist_city_ids) < len(city_list):
                append_ids = set(city_ids).difference(set(exist_city_ids))
                for city_id in append_ids:
                    self.append_city(city_id)
                print('find %s city_id' % str(len(append_ids)))
                self.read_city_info(append_ids)
            else:
                print('not find new city_id')
            return

        return

    # 添加城市ID
    def append_city(self, city_id):
        city_info = {}
        city_info['create_time'] = int(time.time())
        city_info['is_valid'] = 1
        city_info['city_id'] = city_id
        city_info['dt'] = 0
        return self.mysql.insert(TABLE_CITY_LIST, city_info)

    # 获取城市ID信息
    def read_city_info(self, city_ids):
        for city_id in city_ids:
            response_data = self.api_weather.pull_data(
                'get_current_weather_by_city',
                {'city': city_id}
            )
            if response_data['status'] != False:
                self.save_city_content(response_data['response'])
            else:
                continue
        return

    # 保存城市ID信息
    def save_city_content(self, data):
        if data != None:
            city_info = {}
            city_info['city_name'] = data['name']
            city_info['state'] = data['sys']['country']
            city_info['create_time'] = int(time.time())
            city_info['latitude'] = data['coord']['lat']
            city_info['longitude'] = data['coord']['lon']
            city_info['timezone'] = data['timezone']
            self.mysql.update(TABLE_CITY_LIST, city_info, {'city_id':data['id']})
        return

if __name__ == '__main__':
    city_list = CityList()
    city_list.main()