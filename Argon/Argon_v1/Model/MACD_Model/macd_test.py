import numpy as np
import pandas as pd
import logging
from MACD_Model import macd_config

def test(data, optm_vars, cfg):
    ret, tc, rem, buy_signals, sell_signals = strategy(data.Test_data, int(optm_vars['Fast period']), int(optm_vars['Slow period']), int(optm_vars['Signal period']), signal=data.initial_signal)
    return ret, tc, rem, buy_signals, sell_signals

def strategy(data, fastperiod, slowperiod, signalperiod, signal):
    buy_signal = pd.DataFrame().rename(columns={0:'Adj Close'})
    sell_signal = pd.DataFrame().rename(columns={0:'Adj Close'})
    data = pd.DataFrame(data['Adj Close']).rename(columns={0:'Adj Close'})

    ret = 1    
    signal = signal

    stock_macd, stock_signal, hist = macd_config.calculate_macd(data['Adj Close'], fastperiod, slowperiod, signalperiod)

    trade_count = 0
    for i in range(len(data)):
        if stock_macd[i]>stock_signal[i] and signal==1:     # Buy
            buy_signal = buy_signal.append(data.iloc[i])
            ret /= data['Adj Close'][i]
            signal = 1
        elif stock_macd[i]<stock_signal[i] and signal==0:   # Sell
            sell_signal = sell_signal.append(data.iloc[i])
            ret *= data['Adj Close'][i]
            signal = 0
            trade_count += 1
            
    return ret, trade_count, signal, buy_signal, sell_signal