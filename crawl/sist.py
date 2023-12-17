from crawler import Crawler

class SISTCrawler(Crawler):
    def __init__(self, args):
        super().__init__(args)
        self.name = '信息科学技术学院'
        self.main_url = 'https://sist.ustc.edu.cn/'
        self.main_page = 'https://sist.ustc.edu.cn/main.htm'
        self.src_store_url = [
            'https://sist.ustc.edu.cn/5104/list.htm',       # 研究生
            'https://sist.ustc.edu.cn/5111/list.htm',       # 本科生
            'https://sist.ustc.edu.cn/5128/list.htm',       # 党建
            'https://sist.ustc.edu.cn/5095/list.htm',       # 学生工作
            'https://sist.ustc.edu.cn/5085/list.htm',       # 科学研究
            'https://sist.ustc.edu.cn/5079/list.htm',       # 信息服务
        ]
        self.page_url = [url[:-4] + '{id}' + url[-4:] for url in self.src_store_url[:4]] + \
                        [None, None]    # some centers haven't had more than one page

        # self.max_page_num_xpath = None
        
        # self.store_2_page_list_xpath = "//div[@class='view_bg']//a"
        # self.name_holder = ""
        
    def _get_src_urls(self, url, page_url=None):
        element = self.get_etree_html(url)

        if page_url is None:
            src_urls, src_names = self.get_page_src_urls(url)
        else:
            max_page = element.xpath("//em[@class='all_pages']")[0]
            max_page = int(max_page.text)

            src_urls, src_names = [], []
            for id in range(1, max_page + 1):
                
                page_src_urls, page_names = self.get_page_src_urls(page_url.format(id=id))
                if self.args.verbose:
                    print(f'page: {id}')
                    print(f'page_names: {page_names}')
                src_urls += page_src_urls
                src_names += page_names
        
        return src_urls, src_names
            
    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)
        page_src_list = element.xpath("//h5[contains(@class,'card-title')]/a | //div[@class='wp_entry']//a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [a.attrib['title'] if a.attrib.has_key('title') else eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
        
        return src_urls, src_names
            
    def _get_src_from_page(self, element):
        page_src_list = element.xpath("//div[@class='wp_articlecontent']//a")
        src_urls = [a.attrib['href'] for a in page_src_list]
        src_names = [eval(a.attrib['sudyfile-attr'])['title'] for a in page_src_list]
        return src_urls, src_names

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    sist = SISTCrawler(args)
    sist.crawl_src(host_url=sist.main_url, save_path='../cache/sist')