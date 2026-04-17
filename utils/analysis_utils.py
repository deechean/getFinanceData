import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def RSI(df, window=7, window_2=14):
  # Get the ticker from the rawdata downloaded from yahoo
  ticker = df.columns.get_level_values(level=1).unique()[0]

  delta = df[("Close", ticker)].diff()
  
  gain = delta.where(delta > 0, 0.0)
  loss = -delta.where(delta < 0, 0.0)

  avg_gain = gain.ewm(alpha=1/window, adjust=False).mean()
  avg_loss = loss.ewm(alpha=1/window, adjust=False).mean()
  
  rs = avg_gain / avg_loss
  df[("RSI",ticker)] = 100 - (100 / (1 + rs))

  avg_gain = gain.ewm(alpha=1/window_2, adjust=False).mean()
  avg_loss = loss.ewm(alpha=1/window_2, adjust=False).mean()

  rs = avg_gain / avg_loss
  df[("RSI-2",ticker)] = 100 - (100 / (1 + rs))

  return df

def weighted_rsi(df, window=7, decay_factor=0.94):
  # Get the ticker from the rawdata downloaded from yahoo
  ticker = df.columns.get_level_values(level=1).unique()[0]

  weights = np.array([decay_factor ** i for i in range(window-1,-1,-1)])
  weights = weights / weights.sum()

  delta = df[("Close", ticker)].diff()

  gain = delta.where(delta > 0, 0.0)
  loss = -delta.where(delta < 0, 0.0)

  avg_gain = gain.rolling(window=window).apply(
    lambda x: np.sum(x*weights), raw=True
  )
  avg_loss = loss.rolling(window=window).apply(
    lambda x: np.sum(x*weights), raw=True
  )

  rs = avg_gain / avg_loss
  df[("WRSI",ticker)] = 100 - (100 / (1 + rs))

  # avg_gain = gain.rolling(window=window).apply(
  #   lambda x: np.sum(x*weights), raw=True
  # )
  # avg_loss = loss.rolling(window=window).apply(
  #   lambda x: np.sum(x*weights), raw=True
  # )

  # rs = avg_gain / avg_loss
  # df[("WRSI-2",ticker)] = 100 - (100 / (1 + rs))

  return df

def MACD(df, short_period=12, long_period=26, signal_period=9):
  """
    计算 MACD 指标

    参数：
    data: pandas DataFrame，必须包含价格列（默认 ('close', ticker)）
    short_period: 短期 EMA 周期（默认 12）
    long_period: 长期 EMA 周期（默认 26）
    signal_period: 信号线周期（默认 9）
   
    返回：
    DataFrame，包含：
    - DIF (MACD line)
    - DEA (Signal line)
    - MACD (Histogram)
    """
  ticker = df.columns.get_level_values(level=1).unique()[0]

  # 计算 EMA
  df[("EMA_short", ticker)] = df[("Close", ticker)].ewm(span=short_period, adjust=False).mean()
  df[("EMA_long", ticker)] = df[("Close", ticker)].ewm(span=long_period, adjust=False).mean()

  # DIF = 短期EMA - 长期EMA
  df[("DIF", ticker)] = df[("EMA_short", ticker)] - df[("EMA_long", ticker)]

  # DEA = DIF 的 EMA
  df[("DEA", ticker)] = df[("DIF", ticker)].ewm(span=signal_period, adjust=False).mean()

  # MACD Histogram
  df[("MACD", ticker)] = df[("DIF", ticker)] - df[("DEA", ticker)]

  return df
