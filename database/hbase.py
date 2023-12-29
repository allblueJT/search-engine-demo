import happybase
from happybase import Table
from typing import List, Dict
import sys
sys.path.append("..")
from utils import get_logger

class USTCHBase:
    def __init__(self, host='localhost', column_family=['cf0']):
        self.logger = get_logger('ustc-hbase')
        self.logger.info("HBase Connecting...")
        self.connection = happybase.Connection(host)
        self.connection.open()
        self.name = 'ustc'
        if self.name.encode() not in self.connection.tables():
            assert column_family is not None, "Need to indicate column families to create a table"
            self.create_table(self.name, column_family)  
        self.logger.info("HBase Connected Successfully!")
        self.table = self.get_table(self.name)
        
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, message, traceback):
        self.connection.close()
        if isinstance(type, Exception):
            traceback.print_exc()
        
    def create_table(self, table_name: str, column_families: List[str]):
        column_families = {family : dict() for family in column_families}
        self.connection.create_table(table_name, column_families)
        self.logger.info("Table {table_name} is created.")
        
    def get_table(self, table_name: str) -> Table:
        try:
            table = self.connection.table(table_name)
        except Exception as e:
            self.logger.warning(e, exc_info=True)
            table = None
        return table
        
    def put(self, row: bytes, data: Dict[bytes, bytes]):
        
        for key in data.keys():
            data[key] = data[key].encode('utf-8') if isinstance(data[key], str) else data[key]
        self.table.put(row=row, data=data)
        
    def batch_put(self, rows: List[str], data: List[Dict[str, str]]):
        with self.table.batch() as bat:
            for row, item in zip(rows, data):
                row = row.encode('utf-8')
                item = {k.encode('utf-8') : v.encode('utf-8') for k,v in item.items()}
                bat.put(row=row, data=item)

# 基本用法-备忘
        
# 存储数据：Hbase里 存储的数据都是原始的字节字符串    
# cloth_data = {'cf1:content': u'牛仔裤', 'cf1:price': '299', 'cf1:rating': '98%'}
# hat_data = {'cf1:content': u'鸭舌帽', 'cf1:price': '88', 'cf1:rating': '99%'}
# shoe_data = {'cf1:content': u'耐克', 'cf1:price': '988', 'cf1:rating': '100%'}
# author_data = {'cf2:name': u'LiuLin', 'cf2:date': '2017-03-09'}
 
# table.put(row='www.test1.com', data=cloth_data)
# table.put(row='www.test2.com', data=hat_data)
# table.put(row='www.test3.com', data=shoe_data)
# table.put(row='www.test4.com', data=author_data)

# 使用batch一次插入多行数据
# bat = table.batch()
# bat.put('www.test5.com', {'cf1:price': 999, 'cf2:title': 'Hello Python', 'cf2:length': 34, 'cf3:code': 'A43'})
# bat.put('www.test6.com', {'cf1:content': u'剃须刀', 'cf1:price': 168, 'cf1:rating': '97%'})
# bat.put('www.test7.com', {'cf3:function': 'print'})
# bat.send()


# 使用with来管理batch
# with table.batch() as bat:
#     bat.put('www.test5.com', {'cf1:price': '999', 'cf2:title': 'Hello Python', 'cf2:length': '34', 'cf3:code': 'A43'})
#     bat.put('www.test6.com', {'cf1:content': u'剃须刀', 'cf1:price': '168', 'cf1:rating': '97%'})
#     bat.put('www.test7.com', {'cf3:function': 'print'})


# 在batch中删除数据
# with table.batch() as bat:
#     bat.put('www.test5.com', {'cf1:price': '999', 'cf2:title': 'Hello Python', 'cf2:length': '34', 'cf3:code': 'A43'})
#     bat.put('www.test6.com', {'cf1:content': u'剃须刀', 'cf1:price': '168', 'cf1:rating': '97%'})
#     bat.put('www.test7.com', {'cf3:function': 'print'})
#     bat.delete('www.test1.com')

# 通过batch_size参数来设置batch的大小
# with table.batch(batch_size=10) as bat:
#     for i in range(16):
#         bat.put('www.test{}.com'.format(i), {'cf1:price': '{}'.format(i)})

# 获取一个table实例
# table = connection.table('my_table')

# 查看可以使用的table
# print connection.tables()
# 创建一个table   
# connection.create_table(
#     'my_table',
#     {
#         'cf1': dict(max_versions=10),
#         'cf2': dict(max_versions=1, block_cache_enabled=False),
#         'cf3': dict(),  # use defaults
#     }
# )
# 检索一行数据
# row = table.row('www.test4.com')
# return: {'cf2:name': 'LiuLin', 'cf2:date': '2017-03-09'}
# 通过row_start和row_stop参数来设置开始和结束扫描的row key
# for key, value in table.scan(row_start='www.test2.com', row_stop='www.test3.com'):
#     print key, value
# 通过row_prefix参数来设置需要扫描的row key
# for key, value in table.scan(row_prefix='www.test'):
#     print key, value
# 检索多行数据
# rows = table.rows(['www.test1.com', 'www.test4.com'])
# print rows
# 通过指定列族来检索数据
# row = table.row('www.test1.com', columns=['cf1'])
# print row
# 通过指定时间戳来检索数据，时间戳必须是整数
# row = table.row('www.test1.com', timestamp=1489070666)
# print row
# 在返回的数据里面包含时间戳
# row = table.row(row='www.test1.com', columns=['cf1:rating', 'cf1:price'], include_timestamp=True)
# print row
# 删除一整行数据
# table.delete('www.test4.com')
# 删除一个列族的数据
# table.delete('www.test2.com', columns=['cf1'])
# 删除一个列族中几个列的数据
# table.delete('www.test2.com', columns=['cf1：name', 'cf1:price'])
