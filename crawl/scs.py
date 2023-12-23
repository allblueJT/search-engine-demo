from .crawler import Crawler
from database import URLContent

class SCSCrawler(Crawler):
    def __init__(self, args):
        self.name = '网络空间安全学院'
        super().__init__(self.name, args)
        
        self.main_url = 'https://cybersec.ustc.edu.cn/'
        self.main_page = 'https://cybersec.ustc.edu.cn/main.htm'
        self.src_store_url = [
            'https://cybersec.ustc.edu.cn/zlxz_23830/list.htm',     # 研究生
            'https://cybersec.ustc.edu.cn/zlxz/list.htm',           # 本科生
            'https://cybersec.ustc.edu.cn/zlxz_34997/list.htm',     # 学工
            'https://cybersec.ustc.edu.cn/xwdt/list.htm',   # news
        ]
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url]
        self.page_num_xpath = "//em[@class='all_pages']"
        
        # self.store_2_page_list_xpath = "//div[@class='view_bg']//a"
        # self.name_holder = ""
        self.title_xpath = "//div[@class='title']/span/text()"
        self.date_xpath = "//div[@class='fr time']/text()"
        self.article_xpath_prefix = "//div[@class='wp_articlecontent']//"
        
        self.check_init()

    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        a_src = element.xpath("//div[@id='wp_news_w50']//a")
        titles = element.xpath("//div[@id='wp_news_w50']//a//div[@class='fl text txtov']/text()")
        src_urls = [a.attrib['href'] for a in a_src]
        src_names = [title.strip() for title in titles if title.strip()]
        src_date = element.xpath(self.date_xpath)
        rslt = [URLContent(url, date=date, title=title) for url, title, date in zip(src_urls, src_names, src_date)]
        
        return rslt
            
    def _get_src_from_page(self, element, date):
        try:
            page_src_list = element.xpath("//div[@class='text']//a[@sudyfile-attr]")
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
    
    scs = SCSCrawler(args)
    scs.crawl_src(save_path='../cache/scs', host_url=scs.main_url)