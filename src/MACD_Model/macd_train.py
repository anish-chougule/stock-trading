import numpy as np
import pandas as pd
import progressbar
import logging
import time
from pathlib import Path
import os

from MACD_Model import macd_config

def train(data, cfg):
    vars = []
    logging.info("> Optimizer Inputs:")
    for arg in cfg._init_VARIABLES:
        logging.info(arg)
        vars.append(np.arange(arg.Min, arg.Max, arg.Step))

    performance = []
    logging.info('> MACD Model is Optimizing...')
    with progressbar.ProgressBar(max_value=len(vars[0])*len(vars[1])*len(vars[2])) as bar:
        for i, period1 in enumerate(vars[0],1):
            for j, period2 in enumerate(vars[1],1):
                for k, period3 in enumerate(vars[2],1):
                    ret, tc, avgDays = strategy(data.Train_data['Adj Close'], period1, period2, period3)
                    performance.append([period1, period2, period3, ret, tc, avgDays])
                    bar.update((i-1)*len(vars[1])*len(vars[2]) + (j-1)*len(vars[2]) + k)

    logging.info('> Model Optimized Successfully!')

    performance = pd.DataFrame(np.array(performance)).rename(columns={0:'Fast period', 1:'Slow period', 2:'Signal period', 3:'Returns', 4:'Trade Count', 5:'Days per trade'})
    timestr = str(time.strftime("%Y_%m_%d-%H_%M_%S"))
    title = str(Path(os.path.dirname(__file__)).parent) + '\\stock_data\\' + data.Name + f'\\macd\\logs\\{timestr}_log.csv'
    performance.to_csv(title, index=False)

    performance = performance.sort_values(by=['Returns', 'Trade Count'])
    perf_array = [i for i,n in enumerate(performance['Returns']) if performance['Trade Count'][i]>1]
    max_perf_index = max(perf_array)
    return performance.iloc[max_perf_index,:]


def strategy(data, fastperiod, slowperiod, signalperiod):
    signal = 1

    stock_macd, stock_signal, hist = macd_config.calculate_macd(data, fastperiod, slowperiod, signalperiod)
    data = pd.DataFrame(data).rename(columns={0:'Adj Close'})

    ret = 1
    trade_count = 0
    signal = 1

    for i in range(0, len(data)):
        if stock_macd[i] > stock_signal[i] and signal!=0:
            ret /= data['Adj Close'][i]
            signal = 0
        elif stock_macd[i] < stock_signal[i] and signal!=1:
            ret *= data['Adj Close'][i]
            signal = 1
            trade_count += 1

    if signal == 0:
        ret *= data['Adj Close'][-1]

    avgDays = len(data)/trade_count if trade_count!=0 else 0

    return ret, trade_count, avgDays
