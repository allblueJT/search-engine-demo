from .crawler import Crawler
from database import URLContent

class MathCrawler(Crawler):
    def __init__(self, args):
        self.name = '数学科学学院'
        super().__init__(self.name, args)
        
        self.main_url = 'https://math.ustc.edu.cn/'
        self.main_page = 'https://math.ustc.edu.cn/main.htm'
        self.src_store_url = [
            'https://math.ustc.edu.cn/bksjy/list.htm',     # 研究生
            'https://math.ustc.edu.cn/yjsjy/list.htm',           # 本科生
            'https://math.ustc.edu.cn/xyxw/list.htm',       # 新闻
        ]
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url]
        self.page_num_xpath = "//em[@class='all_pages']"
        
        # self.store_2_page_list_xpath = "//div[@class='view_bg']//a"
        # self.name_holder = ""
        self.title_xpath = "//h1[@class='arti_title']/text()"
        self.date_xpath = "//span[@class='Article_PublishDate']/text()"
        self.article_xpath_prefix = "//div[@class='wp_articlecontent']//"
        
        self.check_init()

        
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        a_src = element.xpath("//ul[@class='wp_article_list']//span[@class='Article_Title']//a")
        src_urls = [a.attrib['href'] for a in a_src]
        src_names = [a.attrib['title'] for a in a_src]
        src_date = element.xpath(self.date_xpath)
        rslt = [URLContent(url, date=date, title=title) for url, title, date in zip(src_urls, src_names, src_date)]

        return rslt
        
            
    def _get_src_from_page(self, element, date):
        try:
            page_src_list = element.xpath("//div[@class='entry']//a[@sudyfile-attr]")
            src_urls = [a.attrib['href'] for a in page_src_list]
            src_names = [eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
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
    
    math = MathCrawler(args)
    math.crawl_src(save_path='../cache/math', host_url=math.main_url)