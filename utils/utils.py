import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from IPython.display import display

def cal_annual_return(df, year):
    ticker = df.columns.get_level_values(level=1).unique()[0]  
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    df = df.loc[start_date:end_date]
    
    if df.empty:
        return None, None, None, None
    else:
        idx = df[("Close", ticker)].first_valid_index()
        if idx is not None:
            year_begin = df[("Close",ticker)][idx]
        else:
            year_begin = None

        idx = df[("Close", ticker)].last_valid_index()
        if idx is not None: 
            year_end = df[("Close",ticker)][idx]
        else:
            year_end = None

        acc_div = df[("Dividends",ticker)].sum()
        
        annual_vol = cal_annual_volatility(df, ticker)
        
        no_risk_return_rate = float(
            pd.read_csv("./data/1_year_us_treasury_yield.csv",index_col=0).loc[year][0].strip('%')
        )/100

        # print(f"year_begin:{year_begin}, year_end:{year_end}, acc_div: {acc_div} ")

        if year_begin is not None:

            return_rate = (year_end - year_begin + acc_div) / year_begin

            shape_ratio = (return_rate- no_risk_return_rate)/annual_vol

        else:
            return_rate = None

            shape_ratio = None
            
        return year_begin, year_end, acc_div, return_rate, shape_ratio

def cal_max_drawdown(df, year = None):
    ticker = df.columns.get_level_values(level=1).unique()[0]   
    if year is not None:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        df = df.loc[start_date:end_date]
    df[("cummax",ticker)] = df[("Adj Close",ticker)].cummax() 
    df[("drawdown",ticker)] = df[("Adj Close",ticker)]/df[("cummax",ticker)]-1
    return df[("drawdown",ticker)].min()

def cal_annual_volatility(df, ticker):
    df[("return",ticker)] = df[("Adj Close",ticker)].pct_change()

    daily_vol = df[("return",ticker)].std()

    annual_vol = daily_vol * np.sqrt(252)

    return annual_vol

def cal_dividend_rate(df, year=None):
    ticker = df.columns.get_level_values(level=1).unique()[0]   
    if year is not None:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        df = df.loc[start_date:end_date]
    
    total_dividend = df[("Dividends",ticker)].sum()

    idx = df[("Close", ticker)].first_valid_index()
    if idx is not None:
        dividend_rate = total_dividend/df[("Close",ticker)][idx]
    else:
        dividend_rate = None         

    return dividend_rate

def get_ticker_from_name(df_lookup, trust_name):
    ticker = df_lookup[df_lookup["Name"]==trust_name]["Ticker"].values[0]
    return ticker

def gen_price_chart(df_history, df_lookup, ISIN, period):
    # period in "30d", "90d", "180d", "1y", "5y", "max"
    trust_name = df_lookup[df_lookup["ISIN"]==ISIN]["Name"].values[0]
    ticker = df_lookup[df_lookup["ISIN"]==ISIN]["Ticker"].values[0]

    if period == "30d":
        days = 30
    elif period == "90d":
        days = 90
    elif period == "180d":
        days = 180
    elif period == "1y":
        days = 365
    elif period == "5y":
        days = 365*5
    elif period == "max":
        days = (df_history.index[-1] - df_history.index[0]).days

    start = (datetime.today()- timedelta(days=days)).strftime("%Y-%m-%d")
    end = datetime.today().strftime("%Y-%m-%d")

    df = df_history.loc[start:end, [("Close", ticker), ("Volume", ticker)]]
    df.columns = df.columns.get_level_values(0)

    fig, ax1 = plt.subplots(figsize=(6, 3))

    # 绘制价格
    ax1.plot(df.index, df['Close'], color='blue', label='Price')
    ax1.set_ylabel('Price', color='blue')

    # 添加成交量副轴
    ax2 = ax1.twinx()
    ax2.bar(df.index, df['Volume'], color='gray', alpha=0.3, label='Volume')
    ax2.set_ylabel('Volume', color='gray')

    plt.title(f"{trust_name} - Price")
    plt.show()

def display_annual_metrics(df, ISIN):
    cols = ["Year", "begin_price", "end_price", "Acc Divident", "Return Rate", "Dividend Rate", "Max Drawdown", "Shape Ratio"]
    print(df[df["ISIN"] == ISIN]["Name"].unique()[0])
    display(df.loc[df["ISIN"] == ISIN][cols])

def get_latest_price(df, year):
    ticker = df.columns.get_level_values(level=1).unique()[0]   
    if year is not None:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        df = df.loc[start_date:end_date]
    if df.empty:
        return None
    else:
        idx = df[("Close", ticker)].last_valid_index()
        return df[("Close",ticker)][idx]

def get_initial_price(df, year):
    ticker = df.columns.get_level_values(level=1).unique()[0]   
    if year is not None:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        df = df.loc[start_date:end_date]
    if df.empty:
        return None
    else:
        idx = df[("Close", ticker)].first_valid_index()
        return df[("Close",ticker)][idx]
    
def cal_portfolio_dividend(portfolio, df_unittrust_lookup, df_history, df_metrics):
    total_dividend = 0
    for trust in portfolio:
        ticker = df_unittrust_lookup.loc[df_unittrust_lookup["ISIN"]==trust["ISIN"]]["Ticker"].values[0]
        idx = pd.IndexSlice
        trust_value = get_latest_price(df_history.loc[:, idx[:, ticker]],2025) * trust["unit"]
        dividend_rate = df_metrics[(df_metrics["Year"]==2024)&(df_metrics["ISIN"]==trust["ISIN"])]["Dividend Rate"].values[0]
        total_dividend += trust_value*dividend_rate
    return total_dividend
# Example usage:
# df_close_adj = cal_adjusted_close(df_history[("Close", "0P0000Z1XG.SI")], df_div_hist[df_div_hist["ISIN"] == "SG9999010490"])
# max_drawdown = cal_max_drawdown(df_close_adj, year= 2023)
# print("Max Drawdown in 2023:", max_drawdown)