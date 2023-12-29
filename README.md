# search-engine-demo
A search engine for infomation of USTC. Course: 大数据系统及综合实验

### To Do
运行python crawl_data.py --use_hbase建立hbase table；MapReduce建立倒排索引；写个后端，接受前端输入，在hbase中根据索引进行搜索，将搜索结果传给前端

### Update

Use the following command get the files from the websites of USTC.
```python
python crawl_data.py --save_dir YOUR_PATH [--use_hbase] [--multi_threads] [--verbose ] [--debug] [--demo]
```

To get the whole dataset stored in HBase for a demo of search engineer, run the following command:
```python
python crawl_data.py --save_dir YOUR_PATH --use_hbase --multi_threads --verbose --demo

python crawl_data.py --save_dir ./cache --use_hbase --verbose --demo
```


***


Use the following command to get the files from the websites of USTC.
```shell
bash download_files.sh
```

For checking the correctness of the implementations of crawlers, use this one:
```shell
bash download_files_debug.sh
```