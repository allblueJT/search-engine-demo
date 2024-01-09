# search-engine-demo
A search engine for infomation of USTC. Course: 大数据系统及综合实验


### Update

Use the following command get the files from the websites of USTC.
```python
python crawl_data.py [--save_dir YOUR_PATH] [--use_hbase False] [--multi_threads True] [--verbose] [--debug] [--demo]
```

**Store locally:**
```python
python crawl_data.py --save_dir YOUR_PATH [--multi_threads True] [--verbose] [--debug] [--demo]
```

**Store in HBase:**
```python
python crawl_data.py --use_hbase True [--multi_threads True] [--verbose] [--demo]
```

You can change the settings in the config.py instead of indicating in the command.

TODO

Implement the functionalities of RAG and finetuning LLMs using the articles as datasets in the directories 'ft' and 'rag'.

***

The Code Below Is Not Used Now

Use the following command to get the files from the websites of USTC.
```shell
bash download_files.sh
```

For checking the correctness of the implementations of crawlers, use this one:
```shell
bash download_files_debug.sh
```