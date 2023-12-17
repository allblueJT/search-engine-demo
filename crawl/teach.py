from crawler import Crawler

class TeachCrawler(Crawler):
    def __init__(self, args):
        super().__init__(args)
        self.name = '中科大教务处'
        self.main_url = 'https://www.teach.ustc.edu.cn/'
        self.main_page = 'https://www.teach.ustc.edu.cn/main.htm'
        self.src_store_url = 'https://www.teach.ustc.edu.cn/download/all'
        self.page_url = 'https://www.teach.ustc.edu.cn/download/all/page/{id}'
        self.page_num_xpath = "//a[@class='page-numbers' and position()=last()-1]"
        
        self.check_init()
        
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//ul[contains(@class,'download-list')]//span[@class='post']/a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.text for a in page_src_list]
        
        return src_urls, src_names
            
    def _get_src_from_page(self, element):
        a_node = element.xpath("//article/a")[0]
        return [a_node.attrib['href']], [a_node.attrib['download']]


if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    tc = TeachCrawler(args)
    tc.crawl_src(save_path='../cache/teach')