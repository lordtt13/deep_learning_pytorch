#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 06:40:58 2020

@author: tanmay
"""

import time
import torch

import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


df = pd.read_csv('Data/TimeSeriesData/Energy_Production.csv', index_col = 0, parse_dates = True)
df.dropna(inplace = True)
print(len(df))
df.head()

# Plot data series

plt.figure(figsize = (12,4))
plt.title('Industrial Production Index for Electricity and Gas Utilities')
plt.ylabel('Index 2012 = 100, Not Seasonally Adjusted')
plt.grid(True)
plt.autoscale(axis = 'x',tight = True)
plt.plot(df['IPG2211A2N'])
plt.show()

# Preprocess

y = df['IPG2211A2N'].values.astype(float)

test_size = 12
window_size = 12

train_set = y[:-test_size]
test_set = y[-test_size:]

print(f'Train: {len(train_set)}')
print(f'Test:  {len(test_set)}')

# Normalize the dataset

scaler = MinMaxScaler(feature_range = (-1, 1))

train_norm = scaler.fit_transform(train_set.reshape(-1, 1))

print(f'First item, original: {train_set[0]}')
print(f'First item, scaled: {train_norm[0]}')

# Prepare time series data

train_norm = torch.FloatTensor(train_norm).view(-1)

def input_data(seq,ws):
    out = []
    L = len(seq)
    for i in range(L-ws):
        window = seq[i:i+ws]
        label = seq[i+ws:i+ws+1]
        out.append((window,label))
    return out

train_data = input_data(train_norm,window_size)

print(f'Train_data: {len(train_data)}')