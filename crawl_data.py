import os
from dataclasses import asdict
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from config import CrawlerConfig
from utils import get_args
from crawl import AutoCrawler


args = get_args(asdict(CrawlerConfig()))
crawlers = args.crawlers

if args.multi_threads:
    with ThreadPoolExecutor(len(crawlers)) as t:
        for name in crawlers:
            crawler = AutoCrawler.from_name(name)(args)
            t.submit(
                partial(
                    crawler.crawl_src, 
                    save_path=os.path.join(args.save_dir, name), 
                    host_url=crawler.main_url
                ),
            )
else:
    for name in crawlers:
        crawler = AutoCrawler.from_name(name)(args)
        crawler.crawl_src(save_path=os.path.join(args.save_dir, name), host_url=crawler.main_url)