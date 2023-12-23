from .crawler import Crawler
from database import URLContent

class PressCrawler(Crawler):
    def __init__(self, args):
        self.name = '中国科学技术大学出版社'
        super().__init__(self.name, args)
        
        self.main_url = 'https://press.ustc.edu.cn/'
        self.main_page = 'https://press.ustc.edu.cn/main.htm'
        self.src_store_url = [
            'https://press.ustc.edu.cn/tgxz/list.htm',
            'https://press.ustc.edu.cn/xtxxb/list.htm',
            'https://press.ustc.edu.cn/bzgf/list.htm',
            'https://press.ustc.edu.cn/wjfg/list.htm',
            'https://press.ustc.edu.cn/jxzy/list.htm',
            'https://press.ustc.edu.cn/snxw/list.htm',  # news
        ]
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url]
        self.page_num_xpath = "//em[@class='all_pages']"
        
        # self.store_2_page_list_xpath = "//div[@class='view_bg']//a"
        # self.name_holder = ""
        self.title_xpath = "//h1[@class='title']/text()"
        self.date_xpath = "//div[@class='submitted']/text()"
        self.article_xpath_prefix = "//div[@class='wp_articlecontent']//"

        self.check_init()
            
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//div[contains(@class,'node-article')]//a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.text for a in page_src_list]
        src_date = element.xpath(self.date_xpath)
        rslt = [URLContent(url, date=date, title=title) for url, title, date in zip(src_urls, src_names, src_date)]

        return rslt
            
    def _get_src_from_page(self, element, date):
        try:
            page_src_list = element.xpath("//div[@class='wp_articlecontent']//a[@sudyfile-attr]")
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
    
    press = PressCrawler(args)
    # print(f"sse {sse.page_url}")
    press.crawl_src(save_path='../cache/press', host_url=press.main_url)