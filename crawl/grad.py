from .crawler import Crawler
from database import URLContent

class GradCrawler(Crawler):
    def __init__(self, args):
        self.name = '中国科学技术大学学位与研究生教育'
        super().__init__(self.name, args)
        
        self.main_url = 'https://gradschool.ustc.edu.cn/'
        self.main_page = 'https://gradschool.ustc.edu.cn'
        self.center_url = 'https://gradschool.ustc.edu.cn/column/63'
        self.page_url = []
        # self.src_store_url = ['https://gradschool.ustc.edu.cn/column/10']
        self.src_store_url = self.get_src_store_url(self.center_url) + ['https://gradschool.ustc.edu.cn/column/10'] # news
        self.page_num_xpath = "//section[@class='detail-list']//div[@class='r-box']/div/script"
        self.page_url += [self.src_store_url[-1] + '?current={id}']
        self.page_script = True
        
        self.title_xpath = "//div[@class='content-box']//h1/text()"
        self.date_xpath = "//time/text()"
        self.article_xpath_prefix = "//article//"

        self.check_init()
            
    def get_src_store_url(self, url):
        element = Crawler.get_etree_html(url)
        a_more = element.xpath("//div[@class='title']//a")
        urls_more = [a.attrib['href'] for a in a_more]
        a_nav = element.xpath("//ul[@id='detail-list']/li")[0]
        urls_nav = a_nav.xpath("ul/li/@data-link")[1:]
        urls = urls_nav + urls_more
        urls = self.process_urls(urls, self.main_url)
        
        for url_ in urls:
            element_ = Crawler.get_etree_html(url_)
            if element_.xpath("//section[@class='detail-list']//div[@class='r-box']/div"):
                self.page_url.append(url_ + "?current={id}")
            else:
                self.page_url.append(None)
        return urls
            
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//a[@class='a-max-length']")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.text for a in page_src_list]
        src_date = element.xpath(self.date_xpath)
        rslt = [URLContent(url, date=date, title=title) for url, date, title in zip(src_urls, src_date, src_names)]
        
        return rslt
            
    def _get_src_from_page(self, element, date):
        page_src_list = element.xpath("//div[@class='wp_articlecontent']//a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
        pages = [URLContent(url=url, date=date, title=name) for url, name \
            in zip(src_urls, src_names)]
        return pages
    

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    grad = GradCrawler(args)
    # print(f"sse {sse.page_url}")
    grad.crawl_src(save_path='../cache/grad', host_url=grad.main_url)