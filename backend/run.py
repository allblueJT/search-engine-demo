from flask import Flask, render_template, request
import json
from elasticsearch import Elasticsearch
import happybase
import re

es = Elasticsearch(hosts='http://localhost:9200')

# 创建索引

if es.indices.exists(index="idx"):
    print('索引已存在')
    # es.indices.delete(index="idx")
else:
    print('索引不存在，可以创建')
    
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

    def clean_date(date_str):
        # 使用正则表达式匹配日期部分
        match = re.search(r'\d{4}-\d{2}-\d{2}', date_str)
        if match:
            return match.group()
        return date_str
    
    res = es.indices.create(index="idx", body=doc)

    conn = happybase.Connection('localhost', port=9090)  
    ustc_table = conn.table('ustc') 
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
    conn.close()

app = Flask(__name__, static_url_path='')

@app.route('/result', methods=['GET'])
def result():
    query_string = request.args.get('query')

    # 定义搜索查询
    search_query = {
        "query": {
            "match": {
                "title": query_string
            }
        },
        "size": 10,  # 获取前10个匹配的文档
        "sort": {
            "_score": {  # 首先按照相关性得分降序排序
                "order": "desc"
            },
            "date": {  # 如果相关性得分相同，再按日期降序排序
                "order": "desc"
            }
        }
    }

    search_results = es.search(index="idx", body=search_query)
    allItems = []
    for hit in search_results['hits']['hits']:
        result = hit['_source']
        allItems.append({'url': result['url'], 'title': result['title'], 'content': result['article']})

    # print(allItems)

    return json.dumps(allItems)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/home')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080")
