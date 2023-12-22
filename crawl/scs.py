from .crawler import Crawler

class SCSCrawler(Crawler):
    def __init__(self, args):
        super().__init__(args)
        self.name = '网络空间安全学院'
        self.main_url = 'https://cybersec.ustc.edu.cn/'
        self.main_page = 'https://cybersec.ustc.edu.cn/main.htm'
        self.src_store_url = [
            'https://cybersec.ustc.edu.cn/zlxz_23830/list.htm',     # 研究生
            'https://cybersec.ustc.edu.cn/zlxz/list.htm',           # 本科生
            'https://cybersec.ustc.edu.cn/zlxz_34997/list.htm',     # 学工
        ]
        self.page_url = [None] * len(self.src_store_url)
        
        # self.store_2_page_list_xpath = "//div[@class='view_bg']//a"
        # self.name_holder = ""
        self.title_xpath = "//div[@class='title']/span/text()"
        self.article_xpath = "//div[@class='wp_articlecontent']//p"
        self.date_xpath = "//div[@class='fr time']/text()"
        
        self.check_init()
        
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        a_src = element.xpath("//div[@id='wp_news_w50']//a")
        # div_title_src = element.xpath("//div[@class='view_bg']//a//div[@class='fl text txtov']")
        src_urls = [a.attrib['href'] for a in a_src]
        # src_names = [div.text for div in div_title_src]
        src_names = [""] * len(src_urls)

        return src_urls, src_names
            
    def _get_src_from_page(self, element):
        page_src_list = element.xpath("//div[@class='text']//a[@sudyfile-attr]")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
        
        return src_urls, src_names

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    scs = SCSCrawler(args)
    scs.crawl_src(save_path='../cache/scs', host_url=scs.main_url)