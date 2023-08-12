import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimisation


class MarkoModel:

    def __init__(self,
                 stocks=["AAPL", "WMT", "TSLA", "GE", "AMZN", "DB"],
                 start_date='2012-01-01',
                 end_date='2017-01-01',
                 NUM_TRADING_DAYS=252,
                 NUM_PORTFOLIOS=10000):
        self.stocks = stocks
        self.start_date = start_date
        self.end_date = end_date
        self.NUM_TRADING_DAYS = NUM_TRADING_DAYS
        self.NUM_PORTFOLIOS = NUM_PORTFOLIOS

    def download_data(self):
        # name of stock (key) - stock values = values
        stock_data = {}

        for stock in self.stocks:
            # closing prices
            ticker = yf.Ticker(stock)
            stock_data[stock] = ticker.history(start=self.start_date, end=self.end_date)['Adj Close']
        return pd.DataFrame(stock_data)

    def show_data(self, data):
        data.plot(figsize=(10, 5))
        plt.show()

    def calculate_return(self, data):
        # normalisation - to measure comparably
        log_return = np.log(data / data.shift(1))

        return log_return[1:]

    def generate_portfolios(self, returns):
        portfolio_means = []

        portfolio_risk = []

        portfolio_weights = []

        for _ in range(self.NUM_PORTFOLIOS):
            w = np.random.random(len(self.stocks))
            w /= np.sum(w)
            portfolio_weights.append(w)

            portfolio_means.append(np.sum(returns.mean() * w) * self.NUM_TRADING_DAYS)

            portfolio_risk.append(np.sqrt(np.dot(w.T, np.dot(returns.cov() * self.NUM_TRADING_DAYS, w))))

        return np.array(portfolio_weights), np.array(portfolio_means), np.array(portfolio_risk)

    def show_portfolios(self, returns, volatilities):
        plt.figure(figsize=(10, 6))
        plt.scatter(volatilities, returns, c=returns / volatilities, marker='o')
        plt.grid = True
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Returns')
        plt.colorbar(label='Sharpe Ratio')
        plt.show()

    def statistics(self, weights, returns):
        portfolio_return = np.sum(returns.mean() * weights) * self.NUM_TRADING_DAYS
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * self.NUM_TRADING_DAYS, weights)))

        # sharpe ratio: Rf rate of risk free return assumed 0
        return np.array([portfolio_return, portfolio_volatility, portfolio_return / portfolio_volatility])

    def min_fuction_sharpe(self, weights, returns):
        return -self.statistics(weights, returns)[2]

    # function minimises f(x) = 0
    def optimise_portfolio(self, weights, returns):
        # sum of weights ==1
        constr = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}

        # weights can be at most 1 when 100% money invested
        # every weight has value between 0 and 1
        bounds = tuple((0, 1) for _ in range(len(self.stocks)))

        return optimisation.minimize(fun=self.min_fuction_sharpe, x0=weights[0], args=returns, method='SLSQP', bounds=bounds,
                                     constraints=constr)

    def print_optimal_port(self, optimum, returns):
        print("Optimal portfolio: ", optimum['x'].round(3))
        print("Exp return, vol, Sharpe ratio: ", self.statistics(optimum['x'].round(3), returns))

    def show_optimal_portfolio(self, opt, rets, portfolio_rets, portfolio_vols):
        plt.figure(figsize=(10, 6))
        plt.scatter(portfolio_vols, portfolio_rets, c=portfolio_rets / portfolio_vols, marker='o')
        plt.grid = True
        plt.xlabel('Expected Volatility')
        plt.ylabel('Expected Returns')
        plt.colorbar(label='Sharpe Ratio')
        plt.plot(self.statistics(opt['x'], rets)[1], self.statistics(opt['x'], rets)[0], 'g*', markersize=20.)
        plt.show()