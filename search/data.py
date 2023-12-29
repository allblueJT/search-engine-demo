from elasticsearch import Elasticsearch
import happybase
import re

def clean_date(date_str):
    # 使用正则表达式匹配日期部分
    match = re.search(r'\d{4}-\d{2}-\d{2}', date_str)
    if match:
        return match.group()
    return date_str

es = Elasticsearch(hosts='http://localhost:9200')
doc = {
    "mappings": {
        "properties": {
            "title": {
                "type": "text"    # 使用了IK分词器
            },
            "url": {
                "type": "keyword" # 不会进行分词和分析
            },
            "date": {
                "type": "date"
            },
            "article": {
                "type": "text"
            }
        }
    }
}

if es.indices.exists(index="idx"):
    print('索引已存在')
    # es.indices.delete(index="idx")
else:
    print('索引不存在，可以创建')
    res = es.indices.create(index="idx", body=doc)

conn = happybase.Connection('localhost', port=9090)  
ustc_table = conn.table('ustc')  

if False:
    num = 0
    for key, data in ustc_table.scan():
        num += 1
        # if num >= 10:
            # break
        url = key.decode('utf-8')
        article = data[b'cf0:article'].decode('utf-8')
        date = data[b'cf0:date'].decode('utf-8')
        date = clean_date(date)
        title = data[b'cf0:title'].decode('utf-8')
        es.index(index="idx", id=num, body={"url":url, "article":article, "date":date, "title":title})


query_string = "中科大"
# 定义搜索查询
search_query = {
    "query": {
        "match": {
            "title": query_string
        }
    },
    "sort": {
        "date": {
            "order": "desc"
            }
    }
}

search_results = es.search(index="idx", body=search_query, size=3)

    
# print(es.indices.get(index="idx"))
# print(es.get(index="idx",id=3))

for hit in search_results['hits']['hits']:
    print(hit['_source']['date'])  # 打印匹配到的文档内容
conn.close()