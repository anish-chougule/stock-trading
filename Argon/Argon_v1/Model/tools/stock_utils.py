from math import floor
import pandas as pd
import yfinance as yf
import datetime
from easydict import EasyDict
import logging

def getStockData(ticker, signal=1, abs_ret=True, train_test_split=0, start=datetime.datetime.now()-datetime.timedelta(days=10*365), end=datetime.datetime.today()):
    data = yf.download(ticker, start=start, end=end, progress=False)
    data_len = len(data)
    logging.info('> Stock price history fetched...')

    if train_test_split>0 and train_test_split<=1 :
        testing_len = floor(train_test_split * data_len)
        training_data = data[:data_len-testing_len]
        testing_data = data[data_len-testing_len:]

    elif train_test_split>1 and train_test_split<data_len:
        testing_len = floor(train_test_split)
        training_data = data[:data_len-testing_len]
        testing_data = data[data_len-testing_len:]
        
    else:
        testing_len = 0
        training_data = data
        testing_data = pd.DataFrame(columns=list(data.columns))
        logging.info("> Dates are invalid or stock didn't exist then, please try again...")
        exit(0)
        
    if testing_len<data_len:
        train_start = training_data.index.to_list()[0]
        train_end = training_data.index.to_list()[-1]
        test_start = testing_data.index.to_list()[0]
        test_end = testing_data.index.to_list()[-1]
    elif testing_len==data_len:
        train_start = '00-00-00'
        train_end = '00-00-00'
        test_start = testing_data.index.to_list()[0]
        test_end = testing_data.index.to_list()[-1]

    df = EasyDict({'Name' : ticker,
          'initial_signal': signal,
          'abs_returns'   : abs_ret,
          'train'         : True if testing_len!=data_len else False,
          'test'          : False if testing_len==0 else True,
          'Test_data'     : testing_data,
          'Train_data'    : training_data,
          'Train_start'   : str(train_start).split(' ')[0],
          'Train_end'     : str(train_end).split(' ')[0],
          'Test_start'    : str(test_start).split(' ')[0],
          'Test_end'      : str(test_end).split(' ')[0]})

    logging.info('> Stock data Initialized.')
    return df

def getStockHist(stock, date):
    return yf.download(stock, end=date, progress=False)['Adj Close'][-1]

def getStockMovement(stock, start, end):
    Adj_close = yf.download(stock, start, end, progress=False)['Adj Close']
    return Adj_close[-1]/Adj_close[0]

