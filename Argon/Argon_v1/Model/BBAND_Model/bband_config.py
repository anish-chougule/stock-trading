import logging
import pickle
import talib as ta
import os
from pathlib import Path

from BBAND_Model import bband_train, bband_test
logging.basicConfig(level=logging.INFO)

def calculate_bband(data, *args):
    var = []
    for arg in args:
        var.append(arg)

    return ta.BBANDS(data, timeperiod=var[0], nbdevup=var[1], nbdevdn=var[2])
    
def bband_init(cfg, stock):

    optimizer_file = str(Path(os.path.dirname(__file__)).parent) + '\\stock_data\\' + stock.Name + r'\bband\vars\optimized_variables.pickle'

    if stock.train:
        max_performance = bband_train.train(stock, cfg)

        try:
            with open(optimizer_file, 'wb') as f:
                pickle.dump(max_performance, f)
            logging.info('> Variables Updated')
        except FileNotFoundError:
            with open(optimizer_file, 'wb') as f:
                pickle.dump(max_performance, f)
            logging.info('> Variables Created')

        logging.info('> (Variables) FILE LOCATION: %s\n' % optimizer_file)
        logging.info('> BBAND Optimization Complete\n')
        

    f = open(optimizer_file, 'rb')
    optimized_vars = pickle.load(f)
    logging.info('> Optimized Variables: \n%s' % optimized_vars)

    if stock.test:
        ret, tc, eoy_signal, buy_signals, sell_signals = bband_test.test(stock, optimized_vars, cfg)

        
        if eoy_signal == 0 and eoy_signal!=stock.initial_signal:
            uret = ret*stock.Test_data['Adj Close'][-1]
            if stock.abs_returns is True:
                ret = uret
        else:
            uret = ret

        return ret, uret, tc, eoy_signal, buy_signals, sell_signals

