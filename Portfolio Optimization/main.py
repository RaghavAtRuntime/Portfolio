import pandas_datareader.data as web
import datetime
import pandas as pd
import yfinance as yf
from pypfopt import EfficientCVaR, HRPOpt
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

from functools import reduce

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

start = datetime.datetime(2017, 12, 15)
end = datetime.datetime(2019, 12, 20)


def get_stock(ticker):
    """
    Takes stock ticker as parameter, returns stock close prices as a pandas dataframe.
    :param ticker: String
    :return: DataFrame
    """
    yf.pdr_override()
    data = web.get_data_yahoo(f"{ticker}", start, end)
    data[f'{ticker}'] = data["Close"]
    data = data[[f'{ticker}']]
    print(data.head())
    return data


def combine_stocks(tickers):
    """
    Takes a string of tickers and returns combined dataframe of close prices
    :param tickers: [String]
    :return: DataFrame
    """
    data_frames = []
    for i in tickers:
        data_frames.append(get_stock(i))

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Date'], how='outer'), data_frames)
    print(df_merged.head())
    return df_merged


stocks = ['ABX.TO', 'AAPL', 'HSBC', 'MSFT', 'JPM', 'LLY', 'MA', 'META', 'UNH', 'JNJ', 'SHEL', 'AZN',
          'ABT']
portfolio = combine_stocks(stocks)
portfolio.to_csv("portfolio.csv", index=False)
portfolio = pd.read_csv("portfolio.csv")
latest_prices = get_latest_prices(portfolio)


def mean_variance_opt(portfolio):
    mu = mean_historical_return(portfolio)
    s = CovarianceShrinkage(portfolio).ledoit_wolf()
    ef = EfficientFrontier(mu, s)
    weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()
    print(dict(cleaned_weights))
    ef.portfolio_performance(verbose=True)

    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=10000)

    allocation, leftover = da.greedy_portfolio()
    print("Discrete allocation:", allocation)
    print("Funds remaining: ${:.2f}".format(leftover))


def heirarchical_risk_parity(portfolio):
    returns = portfolio.pct_change().dropna()
    hrp = HRPOpt(returns)
    hrp_weights = hrp.optimize()
    hrp.portfolio_performance(verbose=True)
    print(dict(hrp_weights))
    da_hrp = DiscreteAllocation(hrp_weights, latest_prices, total_portfolio_value=10000)
    allocation, leftover = da_hrp.greedy_portfolio()
    print("Discrete allocation (HRP):", allocation)
    print("Funds remaining (HRP): ${:.2f}".format(leftover))


def mean_cond_value(portfolio):
    mu = mean_historical_return(portfolio)
    S = portfolio.cov()
    ef_cvar = EfficientCVaR(mu, S)
    cvar_weights = ef_cvar.min_cvar()
    cleaned_weights = ef_cvar.clean_weights()
    print(dict(cleaned_weights))
    da_cvar = DiscreteAllocation(cvar_weights, latest_prices, total_portfolio_value=10000)
    allocation, leftover = da_cvar.greedy_portfolio()
    print("Discrete allocation (CVAR):", allocation)
    print("Funds remaining (CVAR): ${:.2f}".format(leftover))
