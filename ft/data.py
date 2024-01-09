import datasets
from typing import List
from database import USTCHBase, URLContent

def get_content_from_hbase(hbase: USTCHBase, table_name: str) -> List[URLContent]:
    pass

def process_content(pages: List[URLContent]) -> List[str]:
    pass

def get_dataset(hbase):
    content = get_content_from_hbase(hbase, 'ustc')
    dataset = process_content(content)
    return dataset