import requests, lxml
from lxml import etree
import time
import random
import io
import logging
import os
from abc import ABC, abstractmethod
from tqdm import tqdm

class Sleep:
    def __init__(self, func):
        self.func = func
        self.visit_cnt = 0
    
    def __call__(self, *args, **kwargs):
        if self.visit_cnt > 4:
            time.sleep(2 + random.random() * 4)
        else:
            self.visit_cnt += 1
        self.func(*args, **kwargs)

class Crawler(ABC):
    def __init__(self):
        self.name = None
        self.main_url = None
        self.src_store_url = None
        self.src_ext = ['doc', 'docx', 'pdf', 'txt', 'xlsx', 'xls', 'ppt', 'zip', 'tar', '7z']
        
        self.visit_cnt = 0
        self.desc = "爬取{name}的爬虫\n" \
                    "主页网址：{main_url}"
        
    def __repr__(self):
        return self.desc.format(name=self.name, main_url=self.main_url)
    
    def sleep(self):
        time.sleep(0.5 + random.random() * 1)
    
    def get_etree_html(self, url):
        self.sleep()
        response = requests.get(url)
        html = response.content
        return etree.HTML(html)
    
    def download_src(self, url, ext, name, save_path='./'):
        self.sleep()
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        self.visit_cnt = Crawler.sleep(self.visit_cnt)
        
        src = requests.get(url)
        content = io.BytesIO(src.content)
        if name.split('.')[-1] not in self.src_ext:
            name = name + '.' + ext
        if name in os.listdir(save_path):
            logging.info(f'>>> {name} exists! Pass <<<')
            return
    
        fname = os.path.join(save_path, name)
        with open(fname, 'wb') as f:
            f.write(content.read())
        logging.info(f'>>> {fname} has been downloaded <<<')
        
    def get_src_from_store(self, src_urls, src_names, host_url=None, save_path='./'):
        if host_url is not None:
            src_urls = [host_url + url for url in src_urls]
            
        for url, name in tqdm(zip(src_urls, src_names), total=len(src_urls), desc='A Page'):
            ext = url.split('.')[-1]
            # print('ext: ', ext)
            if ext not in self.src_ext:
                cur_src_urls, cur_src_names = self.get_src_from_page(url, host_url=host_url)
                # print('doc name: ', cur_src_names)
                # print('doc urls: ', cur_src_urls)
                for url_, name_ in zip(cur_src_urls, cur_src_names):
                    ext_ = url_.split('.')[-1]
                    # print(url_)
                    self.download_src(url_, ext_, name_, save_path)
            else:
                self.download_src(url, ext, name, save_path)
               
    @abstractmethod 
    def get_src_urls(url):
        raise NotImplementedError()
        
    @abstractmethod 
    def get_src_from_page(self, url, host_url=None):
        raise NotImplementedError()

    def crawl_src(self, host_url=None, save_path='./'):
        if self.src_store_url is None:
            logging.info(f"{self.name}没有资源下载网页！")
            return
        src_urls, src_names = self.get_src_urls(self.src_store_url)
        self.get_src_from_store(src_urls, src_names, host_url, save_path)
        