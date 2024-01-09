import requests, lxml
from lxml import etree
import time
import random
import io
import os, sys
import re
import jsonlines
from abc import ABC, abstractmethod
# sys.path.append("..")

from database import USTCHBase
from utils import get_logger
from database import URLContent, SRC_EXT



class Crawler(ABC):
    hbase: USTCHBase = None
    def __init__(self, name, args):
        self.name = name
        self.main_url = None
        self.main_page = None
        self.src_store_url = None   # urls of downloading/news center
        
        self.args = args
        self.page_url = None        # url format with page num
        self.page_num_xpath = None  # xpath to get max-page-num
        self.page_script = False    # whether max page num is in the <script>
        self.add_title = None      # TO DO
        self.title_xpath = None     # xpath to get title
        self.date_xpath = None      # xpath to get date
        self.article_xpath = None   # xpath to get article
        self.article_xpath_prefix = None    # # xpath to get text(part1)
        self.text_node = ['p', 'p//*', 'ul//li', 'ul//li//*', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']   # xpath to get text(part2)
        
        self.visit_cnt = 0      # to control QPS, not used currently
        self.desc = "Crawler for {name}\n" \
                    "Home page: {main_page}"
        log_dir = f'{self.args.save_dir}/log'
        os.makedirs(log_dir, exist_ok=True)
        self.logger = get_logger(self.name, f'{log_dir}/{self.name}.log')
        if args.hbase and not Crawler.hbase:
            Crawler.hbase = args.hbase
        
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
    

    def check_init(self):
        if isinstance(self.src_store_url, str):
            assert isinstance(self.page_url, (str, type(None))), f"Inconsistent shape of src_store_url and page_url!"
        elif isinstance(self.src_store_url, (list, tuple)):
            assert isinstance(self.page_url, (list, tuple)) and len(self.src_store_url) == len(self.page_url), \
                f"Inconsistent shape of src_store_url and page_url!"
        else:
            raise AssertionError("Invalid type of src_store_url! Str | List[Str] expected")
    
    # def get_title(self, element):
    #     node = element.xpath(self.title_xpath)
    #     return URLContent.clean_title(node[0].text) if len(node) != 0 else None
    
    # def get_article(self, element):
    #     node = element.xpath(self.article_xpath)
    #     return URLContent.clean_article(node[0].text) if len(node) != 0 else None

    # def get_date(self, element):
    #     node = element.xpath(self.date_xpath)
    #     return URLContent.clean_title(node[0].text) if len(node) != 0 else None
    
    def get_article(self, element):
        prefix = self.article_xpath_prefix
        xp = ' | '.join([prefix + p + '/text()' for p in self.text_node])
        texts = element.xpath(xp)
        article = '\n'.join(texts)
        return article
    
    def download_src(self, page, save_path='./'):
        self.sleep()
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        if page.ext in SRC_EXT:
            src = requests.get(page.url)
            page.file = io.BytesIO(src.content).read()
        
        if page.title in os.listdir(save_path):
            self.logger.info(f'>>> {page.title} exists! Pass <<<')
            return
    
        
        if self.args.use_hbase:
            page.save_in_hbase(self.hbase)
        else:
            if page.file:
                fname = os.path.join(save_path, page.title)
                with open(fname, 'wb') as f:
                    f.write(page.file)
            elif page.article:
                fname = os.path.join(save_path, page.title + '.txt')
                with open(fname, 'w') as f:
                    f.write(page.article)
            else:
                # raise RuntimeError("Article and File are both empty!")
                self.logger.warning(f"Page:{page.url} - Article and File are both empty! pass")
                return
            with jsonlines.open(os.path.join(save_path, 'meta.jsonl'), 'a') as f:
                f.write(page.as_meta_dict())
            self.logger.info(f'>>> {fname} has been downloaded <<<')
        
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
            if self.args.verbose:
                self.logger.info(f"Downloading from src page {cnt} - {page.url} - Current EXT: {page.ext}")
                
            if page.ext not in SRC_EXT:     # url directs to a page but not src file
                pages_ = self.get_src_from_page(page, host_url=host_url)
                if self.args.verbose:
                    self.logger.info(f"Files of current page: {[page_.title for page_ in pages_]}")
                for page_ in pages_:
                    self.download_src(page_, save_path)
                self.download_src(page, save_path)
            else:
                self.download_src(page, save_path)
            
            if self.args.debug and cnt >= 1:
                break
    
    def get_src_urls(self, url, host_url=None):
        # get src pages from the download center(s)
        if isinstance(url, (list, tuple)):
            pages = []
            for url_, page_url_ in zip(url, self.page_url):
                self.logger.info(f"Getting the src_urls list of center {url_}...")
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
                max_page = element.xpath(self.page_num_xpath)
                if not max_page:
                    self.logger.info(f"Page {url} has no items! pass")
                    return []
                max_page = int(max_page[0].text)
            
            if self.args.demo:
                max_page = min(max_page, 3)
                self.logger.info(f"Url {url} has {max_page} pages totally. Set to {max_page} for the simplity of a demo.")
                
            if self.args.debug:
                max_page = min(max_page, 1)
                self.logger.info(f"Url {url} has {max_page} pages totally. Set to {max_page} under debug mode.")
                
            
                
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
    def _get_src_from_page(self, element, date):
        # Get resource files from a src-page
        raise NotImplementedError()
    
    def get_src_from_page(self, page, host_url=None):
        page.url = self.process_urls(page.url, host_url)
        element = Crawler.get_etree_html(page.url)
        page.article = self.get_article(element)
        title_ = element.xpath(self.title_xpath)
        if title_:
            page.title = title_[0]
        file_pages = self._get_src_from_page(element, page.date)
        for page_ in file_pages:
            page_.url = self.process_urls(page_.url, host_url)
        return file_pages
    
    # @abstractmethod 
    # def get_nav_item(self, url):
    #     raise NotImplementedError()

    def crawl_src(self, host_url=None, save_path='./'):
        if self.src_store_url is None:
            self.logger.info(f"{self.name} has no download center!")
            return

        self.logger.info(f"Downloading src files for {self.name}...")
        
        pages = self.get_src_urls(self.src_store_url, host_url)
        self.get_src_from_store(pages, host_url, save_path)
        
        self.logger.info(f"Done")

        
        