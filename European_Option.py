#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:14:46 2024

@author: michaelreginiano
"""
import numpy as np
import math
import random
import matplotlib.pyplot as plt

S_0 = 100 #starting price
mu = 0.1 #asset drift
sig = 0.3 #volatility
dt = 1/365 #time step
num_paths = 5

paths = []
for _ in range(0,num_paths):
    price = [S_0]
    for i in range(0,365):
        dW = random.gauss(0, math.sqrt(dt))
        dS = price[i]*(mu*dt+sig*dW)
        price.append(price[i]+dS)
    paths.append(price)
    
fig,ax = plt.subplots()
for p in paths:
    plt.plot(p)
plt.show()