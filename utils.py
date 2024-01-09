import sys
import logging
import argparse


def get_logger(name, log_filename=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(name)s - %(levelname)s\t%(message)s", datefmt="%Y/%m/%d %H:%M:%S")
    
    shandler = logging.StreamHandler(sys.stdout)
    shandler.setFormatter(formatter)
    logger.addHandler(shandler)
    
    if log_filename is not None:
        fhandler = logging.FileHandler(log_filename, mode='a', encoding='utf8')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        
    return logger
    
def get_args(args={}):
    args = argparse.Namespace(**args)
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_dir", type=str, default='./cache')
    parser.add_argument("--use_hbase", type=bool, default=False)
    parser.add_argument("--multi_threads", type=bool, default=True)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args(namespace=args)
    logging.info(args)
    return args