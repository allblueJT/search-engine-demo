from .crawler import Crawler, URLContent

class DSCrawler(Crawler):
    def __init__(self, args):
        super().__init__(args)
        self.name = '大数据学院官网'
        self.main_url = 'https://sds.ustc.edu.cn/'
        self.main_page = 'https://sds.ustc.edu.cn/main.htm'
        self.src_store_url = 'https://sds.ustc.edu.cn/15443/list.htm'
        self.page_url = None
        self.title_xpath = "//h1[@class='arti_title']"
        self.article_xpath = "//div[@class='wp_articlecontent']//p"
        self.date_xpath = "//span[@class='Article_PublishDate']/text()"

        self.check_init()

    def get_page_src_urls(self, url):
        element = Crawler.get_etree_html(url)

        src_list = element.xpath("//div[@class='wenzhangliebiao']")[0]
        src_urls = src_list.xpath("//ul[@class='wp_article_list']/li//a/@href")
        src_names = src_list.xpath("//ul[@class='wp_article_list']/li//a/@title")
        src_date = src_list.xpath(self.date_xpath)
        
        rslt = [URLContent(url, date=date, title=title) for url, date, title in zip(src_urls, src_names, src_date)]
        return rslt
        
    def _get_src_from_page(self, element):
                
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

        return all_hrefs, all_titles
    

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from utils import get_args
    
    args = get_args()
    
    dc = DSCrawler(args)
    dc.crawl_src(save_path='../cache/sds', host_url=dc.main_url)