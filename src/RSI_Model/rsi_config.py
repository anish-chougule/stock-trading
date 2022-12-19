import logging
import pickle

import talib as ta
import os
from pathlib import Path

from RSI_Model import rsi_train, rsi_test
logging.basicConfig(level=logging.INFO)

def calculate_rsi(data, var):
    rsi_data = ta.RSI(data, var)
    return rsi_data

def rsi_init(cfg, stock):

    optimizer_file = str(Path(os.path.dirname(__file__)).parent) + '\\stock_data\\' + stock.Name + r'\rsi\vars\optimized_variables.pickle'
    if stock.train:
        max_performance = rsi_train.train(stock, cfg)

        try:
            with open(optimizer_file, 'wb') as f:
                pickle.dump(max_performance, f)
            logging.info('> Variables Updated')
        except FileNotFoundError:
            with open(optimizer_file, 'wb') as f:
                pickle.dump(max_performance, f)
            logging.info('> Variables Created')
        logging.info('> (Variables) FILE LOCATION: %s' % optimizer_file)
        logging.info('> RSI Optimization Complete\n')
        
    f = open(optimizer_file, 'rb')
    optimized_vars = pickle.load(f)
    #optimized_vars = max_performance
    logging.info('> Optimized Variables: \n%s' % optimized_vars)

    if stock.test:
        ret, tc, eoy_signal, buy_signals, sell_signals = rsi_test.test(stock, optimized_vars, cfg)

        if eoy_signal == 0 and eoy_signal!=stock.initial_signal:
            uret = ret*stock.Test_data['Adj Close'][-1]
            if stock.abs_returns is True:
                ret = uret
        else:
            uret = ret

        return ret, uret, tc, eoy_signal, buy_signals, sell_signals
