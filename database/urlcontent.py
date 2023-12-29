import html

SRC_EXT = ['doc', 'docx', 'pdf', 'txt', 'xlsx', 'xls', 'ppt', 'zip', 'tar', '7z', 'rar',
                        'png', 'jpg', 'gif', 'jpeg']

class URLContent:
    def __init__(self, url: str, date: str = '', title: str = '', article: str = '', file: bytes = b''):
        self._url = url
        self.ext = url.split('.')[-1]
        self._date = URLContent.clean_title(date)
        self._title = URLContent.clean_title(title)
        if self.ext in SRC_EXT and self._title.split('.')[-1] not in SRC_EXT:
            self._title = self._title + '.' + self.ext
        self._article = URLContent.clean_article(article)
        self.file = file
        
    def __dict__(self):
        return {
                'cf0:date': self.date,
                'cf0:title': self.title,
                'cf0:article': self.article,
                'cf0:file': self.file,
            }
        
    def as_meta_dict(self):
        return {
                'url': self.url,
                'date': self.date,
                'title': self.title,
            }
    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, d):
        self._date = URLContent.clean_title(d)
    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, t):
        t = URLContent.clean_title(t)
        if hasattr(self, 'ext') and self.ext in SRC_EXT and t.split('.')[-1] not in SRC_EXT:
            self._title = t + '.' + self.ext
    @property
    def article(self):
        return self._article
    @article.setter
    def article(self, a):
        a = URLContent.clean_article(a)
        self._article = a
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, url):
        self.ext = url.split('.')[-1]
        self._url = url
        
    @staticmethod
    def clean_title(text):
        return text.replace(' ', '').replace('\n', '').replace('\r', ''). \
            replace('<br>', '_').replace('<br/>', '_').replace('<br />', '_').replace('\t', '_')
    @staticmethod
    def clean_article(text):
        text = html.unescape(text)
        return text.strip().replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n').\
            replace('\t', ' ').replace(u'\xa0', '').strip()
    
    def save_in_hbase(self, hbase):
        
        if self.article and len(self.article) < 15:     # Filter the blank download page
            return
        hbase.put(self.url, self.__dict__())