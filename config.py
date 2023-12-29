from dataclasses import dataclass
from typing import Tuple

@dataclass
class CrawlerConfig:
    demo: bool = True
    use_hbase: bool = True
    multi_threads: bool = False
    # crawlers: Tuple[str] = ('teach', 'sse', 'sist', 'sds', 'scs', 'press', 'mathematics', 'grad')
    """
    teach:教务处 sse:软件学院 sist:信院 sds:大数据 scs:网安 press:出版社 mathematics:数院 grad:学位与研教
    """
    crawlers: Tuple[str] = ('grad', 't')
    save_dir: str = "./cache"
    verbose: bool = True
    debug: bool = False