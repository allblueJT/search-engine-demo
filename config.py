from dataclasses import dataclass
from typing import Tuple

@dataclass
class CrawlerConfig:
    demo: bool = True
    use_hbase: bool = False
    multi_threads: bool = True
    crawlers: Tuple[str] = ('teach', 'sse', 'sist', 'sds', 'scs', 'press', 'mathematics', 'grad')
    save_dir: str = "./cache"
    verbose: bool = True
    debug: bool = False