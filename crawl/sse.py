from .crawler import Crawler
from database import URLContent

class SSECrawler(Crawler):
    def __init__(self, args):
        self.name = '中国科学技术大学软件学院'
        super().__init__(self.name, args)
        
        self.main_url = 'https://sse.ustc.edu.cn/'
        self.main_page = 'https://sse.ustc.edu.cn/main.htm'
        self.src_store_url = [
            'https://sse.ustc.edu.cn/zcwj/list.htm',
            'https://sse.ustc.edu.cn/19878/list.htm',
            'https://sse.ustc.edu.cn/19879/list.htm',
            'https://sse.ustc.edu.cn/19880/list.htm',
            'https://sse.ustc.edu.cn/19882/list.htm',
            'https://sse.ustc.edu.cn/19884/list.htm',
            'https://sse.ustc.edu.cn/19885/list.htm',
            'https://sse.ustc.edu.cn/19740/list.htm',   # news
        ]
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url]
        self.page_num_xpath = "//em[@class='all_pages']"
        
        self.title_xpath = "//h1[@class='arti_title']/text()"
        self.date_xpath = "//span[@class='Article_PublishDate']/text()"
        self.article_xpath_prefix = "//div[@class='wp_articlecontent']//"
        
        self.check_init()
        
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//span[@class='Article_Title']/a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.attrib['title'] if a.attrib.has_key('title') else eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
        src_date = element.xpath(self.date_xpath)
        rslt = [URLContent(url, date=date, title=title) for url, title, date in zip(src_urls, src_names, src_date)]
        return rslt
            
    def _get_src_from_page(self, element, date):
        try:
            page_src_list = element.xpath("//div[@class='entry']//a")
            src_urls = [a.attrib['href'] for a in page_src_list]
            title_list = element.xpath("//div[@class='entry']//a/span")
            src_names = [node.text for node in title_list]
            pages = [URLContent(url=url, date=date, title=name) for url, name \
                in zip(src_urls, src_names)]
        except:
            pages = []
        return pages
    
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    sse = SSECrawler(args)
    print(f"sse {sse.page_url}")
    sse.crawl_src(save_path='../cache/sse', host_url=sse.main_url)