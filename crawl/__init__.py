from .grad import GradCrawler
from .mathematics import MathCrawler
from .press import PressCrawler
from .scs import SCSCrawler
from .sds import DSCrawler
from .sist import SISTCrawler
from .sse import SSECrawler
from .teach import TeachCrawler
 

NAME_TO_CRAWLER = dict([
    ('teach', TeachCrawler),
    ('sse', SSECrawler),
    ('sist', SISTCrawler),
    ('sds', DSCrawler),
    ('scs', SCSCrawler),
    ('press', PressCrawler),
    ('mathematics', MathCrawler),
    ('grad', GradCrawler),
])

class AutoCrawler:
    @classmethod
    def from_name(cls, name):
        assert name in NAME_TO_CRAWLER, "No such crawler!"
        return NAME_TO_CRAWLER[name]