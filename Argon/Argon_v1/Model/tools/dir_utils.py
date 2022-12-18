from pathlib import Path
import yaml
from easydict import EasyDict
import os, fnmatch
import pathlib
from tools import config
import logging

def clear_cache():
    [p.unlink() for p in pathlib.Path('..').rglob('*.py[co]')]
    [p.rmdir() for p in pathlib.Path('..').rglob('__pycache__')]

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def get_yaml():
    return find('*.yaml', Path(os.path.dirname(__file__)).parent)

def create_dir(stock):
    yaml_files = get_yaml()
    print(yaml_files)
    cfg_list = []
    cfg = EasyDict()
    for file in yaml_files:
        with open( file, 'rb') as f:
            temp = yaml.safe_load(f)
            cfg = config.merge_new_config(config=cfg, new_config=temp)
            name = cfg.NAME
        cfg_list.append({'Name': cfg.INDICATOR, 'Config': cfg})
        cfg.clear()

    # Checking for Stock Data
    path = Path(os.path.dirname(__file__)).parent / 'stock_data' / stock
    try: 
        os.mkdir(path) 
    except OSError as error: 
        logging.info('%s already exists.' % stock)
    
    # Checking for model variables and logs in Stock Data        
    for cfg in cfg_list:
        name = cfg['Name']
        cfg = cfg['Config']
        err = 0

        try: 
            os.mkdir(str(path)+ '//' + name)
        except OSError as error: 
            err += 1
        
        try:
            os.mkdir(str(path)+ '//' + name +'//' +'logs')
        except OSError as error: 
            err += 1

        try:
            os.mkdir(str(path)+ '//' + name +'//'  +'vars')
        except OSError as error: 
            err += 1

        try:
            os.mkdir(str(path)+ '//' + 'strategy')
        except OSError as error: 
            err += 1

        if err>0 and err<3:
            logging.warning( '> Some configuration files were missing, we recommend training this stock again.')
                

