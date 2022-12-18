import pickle
import logging
from easydict import EasyDict
from pathlib import Path
import os
import warnings
import datetime

from tools import *
logging.basicConfig(level=logging.INFO)
warnings.filterwarnings("ignore")

def strategize(ticker, indicator_list=['RSI', 'MACD', 'BBAND'], start=datetime.datetime.now()-datetime.timedelta(days=10*365), end=datetime.datetime.today(), train_test_split=100):

    dir_utils.create_dir(ticker)

    signal = 1
    best_strategy = EasyDict({'Indicator':'None', 'Returns':-1, 'Unrealized Gains':-1, 'Trade Count':-1})
    for indicator in indicator_list:
        logging.info('> Trading: %s' % ticker)
        logging.info('> Indicator: %s' % indicator)

        abs_returns = True
        cfg, stock, model = model_utils.model_constructor(ticker, signal, abs_returns, indicator, train_test_split=train_test_split, start=start, end=end)

        ret, uret, tc, avgDays, buy_signals, sell_signals = model(cfg, stock)
        
        strategy_returns = EasyDict({'Indicator':indicator, 'Returns':ret, 'Unrealized Gains':uret, 'Trade Count':tc})
        if strategy_returns.Returns > best_strategy.Returns:
            best_strategy = strategy_returns
        
        print('\n')

    start_date = stock.Test_start
    end_date = stock.Test_end
    
    
    logging.info('> Strategy:\n%s' % best_strategy)
    logging.info('> **** from %s to %s ****\n\n', start_date, end_date)
    

    strategy_filepath = str(Path(os.path.dirname(__file__))) + '\\stock_data\\' + stock.Name + r'\strategy\best_strategy.pickle'
    try:
        with open(strategy_filepath, 'wb') as f:
            pickle.dump(best_strategy, f)
        logging.info('> Strategy Updated')
    except FileNotFoundError or EOFError:
        with open(strategy_filepath, 'wb') as f:
            pickle.dump(best_strategy, f)
        logging.info('> Strategy Created')

    #dir_utils.clear_cache()