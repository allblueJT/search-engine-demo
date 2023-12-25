from .crawler import Crawler
from database import URLContent

class TeachCrawler(Crawler):
    def __init__(self, args):
        self.name = '中科大教务处'
        super().__init__(self.name, args)
        
        self.main_url = 'https://www.teach.ustc.edu.cn/'
        self.main_page = 'https://www.teach.ustc.edu.cn/main.htm'
        self.src_store_url = ['https://www.teach.ustc.edu.cn/download/all','https://www.teach.ustc.edu.cn/category/notice']
        self.page_url = ['https://www.teach.ustc.edu.cn/download/all/page/{id}', 'https://www.teach.ustc.edu.cn/category/notice/page/{id}']

        self.page_num_xpath = "//a[@class='page-numbers' and position()=last()-1]"
        
        self.title_xpath = "//div[contains(@class,'common-title')]//h1//a/text()"
        self.date_xpath = "//span[@class='date']/text()"
        self.article_xpath_prefix = '//article//'
        
        self.check_init()
        
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//ul[contains(@class,'article-list')]//span[@class='post']/a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.text for a in page_src_list]
        src_date = element.xpath("//span[@class='date']/text()")
        rslt = [URLContent(url, date=date, title=title) for url, date, title in zip(src_urls, src_date, src_names)]

        return rslt
            
    def _get_src_from_page(self, element, date):
        a_node = element.xpath("//article/a")
        if a_node:
            a_node = a_node[0]
            page = URLContent(url=a_node.attrib['href'], date=date, title=a_node.attrib['download'])
            return [page]
        else:
            return []


if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    tc = TeachCrawler(args)
    tc.crawl_src(save_path='../cache/teach')