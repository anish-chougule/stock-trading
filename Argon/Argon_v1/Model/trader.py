import logging
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import os
import datetime
import yfinance as yf

import model_trainer
from tools import *


def trade(ticker, start, end=datetime.datetime.today(), signal=1, abs_returns=True):
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
    cfg, stock, model = model_utils.model_constructor(
        ticker, signal, abs_returns, strategy.Indicator, train_test_split=1, start=start, end=end)

    ret, uret, tc, signal, buy_signals, sell_signals = model(cfg, stock)

    data = yf.download(stock.Name, end=end)
    print('\n\nUnrealized Gains: ', uret)
    print('Last signal: %s' % 'Sell' if signal == 0 else 'Buy')
    print('Buy Signals: ', buy_signals) if not buy_signals.empty else 0
    print('Sell Signals: ', sell_signals) if not sell_signals.empty else 0
    print('Trading for %s stock ends here.\n\n\n' % ticker)
    return ret, uret, signal


def main():
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

    ret_df = []
    uret_df = []
    sig_df = []
    _tts_ = 0.75
    signal = 1
    abs_returns = False

    for end in points:
        trackpoint = datetime.datetime.strptime(
            end, '%Y-%m-%d') - datetime.timedelta(days=1*365)
        model_trainer.strategize(ticker=stock, indicator_list=indicator_list,
                                 start=start, end=trackpoint, train_test_split=_tts_)
        ret, uret, signal = trade(stock, start=trackpoint-datetime.timedelta(
            days=50), end=end, signal=signal, abs_returns=abs_returns)
        ret_df.append(ret)
        uret_df.append(uret)
        sig_df.append(signal)

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
2) 

'''
