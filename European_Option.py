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

E = 110 #Option strike
interest_rate = 0.03 #risk-free interest rate
time_to_expiry = 1 #years

#A matrix of random increments for all price paths
dW_matrix = np.random.normal(0,math.sqrt(dt),size=(num_paths,365))

#Compute price paths using vectorisation
price_paths = S_0 * np.exp(np.cumsum(mu*dt+sig*dW_matrix,axis=1))

fig,ax = plt.subplots()
i = 1
for p in price_paths:
    plt.plot(p, label= f'Path {i}')
    i = i+1
    
plt.title('Geometric Brownian Motion of Asset Price Paths')
plt.xlabel('Time (days)')
plt.ylabel('Price ($)')
plt.legend()
plt.show()

def European_Call_Payoff(S,E):
    return max(S-E,0)

def European_Put_Payoff(S,E):
    return max(E-S,0)

call_pay_offs = np.array([European_Call_Payoff(p[-1], E) for p in price_paths])
discounted_call_pay_offs = call_pay_offs * np.exp(-interest_rate*time_to_expiry)
call_estimate = np.mean(discounted_call_pay_offs)

put_pay_offs = np.array([European_Put_Payoff(p[-1], E) for p in price_paths])
discounted_put_pay_offs = put_pay_offs * np.exp(-interest_rate*time_to_expiry)
put_estimate = np.mean(discounted_put_pay_offs)

print('Call Estimate: {}'.format(call_estimate))
print('Put Estimate: {}'.format(put_estimate))