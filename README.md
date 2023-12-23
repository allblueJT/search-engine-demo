# search-engine-demo
A search engine for infomation of USTC. Course: 大数据系统及综合实验

### Update
Use the following command get the files from the websites of USTC.
```python
python crawl_data.py --save_dir YOUR_PATH [--use_hbase] [--multi_threads] [--verbose ] [--debug] [--demo]
```

To get the whole dataset stored in HBase for a demo of search engineer, run the following command:
```python
python crawl_data.py --save_dir YOUR_PATH --use_hbase --multi_threads --verbose --demo
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