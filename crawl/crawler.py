import requests, lxml
from lxml import etree
import time
import random
import io
import logging
import os, sys
import re
from abc import ABC, abstractmethod
from tqdm import tqdm
from typing import List, Dict
from database import USTCHBase

sys.path.append("..")

from utils import get_logger, get_args

logger = get_logger(__name__, 'crawler.log')

# class Sleep:
#     def __init__(self, func):
#         self.func = func
#         self.visit_cnt = 0
    
#     def __call__(self, *args, **kwargs):
#         if self.visit_cnt > 4:
#             time.sleep(2 + random.random() * 4)
#         else:
#             self.visit_cnt += 1
#         self.func(*args, **kwargs)

class URLContent:
    def __init__(self, url: str, date: str = None, title: str = None, article: str = None, file: bytes = None):
        self.url = url
        self._date = date
        self._title = title
        self._article = article
        self._file = file
        
    @property
    def date(self):
        return self._data
    @date.setter
    def date(self, d):
        self._date = d.encode('utf-8')
    

class Crawler(ABC):
    def __init__(self, args):
        self.name = None
        self.main_url = None
        self.main_page = None
        self.src_store_url = None
        self.src_ext = ['doc', 'docx', 'pdf', 'txt', 'xlsx', 'xls', 'ppt', 'zip', 'tar', '7z', 'rar',
                        'png', 'jpg', 'gif', 'jpeg']
        
        self.args = args
        self.page_url = None
        self.page_num_xpath = None
        self.page_script = False    # whether max page num is in the <script>
        self.add_title = None      # TO DO
        # self.store_2_page_list_xpath = None
        # self.download_page_2_file_xpath = None
        self.title_xpath = None
        self.date_xpath = None
        self.article_xpath = None
        
        self.visit_cnt = 0      # to control QPS, not used currently
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
    
    @staticmethod
    def clean_title(text):
        return text.replace(' ', '').replace('\n', '').replace('\r', ''). \
            replace('<br>', '_').replace('<br/>', '_').replace('<br />', '_').replace('\t', '_')
    @staticmethod
    def clean_article(text):
        return text.strip().replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n').replace('\t', ' ').strip()
    
    def check_init(self):
        if isinstance(self.src_store_url, str):
            assert isinstance(self.page_url, (str, type(None))), f"Inconsistent shape of src_store_url and page_url!"
        elif isinstance(self.src_store_url, (list, tuple)):
            assert isinstance(self.page_url, (list, tuple)) and len(self.src_store_url) == len(self.page_url), \
                f"Inconsistent shape of src_store_url and page_url!"
        else:
            raise AssertionError("Invalid type of src_store_url! Str | List[Str] expected")
    
    def get_title(self, element):
        node = element.xpath(self.title_xpath)
        return Crawler.clean_title(node[0].text) if len(node) != 0 else None
    
    def get_article(self, element):
        node = element.xpath(self.article_xpath)
        return Crawler.clean_article(node[0].text) if len(node) != 0 else None

    def get_date(self, element):
        node = element.xpath(self.date_xpath)
        return Crawler.clean_title(node[0].text) if len(node) != 0 else None
    
    def download_src(self, url, ext, name, save_path='./'):
        self.sleep()
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        if ext not in self.src_ext:
            logger.info(f"Illegal ext to download: {url}")
            return
        # self.visit_cnt = Crawler.sleep(self.visit_cnt)
        
        src = requests.get(url)
        content = io.BytesIO(src.content)
        
        name = Crawler.clean_title(name)
        if name.split('.')[-1] not in self.src_ext:
            name = name + '.' + ext
        if name in os.listdir(save_path):
            logger.info(f'>>> {name} exists! Pass <<<')
            return
    
        fname = os.path.join(save_path, name)
        with open(fname, 'wb') as f:
            f.write(content.read())
        logger.info(f'>>> {fname} has been downloaded <<<')
        
    def process_urls(self, urls, host_url):
        if isinstance(urls, (list, tuple)):
            assert host_url is not None or all([not url.startswith('/') for url in urls]), \
                f"{urls} contains some urls without prefix while host_url is None!"
        else:
            assert host_url is not None or not urls.startswith('/'), \
                f"{urls} has no prefix while host_url is None!"
        if host_url is not None:
            if isinstance(urls, str):
                urls = host_url + urls if urls.startswith('/') else urls
            else:
                urls = [host_url + url if url.startswith('/') else url for url in urls]
        return urls
        
    def get_src_from_store(self, pages, host_url=None, save_path='./'):

        for cnt, page in enumerate(pages):
            url = page.url
            name = page.title
            ext = url.split('.')[-1]
            if self.args.verbose:
                logger.info(f"Downloading from src page {cnt} - {url} - Current EXT: {ext}")
                
            if ext not in self.src_ext:     # url directs to a page but not src file
                cur_src_urls, cur_src_names = self.get_src_from_page(url, host_url=host_url)
                if self.args.verbose:
                    logger.info(f"Files of current page: {list(zip(cur_src_names, cur_src_urls))}")
                for url_, name_ in zip(cur_src_urls, cur_src_names):
                    ext_ = url_.split('.')[-1]
                    self.download_src(url_, ext_, name_, save_path)
            else:
                self.download_src(url, ext, name, save_path)
            
            if self.args.debug and cnt >= 1:
                break
    
    def get_src_urls(self, url, host_url=None):
        # get src pages from the download center(s)
        if isinstance(url, (list, tuple)):
            pages = []
            for url_, page_url_ in zip(url, self.page_url):
                logger.info(f"Getting the src_urls list of center {url_}...")
                pages_ = []
                pages_ = self._get_src_urls(url_, page_url_)
                pages += pages_
        else:
            pages = self._get_src_urls(url, self.page_url)
        for page in pages:
            page.url = self.process_urls(page.url, host_url)
        return pages
    
    def _get_src_urls(self, url, page_url=None):
        element = self.get_etree_html(url)

        if page_url is None:
            pages = self.get_page_src_urls(url)
        else:
            if self.page_script:
                script = element.xpath(self.page_num_xpath)[1].text
                
                max_page = int(re.search("total.*?'(\d+)'", script).group(1))
            else:
                max_page = element.xpath(self.page_num_xpath)[0]
                max_page = int(max_page.text)
            
            
            if self.args.debug:
                max_page = min(max_page, 2)
                logger.info(f"{max_page} pages totally. Set to {max_page} under debug mode.")
                
            pages = []
            for id in range(1, max_page + 1):
                pages_ = self.get_page_src_urls(page_url.format(id=id))
                if self.args.verbose:
                    print(f'page: {id}')
                    print(f'page_names: {[page.title for page in pages_]}')
                pages += pages_
        
        return pages
    
    @abstractmethod 
    def get_page_src_urls(self, url):
        # Get src-pages from a list-page
        raise NotImplementedError()
        
    @abstractmethod 
    def _get_src_from_page(self, element):
        # Get resource files from a src-page
        raise NotImplementedError()
    
    def get_src_from_page(self, url, host_url=None):
        url = self.process_urls(url, host_url)
        element = Crawler.get_etree_html(url)
        src_urls, src_names = self._get_src_from_page(element)
        src_urls = self.process_urls(src_urls, host_url)
        return src_urls, src_names
    # @abstractmethod 
    # def get_nav_item(self, url):
    #     raise NotImplementedError()

    def crawl_src(self, host_url=None, save_path='./'):
        if self.src_store_url is None:
            logger.info(f"{self.name} has no download center!")
            return

        if self.args.use_hbase:
            with USTCHBase(host='localhost') as hbase:
                self.hbase = hbase
                logger.info(f"Downloading src files for {self.name}...")
                
                pages = self.get_src_urls(self.src_store_url, host_url)
                # logger.info(f"All src pages: \n{list(zip(src_names, src_urls))}")
                self.get_src_from_store(pages, host_url, save_path)
                
                logger.info(f"Done")
                del self.hbase
        else:
            logger.info(f"Downloading src files for {self.name}...")
                
            pages = self.get_src_urls(self.src_store_url, host_url)
            # logger.info(f"All src pages: \n{list(zip(src_names, src_urls))}")
            self.get_src_from_store(pages, host_url, save_path)
            
            logger.info(f"Done")
        
        