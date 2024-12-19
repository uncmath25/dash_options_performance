import plotly.graph_objects as go


OPTION_SHARE_MULTIPLIER = 100

PRICE_MESH_RATIO = 10


def compute_break_even_profit_price(start_stock_price, option_price, strike_price, option_number):
    initial_investment = option_number * OPTION_SHARE_MULTIPLIER * option_price
    stock_shares = initial_investment / start_stock_price
    break_even_profit_price = (option_number * OPTION_SHARE_MULTIPLIER * (strike_price + option_price) - stock_shares * start_stock_price) / (option_number * OPTION_SHARE_MULTIPLIER - stock_shares)
    return f'${round(break_even_profit_price, 2)}'


def compute_multiplier(start_stock_price, option_price, strike_price, option_number, stock_price_multiplier):
    initial_investment = option_number * OPTION_SHARE_MULTIPLIER * option_price
    stock_shares = initial_investment / start_stock_price
    stock_prices = [start_stock_price * i / PRICE_MESH_RATIO
                    for i in range(PRICE_MESH_RATIO * stock_price_multiplier + 1)]
    stock_profits = [stock_shares * (p - start_stock_price) for p in stock_prices]
    option_profits = [option_number * OPTION_SHARE_MULTIPLIER * (p - strike_price - option_price)
                      for p in stock_prices]
    option_profits = [max(p, -initial_investment) for p in option_profits]
    multiplier = option_profits[-1] / stock_profits[-1]
    return f'{round(multiplier, 2)} @ {stock_price_multiplier}x stock price'


def build_fig(option_name, start_stock_price, option_price, strike_price, option_number, stock_price_multiplier):
    initial_investment = option_number * OPTION_SHARE_MULTIPLIER * option_price
    stock_shares = initial_investment / start_stock_price
    stock_prices = [start_stock_price * i / PRICE_MESH_RATIO
                    for i in range(PRICE_MESH_RATIO * stock_price_multiplier + 1)]
    stock_profits = [stock_shares * (p - start_stock_price) for p in stock_prices]
    option_profits = [option_number * OPTION_SHARE_MULTIPLIER * (p - strike_price - option_price)
                      for p in stock_prices]
    option_profits = [max(p, -initial_investment) for p in option_profits]
    x_min = stock_prices[0]
    x_max = stock_prices[-1]
    y_min = -initial_investment
    y_max = max(stock_profits + option_profits)
    data = [
        go.Scatter(
            x=stock_prices,
            y=stock_profits,
            name='Stock',
            mode='markers+lines',
            hovertemplate='<b>%{x:$,.0f}: %{y:$,}</b><extra></extra>',
            marker=dict(color='green')
        ),
        go.Scatter(
            x=stock_prices,
            y=option_profits,
            name='Option',
            mode='markers+lines',
            hovertemplate='<b>%{x:$,.0f}: %{y:$,}</b><extra></extra>',
            marker=dict(color='blue')
        )
    ]
    layout = go.Layout(
        title=f'{option_name} Baseline Profit Comparison',
        xaxis=dict(title='Stock Price ($)', range=[x_min, x_max]),
        yaxis=dict(title='Profit ($)', range=[y_min, y_max]),
        template='plotly_dark'
    )
    return go.Figure(data=data, layout=layout)
