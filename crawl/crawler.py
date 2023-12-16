import requests, lxml
from lxml import etree
import time
import random
import io
import logging
import os, sys
from abc import ABC, abstractmethod
from tqdm import tqdm

sys.path.append("..")

from utils import get_logger, get_args

logger = get_logger(__name__, 'crawler.log')

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
    def __init__(self, args):
        self.name = None
        self.main_url = None
        self.main_page = None
        self.src_store_url = None
        self.src_ext = ['doc', 'docx', 'pdf', 'txt', 'xlsx', 'xls', 'ppt', 'zip', 'tar', '7z', 'png', 'jpg', 'gif', 'jpeg']
        
        self.args = args
        self.page_url = None
        # self.store_2_page_list_xpath = None
        # self.download_page_2_file_xpath = None
        
        self.visit_cnt = 0      # to control QPS
        self.desc = "Crawler for {name}\n" \
                    "Home page: {main_page}"
        
    def __repr__(self):
        return self.desc.format(name=self.name, main_page=self.main_page)
    
    def sleep(self):
        time.sleep(0.5 + random.random() * 1)
    
    @staticmethod
    def get_etree_html(url):
        time.sleep(0.5 + random.random() * 1)
        response = requests.get(url)
        html = response.content
        return etree.HTML(html)
    
    def download_src(self, url, ext, name, save_path='./'):
        self.sleep()
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        self.visit_cnt = Crawler.sleep(self.visit_cnt)
        
        src = requests.get(url)
        content = io.BytesIO(src.content)
        if name.split('.')[-1] not in self.src_ext:
            name = name + '.' + ext
        if name in os.listdir(save_path):
            logger.info(f'>>> {name} exists! Pass <<<')
            return
    
        fname = os.path.join(save_path, name)
        with open(fname, 'wb') as f:
            f.write(content.read())
        logger.info(f'>>> {fname} has been downloaded <<<')
        
    def get_src_from_store(self, src_urls, src_names, host_url=None, save_path='./'):
        if host_url is not None:
            src_urls = [host_url + url for url in src_urls]
            
        for cnt, (url, name) in enumerate(zip(src_urls, src_names)):
            ext = url.split('.')[-1]
            print('ext: ', ext)
            if ext not in self.src_ext:     # url directs to a page but not src file
                cur_src_urls, cur_src_names = self.get_src_from_page(url, host_url=host_url)
                cur_src_urls = [host_url + url_ if url_.startswith('/') else url_ for url_ in cur_src_urls]
                # print('doc name: ', cur_src_names)
                # print('doc urls: ', cur_src_urls)
                for url_, name_ in zip(cur_src_urls, cur_src_names):
                    ext_ = url_.split('.')[-1]
                    # print(url_)
                    self.download_src(url_, ext_, name_, save_path)
            else:
                self.download_src(url, ext, name, save_path)
            if self.args.debug and cnt >= 1:
                break
    
    def get_src_urls(self, url):
        # get src pages from the download center(s)
        if isinstance(url, list or tuple):
            src_urls, src_names = [], []
            for url_ in url:
                logger.info(f"getting the src_urls list of center {url_}...")
                src_urls_, src_names_ = [], []
                src_urls, src_names = self._get_src_urls(url_)
                src_urls += src_urls_
                src_names += src_names_
        else:
            src_urls, src_names = self._get_src_urls(url)
        return src_urls, src_names
    
    @abstractmethod 
    def _get_src_urls(self, url):
        raise NotImplementedError()
        
    @abstractmethod 
    def get_src_from_page(self, url, host_url=None):
        raise NotImplementedError()
    
    # @abstractmethod 
    # def get_nav_item(self, url):
    #     raise NotImplementedError()

    def crawl_src(self, host_url=None, save_path='./'):
        if self.src_store_url is None:
            logger.info(f"{self.name}没有资源下载网页！")
            return
        logger.info(f"Downloading src files for {self.name}...")
        
        src_urls, src_names = self.get_src_urls(self.src_store_url)
        self.get_src_from_store(src_urls, src_names, host_url, save_path)
        
        logger.info(f"Done")
        
        