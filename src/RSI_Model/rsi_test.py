import numpy as np
import pandas as pd
import logging
from RSI_Model import rsi_config

def test(data, optm_vars, cfg):
    ret, tc, rem, buy_signal, sell_signal = strategy(data.Test_data, int(optm_vars['RSI Days']), int(optm_vars['Lower Bar']), int(optm_vars['Higher Bar']), signal=data.initial_signal)
    return ret, tc, rem, buy_signal, sell_signal

def strategy(data, num_days, low_bar, high_bar, signal):
    rsi_data = rsi_config.calculate_rsi(data['Adj Close'], num_days)

    buy_signal = pd.DataFrame(columns={0:'Adj Close'})
    sell_signal = pd.DataFrame(columns={0:'Adj Close'})
    data = pd.DataFrame(data['Adj Close']).rename(columns={0:'Adj Close'})

    ret = 1
    signal = signal

    trade_count = 0
    for x in range(1, len(data)):
        if (rsi_data[x] < low_bar) and signal==1:           # Buy
            buy_signal = buy_signal.append(data.iloc[x])
            ret /= data['Adj Close'][x]
            signal = 0
        elif (rsi_data[x-1]>high_bar) and signal==0:        # Sell
            sell_signal = sell_signal.append(data.iloc[x])
            ret *= data['Adj Close'][x]
            signal = 1
            trade_count += 1

    return ret, trade_count, signal, buy_signal, sell_signal