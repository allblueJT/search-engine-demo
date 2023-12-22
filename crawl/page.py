# Not used currently

# from enum import auto, Enum

# class PageType(Enum):
#     List = auto()
#     Source = auto()
#     File = auto()
#     Article = auto()
#     ArticleSource = auto()
#     Blank = auto()

# class BasePage:
#     src_ext = None
#     # host_url = None   # unfit to multi-thread
    
#     def __init__(self, url, title, date=None, type=None):
#         self._url = url
#         self.title = title
#         self.type = type
#         self.date = date
    
#     # @property
#     # def url(self):
#     #     return self._url
#     # @url.setter
#     # def url(self, url):
#     #     self._url = self.host_url + url if url.startswith('/') else url
    
#     @classmethod
#     def isFile(cls, url):
#         ext = url.split('.')[-1]
#         if ext in cls.src_ext:
#             return True
#         return False
    
    
# class SrcPage(BasePage):
#     def __init__(self, url, title, date, src_urls):
#         super().__init__(url, title, date, PageType.Source)
#         self.src_urls = src_urls
        
# class FilePage(BasePage):
#     def __init__(self, url, title, date):
#         super().__init__(url, title, date, PageType.Source)
#         self.ext = self.url.split('.')[-1]
        
# class ListPage(BasePage):
#     def __init__(self, url, title, url_list):
#         super().__init__(url, title, PageType.Source)
#         self.url_list = url_list
    
# class ArticlePage(BasePage):
#     def __init__(self, url, title, date, article):
#         super().__init__(url, title, PageType.Source)
#         self.article = article
    
# class ArticleSourcePage(ArticlePage, SrcPage):
#     def __init__(self, url, title, date, article, src_urls):
#         ArticlePage.__init__(url, title, date, article)
#         SrcPage.__init__(url, title, date, src_urls)
#         self.type = PageType.ArticleSource
