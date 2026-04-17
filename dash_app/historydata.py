import datetime, os
from datetime import datetime
import pandas as pd

# UnitTrust class 有两个核心数据
# 1. ticker：string类型，存储这个UnitTrust的ticker
# 2. df_history：pandas dataframe类型，存储这个UnitTrust的历史数据
# 这个类有以下属性
# 1. historydata：panda dataframe类型，返回指定时间段的历史数据
# 2. last_close：这个UnitTrust的最后close的时间
# 3. close_change： 这个UnitTrust的最后两个价格之间的涨跌变化
# 4. 
class UnitTrust():

  def __init__(self, ticker, df_history):
    self._ticker = ticker
    self._df_history = df_history.dropna()

    if len(self._df_history)>1:
      # Get last close price and change rate
      self._last_close = self._df_history.iloc[-1]["Close"][0] 
      self._last_2nd_close = self._df_history.iloc[-2]["Close"][0]
      self._close_change = self._last_close-self._last_2nd_close
      self._change_rate_close = self._close_change/self._last_2nd_close*100
      
      # Get last adj close price and change rate
      self._last_adjclose = self._df_history.iloc[-1]["Adj Close"][0] 
      self._last_2nd_adjclose = self._df_history.iloc[-2]["Adj Close"][0]
      self._adjclose_change = self._last_adjclose-self._last_2nd_adjclose
      self._change_rate_adjclose = self._adjclose_change/self._last_2nd_adjclose*100

      # Get last update date
      self._update_date = self._df_history.last_valid_index().strftime('%b %d %Y %H:%M:%S')
    elif len(self._df_history)==1:
      # Get last close price and change rate
      self._last_close = self._df_history.iloc[-1]["Close"][0] 
      self._last_2nd_close = 0
      self._close_change = self._last_close-self._last_2nd_close
      self._change_rate_close = self._close_change/self._last_2nd_close*100
      
      # Get last adj close price and change rate
      self._last_adjclose = self._df_history.iloc[-1]["Adj Close"][0] 
      self._last_2nd_adjclose = 0
      self._adjclose_change = self._last_adjclose-self._last_2nd_adjclose
      self._change_rate_adjclose = self._adjclose_change/self._last_2nd_adjclose*100

      # Get last update date
      self._update_date = self._df_history.last_valid_index().strftime('%b %d %Y %H:%M:%S')
    else:
      # Get last close price and change rate
      self._last_close = 0
      self._last_2nd_close = 0
      self._close_change = 0
      self._change_rate_close = 0
      
      # Get last adj close price and change rate
      self._last_adjclose = 0 
      self._last_2nd_adjclose = 0
      self._adjclose_change = 0
      self._change_rate_adjclose = 0

      # Get last update date
      self._update_date = "Unknown"
  
  @property
  def ticker(self):
    return self._ticker

  @property
  def historydata(self, start=None, end=None):
    if start is None and end is None:
      return self._df_history
    elif start is None:
      return self._df_history[start:]
    elif end is None:
      return self._df_history[:end]
    else:
      return self._df_history[start:end] 

  @property
  def last_close(self):
    """Get the last close price"""
    return self._last_close

  @property
  def close_change(self):
    """Get the change between the last 2nd close and last close price"""
    return self._close_change

  @property
  def close_change_rate(self):
    """Get the change rate between the last 2nd close and last close price"""
    return self._change_rate_close

  @property
  def last_adjclose(self):
    """Get the last adj close price"""
    return self._last_adjclose

  @property
  def adjclose_change(self):
    """Get the change between the last 2nd adj close and last adj close price"""
    return self._adjclose_change

  @property
  def adjclose_change_rate(self):
    """Get the change rate between the last 2nd adj close and last adj close price"""
    return self._change_rate_adjclose

  @property
  def update_date(self):
    """Get the last update date"""
    return self._update_date

  @property
  def first_month(self):
    return self._df_history.first_valid_index()
  
  @property
  def last_month(self):
    return self._df_history.last_valid_index() 


# 
class UnitTrustData():
  def __init__(self, file):
    self._file = file
    self._df_rawdata = pd.read_csv(file, header=[0, 1], index_col=0, parse_dates=True)
    self._ticker_list = self._df_rawdata.columns.get_level_values("Ticker").to_series().unique()
    # set init index is 0
    self._index = 0   

  def __iter__(self):
    return self

  def __next__(self):
    if self._index >= len(self._ticker_list):
      self._index = 0
      raise StopIteration  # Signal the end of iteration
    ticker = self._ticker_list[self._index]
    df_history = self._df_rawdata[[("Close", ticker),("Adj Close", ticker),("Volume", ticker),("Dividends", ticker)]]
    unittrust = UnitTrust(ticker, df_history)
    self._index += 1
    return unittrust
  
  def get_by_ticker(self, ticker: str):
    df_history = self._df_rawdata[[("Close", ticker),("Adj Close", ticker),("Volume", ticker), ("Dividends", ticker)]]
    unittrust = UnitTrust(ticker, df_history)
    self._index += 1
    return unittrust

  def get_history_price(self, ticker, start=None, end=None):
      
    if start is None:
      start = self._df_rawdata[("Close", ticker)].first_valid_index()
    if end is None:
      end = self._df_rawdata[("Close", ticker)].last_valid_index()  
    
    return self._df_rawdata[start:end]
    
if __name__ == "__main__":
  unittrust_data = UnitTrustData("./data/unit_trust_history_data-20260105.csv") 
  for data in unittrust_data:

    print(f"ticker: {data.ticker}")
    print(data.historydata)
    print(f"last_close: {data.last_close}")
    print(f"close_change: {data.close_change}")
    print(f"close_change_rate: {data.close_change_rate}%")
    print(f"last_adjclose: {data.last_adjclose}")
    print(f"adjclose_change: {data.adjclose_change}")
    print(f"adjclose_change_rate: {data.adjclose_change_rate}%")
    print(f"first_month: {data.first_month}")
    print(f"last_month: {data.last_month}")
    print(">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<")