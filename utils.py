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
    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", type=bool, default=False)
    parser.add_argument("--verbose", type=bool, default=True)
    args = parser.parse_args()
    return args