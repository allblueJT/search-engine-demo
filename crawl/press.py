from crawler import Crawler

class PressCrawler(Crawler):
    def __init__(self, args):
        super().__init__(args)
        self.name = '中国科学技术大学出版社'
        self.main_url = 'https://press.ustc.edu.cn/'
        self.main_page = 'https://press.ustc.edu.cn/main.htm'
        self.src_store_url = [
            'https://press.ustc.edu.cn/tgxz/list.htm',
            'https://press.ustc.edu.cn/xtxxb/list.htm',
            'https://press.ustc.edu.cn/bzgf/list.htm',
            'https://press.ustc.edu.cn/wjfg/list.htm',
            'https://press.ustc.edu.cn/jxzy/list.htm',
        ]
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url]
        self.page_num_xpath = "//em[@class='all_pages']"
        
        # self.store_2_page_list_xpath = "//div[@class='view_bg']//a"
        # self.name_holder = ""
        
        self.check_init()
            
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//div[contains(@class,'node-article')]//a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.text for a in page_src_list]
        
        return src_urls, src_names
            
    def _get_src_from_page(self, element):
        page_src_list = element.xpath("//div[@class='wp_articlecontent']//a[@sudyfile-attr]")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
        return src_urls, src_names
    
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    press = PressCrawler(args)
    # print(f"sse {sse.page_url}")
    press.crawl_src(save_path='../cache/press', host_url=press.main_url)