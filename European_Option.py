#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:14:46 2024

@author: michaelreginiano
"""
import numpy as np
import math

S_0 = 100 #starting price
sig = 0.3 #volatility
dt = 1/365 #time step
num_paths = 50000 #number of price paths to simulate

E = 110 #Option strike
interest_rate = 0.03 #risk-free interest rate
time_to_expiry = 1 #years

n_steps = int(round(time_to_expiry/dt)) #number of time steps to expiry

#A matrix of random increments for all price paths
dW_matrix = np.random.normal(0,math.sqrt(dt),size=(num_paths,n_steps))

#Compute risk-neutral price paths using vectorisation.
#Pricing uses the risk-free rate as drift, and the -sig^2/2 term
#is the Ito correction for the log of a GBM.
price_paths = S_0 * np.exp(np.cumsum((interest_rate-0.5*sig**2)*dt+sig*dW_matrix,axis=1))

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