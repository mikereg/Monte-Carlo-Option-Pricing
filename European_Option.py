#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monte Carlo pricing of European options.

The underlying follows geometric Brownian motion. For pricing, paths are
simulated under the risk-neutral measure (drift = risk-free rate r):

    S_T = S0 * exp((r - sigma^2 / 2) * T + sigma * sqrt(T) * Z),  Z ~ N(0, 1)

Created on Fri Jan 19 14:14:46 2024

@author: michaelreginiano
"""
import numpy as np

S0 = 100          # initial asset price
K = 110           # option strike
r = 0.03          # risk-free interest rate
sigma = 0.3       # volatility
T = 1             # time to expiry (years)
n_paths = 100_000 # number of simulated paths
seed = 42         # random seed for reproducibility


def simulate_terminal_prices(S0, r, sigma, T, n_paths, rng):
    """Sample risk-neutral terminal prices S_T exactly, in a single step."""
    Z = rng.standard_normal(n_paths)
    return S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)


def simulate_paths(S0, mu, sigma, T, n_steps, n_paths, rng):
    """Simulate full GBM paths with drift mu, returning shape (n_paths, n_steps + 1).

    Only needed for plotting: European payoffs depend on S_T alone.
    """
    dt = T / n_steps
    dW = rng.normal(0, np.sqrt(dt), size=(n_paths, n_steps))
    log_increments = (mu - 0.5 * sigma**2) * dt + sigma * dW
    log_paths = np.cumsum(log_increments, axis=1)
    log_paths = np.hstack([np.zeros((n_paths, 1)), log_paths])
    return S0 * np.exp(log_paths)


def payoff(S, K, option="call"):
    """European payoff at expiry."""
    if option == "call":
        return np.maximum(S - K, 0)
    if option == "put":
        return np.maximum(K - S, 0)
    raise ValueError(f"option must be 'call' or 'put', got {option!r}")


def mc_price(S0, K, r, sigma, T, n_paths, option="call", rng=None):
    """Monte Carlo price of a European option.

    Returns (price, std_err), where std_err is the standard error of the
    mean discounted payoff.
    """
    if rng is None:
        rng = np.random.default_rng()
    S_T = simulate_terminal_prices(S0, r, sigma, T, n_paths, rng)
    discounted = np.exp(-r * T) * payoff(S_T, K, option)
    return discounted.mean(), discounted.std(ddof=1) / np.sqrt(n_paths)


if __name__ == "__main__":
    rng = np.random.default_rng(seed)
    print(f"S0={S0}, K={K}, r={r}, sigma={sigma}, T={T}, n_paths={n_paths:,}\n")
    for option in ("call", "put"):
        mc, se = mc_price(S0, K, r, sigma, T, n_paths, option, rng)
        print(f"{option.capitalize()} estimate: {mc:.4f} (SE {se:.4f})")
