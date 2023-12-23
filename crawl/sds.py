from .crawler import Crawler
from database import URLContent

class DSCrawler(Crawler):
    def __init__(self, args):
        self.name = '大数据学院官网'
        super().__init__(self.name, args)
        
        self.main_url = 'https://sds.ustc.edu.cn/'
        self.main_page = 'https://sds.ustc.edu.cn/main.htm'
        # self.src_store_url = ['http://sds.ustc.edu.cn/15410/list.htm']
        self.src_store_url = ['https://sds.ustc.edu.cn/15443/list.htm', 'http://sds.ustc.edu.cn/15410/list.htm']
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url]
        self.page_num_xpath = "//em[@class='all_pages']"

        self.title_xpath = "//h1[@class='arti_title']/text()"
        self.date_xpath = "//span[@class='Article_PublishDate']/text()"
        self.article_xpath_prefix = "//div[@class='wp_articlecontent']//"

        self.check_init()

    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)

        src_list = element.xpath("//div[@class='wenzhangliebiao']")[0]
        src_urls = src_list.xpath("//ul[@class='wp_article_list']/li//a/@href")
        src_names = src_list.xpath("//ul[@class='wp_article_list']/li//a/@title")
        src_date = src_list.xpath(self.date_xpath)
        
        rslt = [URLContent(url, date=date, title=title) for url, title, date in zip(src_urls, src_names, src_date)]
        return rslt
        
    def _get_src_from_page(self, element, date):
        try:
            # node a
            a_src = element.xpath("//div[@class='read']//a[@sudyfile-attr]")
            a_href_src = [a.attrib['href'] for a in a_src]
            a_title_src = [eval(a.attrib['sudyfile-attr'])['title'] for a in a_src]
            
            # node div
            div_src = element.xpath("//div[@class='wp_pdf_player']")
            div_href_src = [div.attrib['pdfsrc'] for div in div_src]
            div_title_src = [eval(div.attrib['sudyfile-attr'])['title'] for div in div_src]
            
            all_hrefs = a_href_src + div_href_src
            all_titles = a_title_src + div_title_src
            pages = [URLContent(url=url, date=date, title=name) for url, name \
                in zip(all_hrefs, all_titles)]
        except:
            pages = []
        return pages
    

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    dc = DSCrawler(args)
    dc.crawl_src(save_path='../cache/sds', host_url=dc.main_url)