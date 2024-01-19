#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:14:46 2024

@author: michaelreginiano
"""
import numpy as np
import math
import matplotlib.pyplot as plt

S_0 = 100 #starting price
mu = 0.1 #asset drift
sig = 0.3 #volatility
dt = 1/365 #time step
num_paths = 5 #number of price paths to simulate

#Generate random increments for all paths at once
dW_matrix = np.random.normal(0,math.sqrt(dt),size=(num_paths,365))

#Compute price paths using vectorisation
price_paths = S_0 * np.exp(np.cumsum(mu*dt+sig*dW_matrix,axis=1))

# paths = []
# for _ in range(0,num_paths):
#     price = [S_0]
#     for i in range(0,365):
#         dW = random.gauss(0, math.sqrt(dt))
#         dS = price[i]*(mu*dt+sig*dW)
#         price.append(price[i]+dS)
#     paths.append(price)
    
fig,ax = plt.subplots()
for p in price_paths:
    plt.plot(p)
plt.show()