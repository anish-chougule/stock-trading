import numpy as np
import pandas as pd
import progressbar
import logging
import time
from pathlib import Path
import os

from RSI_Model import rsi_config

def train(data, cfg):
    vars = []
    logging.info("> Optimizer Inputs:")
    for arg in cfg._init_VARIABLES:
        logging.info(arg)
        vars.append(np.arange(arg.Min, arg.Max, arg.Step))

    performance = []
    logging.info('> RSI Model is Optimizing...')
    with progressbar.ProgressBar(max_value=len(vars[0])*len(vars[1])*len(vars[2])) as bar:
        for i, num_days in enumerate(vars[0],1):
            for j, low_bar in enumerate(vars[1],1):
                for k, high_bar in enumerate(vars[2],1):
                    ret, tc, avgDays = strategy(data.Train_data['Adj Close'], num_days, low_bar, high_bar)
                    performance.append([num_days, low_bar, high_bar, ret, tc, avgDays])
                    bar.update((i-1)*len(vars[1])*len(vars[2]) + (j-1)*len(vars[2]) + k)

    logging.info('> Model Optimized Successfully!')

    performance = pd.DataFrame(np.array(performance)).rename(columns={0:'RSI Days', 1:'Lower Bar', 2:'Higher Bar', 3:'Returns', 4:'Trade Count', 5:'Days per trade'})
    timestr = str(time.strftime("%Y_%m_%d-%H_%M_%S"))
    title = str(Path(os.path.dirname(__file__)).parent) + '\\stock_data\\' + data.Name + f'\\rsi\\logs\\{timestr}_log.csv'
    performance.to_csv(title)

    performance = performance.sort_values(by=['Returns', 'Trade Count'])
    perf_array = [i for i,n in enumerate(performance['Returns']) if performance['Trade Count'][i]>1]
    max_perf_index = max(perf_array)
    return performance.iloc[max_perf_index,:]


def strategy(data, num_days, low_bar, high_bar):
    rsi_data = rsi_config.calculate_rsi(data, num_days)
    
    data = pd.DataFrame(data).rename(columns={0:'Adj Close'})

    trade_count = 0
    ret = 1
    signal = 1
    
    for x in range(0, len(data)):
        if (rsi_data[x] < low_bar) and signal!=0:
            ret /= data['Adj Close'][x]
            signal = 0
        elif (rsi_data[x]>high_bar) and signal!=1:
            ret *= data['Adj Close'][x]
            signal = 1
            trade_count += 1

    if signal == 0:
        ret *= data['Adj Close'][-1]

    avgDays = len(data)/trade_count if trade_count!=0 else 0

    return ret, trade_count, avgDays