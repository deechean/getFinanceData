
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

from  datetime import datetime
import numpy as np

from unittrustinfo import UnitTrustInfoList
from historydata import UnitTrustData, UnitTrust

from utils.analysis_utils import RSI, weighted_rsi, MACD

def gen_layout(unittrust_info_list, unittrust, unittrust_info, indicator, price_type="Close"):
  unittrust_list = [{'label': item.name, 'value': item.ticker} for item in unittrust_info_list]
  layout = dbc.Row(
    [
      # dbc.Col(width=1, style={"background-color":"darkolivegreen"}),
      dbc.Col(
        [         
        html.Div(
          children = [
          "Select a unittrust:",
          dcc.Dropdown(
            options=unittrust_list, id="ticker-input",
            value=unittrust_list[0]['value']),
          ]
          
        ),
        html.Div(
         [gen_title(unittrust, unittrust_info, price_type),],
         id="title-block"
        ),
        html.Div(
          style={"border-width": "1px", "border-style": "solid", "border-color": "grey", "padding": "5px"},
          children=[
            html.Div(
              gen_filter(),
              id="filter-block"
            ),
            dbc.RadioItems(
              options=[
                  {"label": "Close", "value": "Close"},
                  {"label": "Adj Close", "value": "Adj Close"},
              ],
              value=price_type,
              id="price-type-input",
              inline=True,
            ),
            dcc.Graph(
              id = "price-graph",
              # figure = gen_close_price_graph(unittrust, price_type)
            ),
            html.Div(
              children=[
                "End of Chart"
              ]
            ),
            html.Div(
              children = [
              dbc.Row(
                [
                  dbc.Label("RSI Window:",width=2),
                  dbc.Col([
                  dbc.Input(
                      value=7,
                      id="rsi-window-input",
                      type="number",
                      min=1, max=31, step=1
                  )],
                  width=1
                  ),
                  dbc.Col([
                  dbc.Checkbox(
                      id="second-rsi-line",
                      label="Add second RSI line",
                      value=False,
                  )],
                  width=3
                  ),
                  dbc.Label("2nd RSI Window:",width=2),
                  dbc.Col([
                  dbc.Input(
                      value=14,
                      id="rsi-window-input-2",
                      type="number",
                      min=1, max=31, step=1, 
                      disabled=True
                  )],
                  width=1
                  )
                ]),
              html.Small("RSI window a number between 1 to 30. A typical value is 7 or 14."),
              dcc.Graph(
                id="rsi-graph",
                figure={'data': [], 'layout': {}}
              ),
              ],
              id="rsi-block"
            ),

            html.Div(
              children = [
                dbc.Row(
                [
                  
                  dbc.Label("WRSI Window:",width=2),
                  dbc.Col([
                  dbc.Input(
                      value=7,
                      id="wrsi-window-input",
                      type="number",
                      min=1, max=31, step=1
                  )],
                  width=1
                  ),
                  dbc.Label("WRSI decay factor:",width=2),
                  dbc.Col([
                  dbc.Input(
                      value=0.94,
                      id="wrsi-decay-input",
                      type="number",
                      min=0.5, max=0.99, step=0.01
                  )],
                  width=1
                  ),
                ]),
                dcc.Graph(
                  id="wrsi-graph",
                  figure={'data': [], 'layout': {}}
                ),
              ],
              id="wrsi-block"
            ),
            html.Div(
              children = [
                dbc.Row([
                  dbc.Label("Fast MA Period:",width=2),
                  dbc.Col([
                    dbc.Input(
                      value=12,
                      id="macd-fast-ma-period-input",
                      type="number",
                      min=1, max=31, step=1
                    )
                  ],
                  width=1
                  ),
                  dbc.Label("Slow MA Period:",width=2),
                  dbc.Col([
                    dbc.Input(
                      value=26,
                      id="macd-slow-ma-period-input",
                      type="number",
                      min=1, max=31, step=1
                    )
                  ],
                  width=1
                  ),
                  dbc.Label("Signal Period:",width=2),
                  dbc.Col([
                    dbc.Input(
                      value=9,
                      id="macd-signal-period-input",
                      type="number",
                      min=1, max=31, step=1
                    )
                  ],
                  width=1
                  ),
                 ]),
                dcc.Graph(id="macd-graph")
              ],            
              id="macd-block"
            ),
          ]
        ),
        html.Div(
          style={"padding": "2px"},
          children=[gen_info(unittrust)],
          id="info-block"
        )
        ],
        className="px-5"
      ),
      # dbc.Col(width=1, style={"background-color":"darkolivegreen"}),
    ]
  )
  return layout


def gen_title(unittrust, unittrust_info, price_type):
  # Input Parameters:
  # unittrust: UnitTrust Class
  # unittrust_info: 
  # price_type: string type, value could be "Close" or "Adj Close"
  # Returns: a dbc.Row object which contains the title information
  
  if unittrust_info is None:
    name = ""
    ticker = ""
    close_price = 0
    change = 0
    change_rate = 0
    update_date = "Unknown"
  else: 
    name = unittrust_info.name
    ticker = unittrust_info.ticker
    update_date = unittrust.update_date
    if price_type == "Close":
      close_price = unittrust.last_close
      change = unittrust.close_change
      change_rate = unittrust.close_change_rate
    else:
      close_price = unittrust.last_adjclose
      change = unittrust.adjclose_change
      change_rate = unittrust.adjclose_change_rate

  chart_title = dbc.Row(
    [
      html.H5(
        className="text-center font-weight-bold",
        children= name +"("+ticker+")" ,
        style={"textAlign":"center","font-weight":"bold"}
      ),
      html.P(),
      html.Div(
        style={"padding": "1px"},
        children=[
        html.H2(
            style={"font-weight": "bold", "display": "inline-block"},
            children=f"$ {close_price:.2f}"
        ),
        html.H5(
            style={"font-weight": "bold", "display": "inline-block","color": "green" if change >0 else "red"},
            children=f" {change:.2f}"
        ),
        html.H5(
            style={"font-weight": "bold", "display": "inline-block","color": "green" if change >0 else "red"},
            children=f" ({change_rate:.2f}%)"
        ),
        ]
      ),
      html.Div(
        style={"padding": "1px"},
        children=[
        html.Small(
            style={"display": "inline-block"},
            children=f"(At Close: {update_date})"
        ),
        
        ]
      ),
    ]
  )
  return chart_title

def gen_filter():
  
  filter = dbc.ButtonGroup(
    children = [
      dbc.RadioItems(
        options=[
          {"label": "1M", "value": "1M"},
          {"label": "3M", "value": "3M"},
          {"label": "6M", "value": "6M"},
          {"label": "YTD", "value": "YTD"},
          {"label": "1Y", "value": "1Y"},
          {"label": "5Y", "value": "5Y"},
          {"label": "10Y", "value": "10Y"},
          {"label": "All", "value": "All"},
        ],
        value="1M",
        id="period-input",
        inline=True
      ),
      dbc.Checklist(
        options=[
          {"label": "RSI", "value": "RSI"},
          {"label": "Weighted RSI", "value": "WRSI"},
          {"label": "MACD", "value": "MACD"},
          {"label": "Moving Average", "value": "Moving Average"},
        ],
        value=["RSI"],
        id="indicator-input",
        inline=True
      ),
    ],
    size="sm",
    className="gap-2"
  )
  
  return filter

def gen_info(unittrust):
  if unittrust is not None:
        
    row1 = html.Tr([
        html.Td("Currency: " + unittrust.unittrust_info.currency), 
        html.Td("Type: " + unittrust.unittrust_info.fund_type), 
        html.Td("Dividend Type: " + unittrust.unittrust_info.dividend_type),
    ])

    row2 = html.Tr([
        html.Td("Launch Date: " + unittrust.unittrust_info.launch_date.strftime("%Y-%m")), 
        html.Td("Total Net Asset: " + unittrust.unittrust_info.total_net_asset), 
        html.Td("Dividend Period: " + unittrust.unittrust_info.dividend_period),
    ])
      
    info_table = dbc.Table([html.Tbody([row1, row2])],bordered=1)
  else:
    info_table = dbc.Row()
  return info_table 

def gen_close_price_graph(unittrust, price_type, start=None, end=None):
  # Input Parameters:
  # unittrust: UnitTrust Class object
  # price_type：String type, value could be "Close" or "Adj Close"
  # start: date type, start date of the history price
  # end: date type, end date of the history price
  # print(f"unittrust={unittrust}, price_type={price_type}, start={start}, end={start}")

  if price_type is None:
    price_type = "Close"
  if unittrust is not None:
    df = unittrust.historydata.droplevel("Ticker", axis=1)
    # print(df.index)

    if start is None and end is None:
      df =  df[[price_type]]

    elif start is None:
      df = df.loc[:end, [price_type]]
    
    elif end is None:
      df = df.loc[start:, [price_type]]
    
    else:
      df = df.loc[start:end, [price_type]]
    
    fig = px.area(df, x=df.index, y=price_type)

    # fig.update_traces(line_width=1)
  else:
    fig = {"data": [], "layout": {}}

  # print("fig:")
  # print(fig)

  return fig
  

def gen_RSI_graph(unittrust, start=None, end=None, rsi_window=7, second_rsi=False, rsi_window_2=14):

  # print(f"unittrust={unittrust}, rsi_window={rsi_window}, second_rsi={second_rsi}, rsi_window_2={rsi_window_2}")
    
  if unittrust is not None:
    df = unittrust.historydata    

    if second_rsi:
      cols = ["RSI", "RSI-2"]
    else:
      cols = ["RSI"]
    
    df = RSI(df, rsi_window, rsi_window_2).droplevel("Ticker", axis=1)

    if start is not None:
      df = df.loc[start:]

    if end is not None:
      df = df.loc[:end]
    
    df["OverBought"] = [80 for i in range(len(df))]
    df["OverSold"] = [20 for i in range(len(df))]
    df = pd.melt(df, value_vars=cols+["OverBought", "OverSold"], ignore_index=False)
    
    fig = px.line(df, x=df.index, y="value", color="Price")
    fig.update_layout(yaxis_range=[0,100])
  else:
    fig = {"data": [], "layout": {}}

  return fig

def gen_WRSI_graph(unittrust, start=None, end=None, rsi_window=7,decay_factor=0.94):
  # print(f"unittrust={unittrust}, rsi_window={rsi_window}, decay_factor={decay_factor}")

  if unittrust is not None:
    df = unittrust.historydata 

    df = weighted_rsi(df, rsi_window, decay_factor).droplevel("Ticker", axis=1)   

    if start is not None:
      df = df.loc[start:]

    if end is not None:
      df = df.loc[:end]
    
    df["OverBought"] = [80 for i in range(len(df))]

    df["OverSold"] = [20 for i in range(len(df))]

    df = pd.melt(df, value_vars=["WRSI", "OverBought", "OverSold"], ignore_index=False)
    
    fig = px.line(df, x=df.index, y="value", color="Price")

    fig.update_layout(yaxis_range=[0,100])

  else:
    fig = {"data": [], "layout": {}}

  return fig
  
def gen_MACD_graph(unittrust, start=None, end=None, short_period=12, long_period=26, signal_period=9):
    
  if unittrust is not None:
    df = unittrust.historydata 

    df = MACD(df, short_period, long_period, signal_period).droplevel("Ticker", axis=1)  

    if start is not None:
      df = df.loc[start:]

    if end is not None:
      df = df.loc[:end]

    df_line = pd.melt(df, value_vars=["DIF", "DEA"], ignore_index=False)
    
    fig = px.line(df_line, x=df_line.index, y="value", color="Price", 
      color_discrete_map={
                  "DIF": "black",
                  "DEA": "red",
      }
    )

    fig.add_bar(x=df.index, y=df["MACD"], name="MACD")

    fig.update_layout(
      legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
      )
    )
  else:
    fig = {"data": [], "layout": {}}
  
  return fig