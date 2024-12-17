'''
Example:
Call IBIT 1/16/26 75 @ $15 - IBIT 56.76
$1500 buys 1 call option or 26.43 shares
IBIT 56.76 - break even for base stock investment
IBIT 90 - break even for call option - buy 100 shares costing $90 @ $75, making $1500
    26.43*(90-56.76) - $879 or 59% profit for stock investment

IBIT ~ (bitcoin_price / 101) * 57.6
179 - 102

stock_shares * (p - start_stock_price) = option_number * OPTION_SHARE_MULTIPLIER * (p - strike_price - option_price)
p = [option_number * OPTION_SHARE_MULTIPLIER * (strike_price + option_price) - stock_shares * start_stock_price] / (option_number * OPTION_SHARE_MULTIPLIER - stock_shares)

multiplier = OPTION_SHARE_MULTIPLIER * option_price / (option_number * OPTION_SHARE_MULTIPLIER * option_price / start_stock_price) = start_stock_price / option_price
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

POTENTIAL_STOCK_PRICE_MULTIPLIER = 5
OPTION_SHARE_MULTIPLIER = 100

PRICE_MESH_RATIO = 100

def build_options_performance_plot(options_name, start_stock_price, option_price, strike_price, option_number=1):
    initial_investment = option_number * OPTION_SHARE_MULTIPLIER * option_price
    stock_shares = initial_investment / start_stock_price
    plt.rcParams["figure.figsize"] = (16, 9)
    stock_prices = [start_stock_price * i / PRICE_MESH_RATIO
        for i in range(PRICE_MESH_RATIO * POTENTIAL_STOCK_PRICE_MULTIPLIER + 1)]
    stock_profits = [stock_shares * (p - start_stock_price) for p in stock_prices]
    option_profits = [option_number * OPTION_SHARE_MULTIPLIER * (p - strike_price - option_price)
        for p in stock_prices]
    option_profits = [max(p, -initial_investment) for p in option_profits]
    break_even_profit_price = compute_break_even_profit_price(
        start_stock_price, option_price, strike_price, option_number, stock_shares)
    print(f'{options_name} Performance Profile')
    print(f'Break Even Profit Price: {round(break_even_profit_price, 2)}')
    print(f'Break Even Bitcoin Price: {1000 * (estimate_btc_from_stock_price(break_even_profit_price) // 1000)}')
    print(f'Expected Stock Price Multiplier: {POTENTIAL_STOCK_PRICE_MULTIPLIER}')
    print(f'Asymptotic Multiplier: {round(start_stock_price / option_price, 2)}')
    print(f'Realized Multiplier: {round(option_profits[-1] / stock_profits[-1], 2)}')
    print('')
    y_min = -initial_investment
    y_max = max(stock_profits + option_profits)
    plt.plot(stock_prices, stock_profits, color='green')
    plt.plot(stock_prices, option_profits, color='blue')
    plt.plot([start_stock_price, start_stock_price], [y_min, y_max], color='yellow')
    plt.plot([break_even_profit_price, break_even_profit_price], [y_min, y_max], color='red')
    plt.plot([0, stock_prices[-1]], [0, 0], color='black')
    axes = plt.gca()
    axes.set_xlim([stock_prices[0], stock_prices[-1]])
    axes.set_ylim([y_min, y_max])
    plt.title(f'{options_name} Performance Profile')
    plt.xlabel('Stock Price ($)')
    plt.ylabel('Profit ($)')
    plt.savefig(f'{options_name}.png')
    plt.clf()

def compute_break_even_profit_price(start_stock_price, option_price, strike_price, option_number, stock_shares):
    return (option_number * OPTION_SHARE_MULTIPLIER * (strike_price + option_price) - stock_shares * start_stock_price) / (option_number * OPTION_SHARE_MULTIPLIER - stock_shares)

def estimate_btc_from_stock_price(stock_price):
    return (stock_price / 57.6) * 101000

build_options_performance_plot('IBIT_CALL_Jan_16_26_75', 56.76, 15.01, 75, 20)
build_options_performance_plot('IBIT_CALL_Jan_16_26_100', 56.76, 10.93, 100, 15)
