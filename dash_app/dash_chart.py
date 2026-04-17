
import sys
sys.path.append("c:\\MyCode\\getFinanceData\\")
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from dash import Dash, State, html, dcc, callback, Output, Input, ctx
import dash_bootstrap_components as dbc
import urllib.parse

from unittrustinfo import UnitTrustInfoList
from historydata import UnitTrustData, UnitTrust

from dash_layout import gen_layout, gen_title, gen_close_price_graph, gen_RSI_graph, gen_WRSI_graph, gen_MACD_graph

unittrust_info_file = "./data/unitTrust Lookup.csv"
history_data_file = "./data/unit_trust_history_data-20260417.csv"
unittrust_info_list = UnitTrustInfoList("./data/unitTrust Lookup.csv")
unittrust_data = UnitTrustData(history_data_file)  


# print(f"unittrust_data length: {len(unittrust_data)}")

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Charts of Unit Trusts"

app.layout = html.Div(
  [
    html.Div(
      id="unit-trust-container",
      children = gen_layout(unittrust_info_list, None, None, None)
    ),

    # dcc.Location(id="url", refresh=True),
    dcc.Store(id="ticker-value"),
    dcc.Store(id="start-date", data=(date.today().replace(day=1)-timedelta(days=1)).replace(day=1)),
    dcc.Store(id="end-date"),
  ]
)

# --- start of update data ---

# def update_price(ticker, start_date=None, end_date=None):
  
#   df_history = unittrust_data.get_history_price(ticker)

#   df_history = df_history.dropna()

#   return df_history[start_date:end_date]

def get_unittrust_info(ticker): 
  
  unittrust_info = unittrust_info_list.get_unittrust_by_ticker(ticker)

  return unittrust_info

# def update_indicator(df_history, indicator="RSI", start_date=None, end_date=None, rsi_window=7, rsi_window_2=14):  
  
#   if indicator == "RSI":
#     df_history = RSI(df_history, rsi_window, rsi_window_2)
#   elif indicator == "MACD":
#     df_history = MACD(df_history)

#   df_history = df_history.dropna()
#   print(df_history)
#   return df_history #[start_date:end_date]

# def get_latest_price(df_history, price_type):

#   if df_history is not None:
#     last_price = df_history.iloc[-1][price_type][0]
#     last_second_price = df_history.iloc[-2][price_type][0]
#     change = last_price-last_second_price
#     ratio = change/last_second_price*100
#     update_date = df_history.last_valid_index().strftime('%b %d %Y %H:%M:%S')
    
#   else:
#     last_price = 0
#     change = 0
#     ratio = 0
#     update_date = "Unknown"
  
#   return last_price, change, ratio, update_date

# --- end of update data ---
@app.callback(
  Output("ticker-value", "data"),
  Input("ticker-input","value")
)
def get_ticker(ticker):
  print(f">>>>ticker: {ticker}<<<<<")
  return ticker

# @app.callback(
#   Output("ticker-value", "data"),
#   Input("url", "search")
# )
# def get_ticker(params):
#   print(f">>>>params: {params}<<<<<")
#   parsed = urllib.parse.urlparse(params)
#   parsed_dict = urllib.parse.parse_qs(parsed.query)
#   return parsed_dict["ticker"][0]

# Update title block
@app.callback(
  Output("title-block", "children"),
  Input("ticker-value", "data"),
  Input("price-type-input","value"),
)
def update_title(ticker, price_type):
  # print(f">>>>update_title: {ticker}<<<<<")
  unittrust = unittrust_data.get_by_ticker(ticker)
  unittrust_info = get_unittrust_info(ticker)

  title_layout = gen_title(unittrust, unittrust_info, price_type)
  return title_layout

# Update date range
@app.callback(
  Output("start-date", "data"),
  Output("end-date", "data"),
  Input("period-input","value"),
  State("ticker-value", "data"),
  prevent_initial_call=True,
)
# def update_date_range(one_mth, three_mth, six_mth, ytd, one_year, five_year, ten_year, all, ticker):
def update_date_range(period, ticker):
  
  unittrust = unittrust_data.get_by_ticker(ticker)
  start_date = None
  end_date = unittrust.last_month

  if period == "1M":
    start_date = (unittrust.last_month - relativedelta(months=1)).replace(day=1)
  elif period == "3M":
    start_date = (unittrust.last_month - relativedelta(months=3)).replace(day=1)
  elif period == "6M":
    start_date = (unittrust.last_month - relativedelta(months=6)).replace(day=1)
  elif period == "YTD":
    start_date = unittrust.last_month.replace(month=1).replace(day=1)
  elif period == "1Y":
    start_date = (unittrust.last_month - relativedelta(years=1)).replace(day=1)
  elif period == "5Y":
    start_date = (unittrust.last_month - relativedelta(years=5)).replace(day=1)
  elif period == "10Y":
     start_date = (unittrust.last_month - relativedelta(years=10)).replace(day=1)
  else:
    start_date = unittrust.first_month

  return start_date, end_date

# Update price chart
@app.callback(
  Output("price-graph", "figure"),
  Input("price-type-input","value"),
  Input("start-date","data"),
  Input("end-date","data"),
  Input("ticker-value","data"),
  prevent_initial_call=True,
)
def update_price_charts(price_type, start_date, end_date, ticker):
  global unittrust_data
  unittrust = unittrust_data.get_by_ticker(ticker)
 
  if start_date is not None:
    start_date = start_date[:10]
  
  if end_date is not None:
    end_date = end_date[:10]
 
  if unittrust is None:
    return {"data": [], "layout": {}}

  return gen_close_price_graph(unittrust, price_type, start_date, end_date)

# Change the visibility of rsi/macd chart
@app.callback(
  Output("rsi-block", "style"),
  Output("wrsi-block", "style"),
  Output("macd-block", "style"),
  Input("indicator-input", "value"),
)
def update_indicator_block_visibility(indicator):
  print(indicator)
  if "RSI" in indicator:
    rsi_style = {"display":"block"}
  else:
    rsi_style = {"display":"none"}
   
  if  "WRSI" in indicator:
    wrsi_style = {"display":"block"} 
  else:
    wrsi_style = {"display":"none"} 
    
  if "MACD" in indicator:  
    macd_style = {"display":"block"} 
  else:
    macd_style = {"display":"none"} 
    
  return rsi_style, wrsi_style, macd_style

@app.callback(
  Output("rsi-graph", "figure"),
  Output("rsi-window-input-2","disabled"),
  Input("rsi-block", "style"),
  Input("rsi-window-input", "value"),
  Input("rsi-window-input-2", "value"),
  Input("second-rsi-line", "value"),
  Input("start-date","data"),
  Input("end-date","data"),
  Input("ticker-value", "data"),
  prevent_initial_call=True,
)
def update_rsi_chart(block_style, rsi_window, rsi_window_2, second_rsi, start_date, end_date, ticker):
  # print(f"block_style={block_style}, rsi_window={rsi_window}, rsi_window_2={rsi_window_2}, second_rsi={second_rsi}, start_date={start_date},end_date={end_date}, ticker={ticker}")
  if block_style == {'display': 'block'} and ticker is not None:
    global unittrust_data 
    unittrust = unittrust_data.get_by_ticker(ticker)

    if start_date is not None:
      start_date = start_date[:10]
    
    if end_date is not None:
      end_date = end_date[:10]
   
    return gen_RSI_graph(unittrust, start_date, end_date, rsi_window, second_rsi, rsi_window_2), not second_rsi
  else:
    return {"data": [], "layout": {}}, not second_rsi
  
@app.callback(
  Output("wrsi-graph", "figure"),
  Input("wrsi-block", "style"),
  Input("wrsi-window-input", "value"),
  Input("wrsi-decay-input", "value"),
  Input("start-date","data"),
  Input("end-date","data"),
  Input("ticker-value", "data"),
  prevent_initial_call=True,
)
def update_wrsi_chart(block_style, rsi_window, decay_factor, start_date, end_date, ticker):
  # print(f"block_style={block_style}, rsi_window={rsi_window}, decay_factor={decay_factor}, start_date={start_date},end_date={end_date}, ticker={ticker}")
  if block_style == {'display': 'block'} and ticker is not None:
    global unittrust_data
    unittrust = unittrust_data.get_by_ticker(ticker)

    if start_date is not None:
      start_date = start_date[:10]
    
    if end_date is not None:
      end_date = end_date[:10]

    return gen_WRSI_graph(unittrust, start_date, end_date, rsi_window, decay_factor)  
  else:
    return {"data": [], "layout": {}}
  
@app.callback(
  Output("macd-graph", "figure"),
  Input("macd-block", "style"),
  Input("macd-fast-ma-period-input", "value"),
  Input("macd-slow-ma-period-input", "value"),
  Input("macd-signal-period-input", "value"),  
  Input("start-date","data"),
  Input("end-date","data"),
  Input("ticker-value", "data"),
  prevent_initial_call=True,
)
def update_macd_chart(block_style, fast_period, slow_period, signal_period, start_date, end_date, ticker):
  
  if block_style == {'display': 'block'} and ticker is not None:
    global unittrust_data
    unittrust = unittrust_data.get_by_ticker(ticker)

    if start_date is not None:
      start_date = start_date[:10]
    
    if end_date is not None:
      end_date = end_date[:10]

    return gen_MACD_graph(unittrust, start_date, end_date, fast_period, slow_period, signal_period)
  else:
    return {"data": [], "layout": {}}
  
if __name__ == '__main__':
    app.run(debug=True)