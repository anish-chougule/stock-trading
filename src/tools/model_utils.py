from tools import config_utils, dir_utils, stock_utils
from easydict import EasyDict
import datetime

from MACD_Model.macd_config import macd_init
from RSI_Model.rsi_config import rsi_init
from BBAND_Model.bband_config import bband_init


def model_constructor(stock_ticker, signal, abs_returns, technical_indicator, train_test_split=0, start=datetime.datetime.now()-datetime.timedelta(days=10*365), end=datetime.datetime.today()):

    # Collect model files
    cfg_files = dir_utils.get_yaml()

    # Create a dictionary of models
    # P.S: clear this so technical indicator var directly calls model from yaml.
    model_dict = EasyDict(
        {'BBAND': {'cfg': cfg_files[0], 'model': bband_init}})
    model_dict.update({'MACD': {'cfg': cfg_files[1], 'model': macd_init}})
    model_dict.update({'RSI': {'cfg': cfg_files[2], 'model': rsi_init}})

    # Selecting model that variable called for.
    cfg_file = model_dict[technical_indicator].cfg
    model = model_dict[technical_indicator].model

    cfg = EasyDict()

    # Constructing model from their instruction files and configuration files
    stock = stock_utils.getStockData(
        stock_ticker, signal, abs_returns, train_test_split, start, end)
    cfg = config_utils.cfg_from_yaml_file(cfg_file, cfg)

    return cfg, stock, model
