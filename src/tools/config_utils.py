from pathlib import Path
import yaml
from easydict import EasyDict
import os

def merge_new_config(config, new_config):

    for key, val in new_config.items():
        if not isinstance(val, dict):
            config[key] = val
            continue
        if key not in config:
            config[key] = EasyDict()
        merge_new_config(config[key], val)

    return config


def cfg_from_yaml_file(path, config):
    
    print('Configurations Loaded')
    print(path)
    #path = str(Path(os.path.dirname(__file__)).parent) + f'\{cfg_file}'
    
    with open( path, 'r') as f:
        try:
            new_config = yaml.safe_load(f, Loader=yaml.FullLoader)
        except:
            new_config = yaml.safe_load(f)

        merge_new_config(config=config, new_config=new_config)

    return config


cfg = EasyDict()