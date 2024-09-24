import sys,json
sys.path.append("./framework/component")
from component import *

class FCode:

    def __init__(self):
        component = Component()
        self.mysql_conn = component.TESTING_MYSQL()
        return


    # 读数据
    def read_file(self):
        filepath = './source/config.json'
        try:
            fp = open(filepath, "r")
            content = fp.read()
            fp.close()
            return content
        except IOError:
            print('file error')
        return None

    # 擦写
    def erase_data(self):
        sql = 'truncate table TESTING_fcode'
        self.mysql_conn.query(sql)

    # 计数
    def count_mysql_data(self):
        sql = 'select count(*) as t from TESTING_fcode'
        return self.mysql_conn.query(sql)[0]['t']

    def main(self):
        self.erase_data()
        data = self.read_file()
        data = json.loads(data)
        file_count = len(data)
        for fcode in data:
            item = {}
            item['encode'] = fcode
            item['stage'] = json.dumps(data[fcode])
            self.mysql_conn.insert('TESTING_fcode', item)
        db_count = self.count_mysql_data()
        print(file_count)
        print(db_count)
        if file_count == db_count:
            print('finish')
        else:
            print('count error')

if __name__ == '__main__':
    fcode = FCode()
    fcode.main()
