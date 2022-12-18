import logging
import pickle
import talib as ta
import os
from pathlib import Path

from MACD_Model import macd_train, macd_test
logging.basicConfig(level=logging.INFO)

def calculate_macd(data, *args):
    var = []
    for arg in args:
        var.append(arg)

    return ta.MACD(data, fastperiod=var[0], slowperiod=var[1], signalperiod=var[2])

def macd_init(cfg, stock):

    optimizer_file = str(Path(os.path.dirname(__file__)).parent) + '\\stock_data\\' + stock.Name + r'\macd\vars\optimized_variables.pickle'
    if stock.train:
        max_performance = macd_train.train(stock, cfg)

        try:
            with open(optimizer_file, 'wb') as f:
                pickle.dump(max_performance, f)
            logging.info('> Variables Updated')
        except FileNotFoundError:
            with open(optimizer_file, 'wb') as f:
                pickle.dump(max_performance, f)
            logging.info('> Variables Created')

        logging.info('> (Variables) FILE LOCATION: %s\n' % optimizer_file)
        logging.info('> MACD Optimization Complete')
        

    f = open(optimizer_file, 'rb')
    optimized_vars = pickle.load(f)
    logging.info('> Optimized Variables: \n%s' % optimized_vars)

    if stock.test:
        ret, tc, eoy_signal, buy_signals, sell_signals = macd_test.test(stock, optimized_vars, cfg)

        
        if eoy_signal == 0 and eoy_signal!=stock.initial_signal:
            uret = ret*stock.Test_data['Adj Close'][-1]
            if stock.abs_returns is True:
                ret = uret
        else:
            uret = ret

        return ret, uret, tc, eoy_signal, buy_signals, sell_signals


