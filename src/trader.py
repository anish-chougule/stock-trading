import logging              # Logging actions
import pandas as pd
import numpy as np
from pathlib import Path
import pickle               # Used to handle strategies
import os
import datetime
import yfinance as yf       # Fetching stock data

import model_trainer
# Includes tools for directory handling, model construction, stock data
from tools import *

from easydict import EasyDict

print("Success")
# Trading on validation/live data.
def trade(ticker, start, end=datetime.datetime.today(), signal=1, abs_returns=True):
    # Inputs = stock name, start and end time for trading, initial signal(1:buy | 0:sell), bool for absolute/unrealized returns

    # Loading best strategy
    strategy_filepath = str(Path(os.path.dirname(__file__))) + \
        '\\stock_data\\' + ticker + r'\strategy\best_strategy.pickle'
    try:
        with open(strategy_filepath, 'rb') as f:
            strategy = pickle.load(f)
    except FileNotFoundError or EOFError:
        logging.error(
            'xxxx Please Train the models and strategize before trading xxxx')
        exit(0)

    logging.info('Optimization and Strategizing Complete.')
    logging.info('> Trading: %s' % ticker)
    logging.info('> Indicator: %s' % strategy.Indicator)

    # Constructing model with best trained strategy
    cfg, stock, model = model_utils.model_constructor(
        ticker, signal, abs_returns, strategy.Indicator, train_test_split=1, start=start, end=end)

    # Trading live
    ret, uret, tc, signal, buy_signals, sell_signals = model(cfg, stock)

    print('\n\nUnrealized Gains: ', uret)
    print('Last signal: %s' % 'Sell' if signal == 0 else 'Buy')
    print('Buy Signals: ', buy_signals) if not buy_signals.empty else 0
    print('Sell Signals: ', sell_signals) if not sell_signals.empty else 0
    print('Trading for %s stock ends here.\n\n\n' % ticker)

    # Returns gains, unrealized gains and last signal
    return ret, uret, signal


def main():

    # Initializing stock name, list of indicators, start and end date
    stock = 'GOOGL'
    indicator_list = ['RSI', 'MACD', 'BBAND']

    start = '2012-01-01'
    points = ['2020-01-01']

    '''
    '2011-01-01',
            '2012-01-01',
            '2013-01-01',
            '2014-01-01', 
            '2015-01-01',
            '2016-01-01',
            '2017-01-01', 
            '2018-01-01',
            '2019-01-01',
    '''

    # Initializing returns list, unrealized returns list, signals list, train-test-split, initial signal and absolute returns(bool).
    ret_df = []
    uret_df = []
    sig_df = []
    _tts_ = 0.75
    signal = 1
    abs_returns = False

    # Passing on to trader
    for end in points:

        # Trackpoint is separating train-test and validation data
        trackpoint = datetime.datetime.strptime(
            end, '%Y-%m-%d') - datetime.timedelta(days=1*365)

        # Developing best strategy (trainging and testing strategies)
        model_trainer.strategize(ticker=stock, indicator_list=indicator_list,
                                 start=start, end=trackpoint, train_test_split=_tts_)

        # Live trading on validation data
        ret, uret, signal = trade(stock, start=trackpoint-datetime.timedelta(
            days=50), end=end, signal=signal, abs_returns=abs_returns)

        ret_df.append(ret)
        uret_df.append(uret)
        sig_df.append(signal)

    # Calculating returns
    print('Return: ', np.prod(np.array(ret_df)) if abs_returns == True else np.prod(
        np.array(ret_df))*stock_utils.getStockHist(stock, trackpoint))
    print('Stock movement: ', stock_utils.getStockMovement(stock, datetime.datetime.strptime(
        points[0], '%Y-%m-%d') - datetime.timedelta(days=365+50), points[-1]))
    print('Unrealized gains: \n', uret_df)
    print('Signals: \n', sig_df)

    dir_utils.clear_cache()


if __name__ == "__main__":
    main()

'''

Guide:
1) Trackpoint: Start date for trading and end date for strategizing 

'''
