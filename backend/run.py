from flask import Flask, render_template, request
import json

app = Flask(__name__, static_url_path='')


@app.route('/result', methods=['GET'])
def result():
    search_query = request.args.get('query')
    if (search_query == '12'):
        allItems = [
            {'url': 'http://sds.ustc.edu.cn/2021/1023/c15412a526740/page.htm', 'title': '2021级数据科学硕士班组织开展新生入学教育主题班会',
             'content': '9月28日，2021级数据科学硕士班在班长吴桐、团支书叶雨涵、组织委员朱煜等班委的组织下，在校区本部开展了新生入学教育主题班会。'},
            {'url': 'http://sds.ustc.edu.cn/2021/1023/c15412a526740/page.htm', 'title': '2021级数据科学硕士班组织开展新生入学教育主题班会',
             'content': '9月28日，2021级数据科学硕士班在班长吴桐、团支书叶雨涵、组织委员朱煜等班委的组织下，在校区本部开展了新生入学教育主题班会。'},
            {'url': 'https://news.ustc.edu.cn/info/1055/85761.htm', 'title': '中国科大考点2024年全国硕士研究生招生考试顺利举行',
             'content': '12月23至24日，2024年全国硕士研究生招生考试开考，近1400名考生在我校考点参加考试。校长包信和到考场巡考，检查指导考务，慰问考务工作人员和研招志愿者。安徽省教育招生考试院巡考人员到场巡查我校考点情况'},
            {'url': 'https://gradschool.ustc.edu.cn/article/3004', 'title': '中科院大学培养与学位管理部来校调研研究生教育工作',
             'content': '10月8日，为加强院属大学沟通交流，共同提升院属大学研究生教育工作水平，中科院大学培养与学位管理部乔晗部长一行6人来我校调研学位与研究生教育相关工作。研究生院常务副院长龚流柱、副院长李思敏接待了乔晗部长一行，并出席了工作座谈交流活动，研究生院相关部门负责人和业务主管参加了座谈交流会。'},
        ]
    else:
        allItems = [
            {'url': 'http://sds.ustc.edu.cn/2021/1023/c15412a526740/page.htm', 'title': '2021级数据科学硕士班组织开展新生入学教育主题班会',
             'content': '9月28日，2021级数据科学硕士班在班长吴桐、团支书叶雨涵、组织委员朱煜等班委的组织下，在校区本部开展了新生入学教育主题班会。'},
            {'url': 'https://news.ustc.edu.cn/info/1055/85761.htm', 'title': '中国科大考点2024年全国硕士研究生招生考试顺利举行',
             'content': '12月23至24日，2024年全国硕士研究生招生考试开考，近1400名考生在我校考点参加考试。校长包信和到考场巡考，检查指导考务，慰问考务工作人员和研招志愿者。安徽省教育招生考试院巡考人员到场巡查我校考点情况'},
            {'url': 'https://gradschool.ustc.edu.cn/article/3004', 'title': '中科院大学培养与学位管理部来校调研研究生教育工作',
             'content': '10月8日，为加强院属大学沟通交流，共同提升院属大学研究生教育工作水平，中科院大学培养与学位管理部乔晗部长一行6人来我校调研学位与研究生教育相关工作。研究生院常务副院长龚流柱、副院长李思敏接待了乔晗部长一行，并出席了工作座谈交流活动，研究生院相关部门负责人和业务主管参加了座谈交流会。'},
        ]
    print('search_query', search_query)

    return json.dumps(allItems)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/home')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080")
