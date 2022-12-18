import numpy as np
import pandas as pd
import logging
from BBAND_Model import bband_config

def test(data, optm_vars, cfg):
    ret, tc, rem, buy_signal, sell_signal = strategy(data.Test_data, int(optm_vars['Time period']), int(optm_vars['nbdevup']), int(optm_vars['nbdevdn']), signal=data.initial_signal)
    return ret, tc, rem, buy_signal, sell_signal

def strategy(data, Timeperiod, nbdevup, nbdevdn, signal):
    HighBand, MiddleBand, LowBand = bband_config.calculate_bband(data['Adj Close'], Timeperiod, nbdevup, nbdevdn)

    buy_signal = pd.DataFrame().rename(columns={0:'Adj Close'})
    sell_signal = pd.DataFrame().rename(columns={0:'Adj Close'})
    data = pd.DataFrame(data['Adj Close']).rename(columns={0:'Adj Close'})

    HighBand   = HighBand[Timeperiod-1:]
    LowBand    = LowBand[Timeperiod-1:]
    MiddleBand = MiddleBand[Timeperiod-1:]
    data       = data[Timeperiod-1:]

    ret = 1
    signal = signal
    trade_count = 0

    for x in range(0, len(data)-1):
        if data['Adj Close'][x] < LowBand[x] and signal==1:     # Buy
            buy_signal = buy_signal.append(data.iloc[x])
            ret /= data['Adj Close'][x]
            signal = 0
        elif data['Adj Close'][x] > HighBand[x] and signal==0:  # Sell
            sell_signal = sell_signal.append(data.iloc[x])
            ret *= data['Adj Close'][x]
            signal = 1
            trade_count += 1

    return ret, trade_count, signal, buy_signal, sell_signal