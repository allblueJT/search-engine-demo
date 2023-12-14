from crawler import Crawler
from tqdm import tqdm

class TeachCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.name = '中科大教务处'
        self.main_url = 'https://www.teach.ustc.edu.cn/'
        self.src_store_url = 'https://www.teach.ustc.edu.cn/download/all'
        self.page_url = 'https://www.teach.ustc.edu.cn/download/all/page/{id}'
        
    def get_src_urls(self, url):
        element = self.get_etree_html(url)

        max_page = element.xpath("//a[@class='page-numbers' and position()=last()-1]")[0]
        max_page = int(max_page.text)

        src_urls, src_names = [], []
        # for id in range(1, max_page + 1):
        for id in range(1, 1 + 1):
            # print('page: 1')
            page_url = self.page_url.format(id=id)
            page_src_urls, page_names = self.get_page_src_urls(page_url)
            # print('page_names: ', page_names)
            src_urls += page_src_urls
            src_names += page_names
        
        return src_urls, src_names
            
    def get_page_src_urls(self, url):
        element = self.get_etree_html(url)
        page_src_list = element.xpath("//ul[contains(@class,'download-list')]//span[@class='post']/a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.text for a in page_src_list]
        
        return src_urls, src_names
            
    def get_src_from_page(self, url, host_url=None):
        assert host_url is not None or not url.startswith('/'), f"{url} has no prefix while host_url is None!"
        
        element = self.get_etree_html(url)
        a_node = element.xpath("//article/a")[0]
        return [a_node.attrib['href']], [a_node.attrib['download']]


if __name__ == '__main__':
    tc = TeachCrawler()
    tc.crawl_src(save_path='../cache/teach')