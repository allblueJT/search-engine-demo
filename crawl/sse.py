from crawler import Crawler

class SSECrawler(Crawler):
    def __init__(self, args):
        super().__init__(args)
        self.name = '中国科学技术大学软件学院'
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
        ]
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url]
        # self.src_store_url = self.src_store_url[:3:2]     # For debug
        # self.page_url = self.page_url[:3:2]
        self.page_num_xpath = "//em[@class='all_pages']"
        
        # self.store_2_page_list_xpath = "//div[@class='view_bg']//a"
        # self.name_holder = ""
        
        self.check_init()
            
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//span[@class='Article_Title']/a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.attrib['title'] if a.attrib.has_key('title') else eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
        
        return src_urls, src_names
            
    def _get_src_from_page(self, element):
        page_src_list = element.xpath("//div[@class='entry']//a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        title_list = element.xpath("//div[@class='entry']//a/span")
        src_names = [node.text for node in title_list]
        return src_urls, src_names
    
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    sse = SSECrawler(args)
    print(f"sse {sse.page_url}")
    sse.crawl_src(save_path='../cache/sse', host_url=sse.main_url)