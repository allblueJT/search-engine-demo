from crawler import Crawler


class DSCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.name = '大数据学院官网'
        self.main_url = 'https://sds.ustc.edu.cn/'
        self.src_store_url = 'https://sds.ustc.edu.cn/15443/list.htm'
        
    def get_src_urls(self, url):
        element = self.get_etree_html(url)

        src_list = element.xpath("//div[@class='wenzhangliebiao']")[0]
        src_urls = src_list.xpath("//ul[@class='wp_article_list']/li//a/@href")
        src_names = src_list.xpath("//ul[@class='wp_article_list']/li//a/@title")
        
        return src_urls, src_names
        
    def get_src_from_page(self, url, host_url=None):
        assert host_url is not None or not url.startswith('/'), f"{url} has no prefix while host_url is None!"
        
        element = self.get_etree_html(url)
        
        # node a
        a_src = element.xpath("//div[@class='read']//a")
        a_href_src = [a.attrib['href'] for a in a_src]
        a_title_src = [eval(a.attrib['sudyfile-attr'])['title'] for a in a_src]
        
        # node div
        div_src = element.xpath("//div[@class='wp_pdf_player']")
        div_href_src = [div.attrib['pdfsrc'] for div in div_src]
        div_title_src = [eval(div.attrib['sudyfile-attr'])['title'] for div in div_src]
        
        all_hrefs = a_href_src + div_href_src
        all_titles = a_title_src + div_title_src
        if host_url is not None:
            all_hrefs = [host_url + href if href.startswith('/') else href for href in all_hrefs]
        
        return all_hrefs, all_titles
    

if __name__ == '__main__':
    dc = DSCrawler()
    dc.crawl_src(save_path='../cache/sds')