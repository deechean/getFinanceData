
import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

from  datetime import datetime
import numpy as np

from utils.unittrustinfo import UnitTrustInfoList
from utils.historydata import UnitTrustData, UnitTrust

from utils.analysis_utils import RSI, weighted_rsi, MACD

def gen_layout(unittrust_info_list, unittrust, unittrust_info):
  unittrust_list = [{'label': item.name, 'value': item.ticker} for item in unittrust_info_list]
  layout = dbc.Row(
    [
      dbc.Col(
        [         
        html.Div(
          children = [
          "Select a unittrust:",
          dbc.RadioItems(
            options=unittrust_list, id="ticker-input",
            value=unittrust_list[0]['value']),
          ]
        ),
        ],
        width=4
      ),  
      dbc.Col(
        [      
        gen_title(unittrust, unittrust_info),
        html.Div(
          style={"border-width": "1px", "border-style": "solid", "border-color": "grey", "padding": "5px"},
          children=[
            gen_price_div(),                       
            
            gen_rsi_div(),
            
            gen_wrsi_div(),
            
            gen_macd_div(),
          ]
        ),
        html.Div(
          style={"padding": "2px"},
          children=[gen_info(unittrust)],
          id="info-block"
        )
        ],
        width=8
      ),
    ],
    style={"paddingTop": "20px", "paddingBottom": "20px"}
  )
  return layout


def gen_title(unittrust, unittrust_info, price_type="Close"):
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

  chart_title = html.Div(
    dbc.Row(
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
          html.Small(
              style={"display": "inline-block"},
              children=f"(At Close: {update_date})"
          ),
        ]
      ),
    ]),
    id="title-block"
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
      dbc.RadioItems(
        options=[
            {"label": "Close", "value": "Close"},
            {"label": "Adj Close", "value": "Adj Close"},
        ],
        value="Close",
        id="price-type-input",
        inline=True,
      ),
    ],
    size="sm",
    className="gap-2"
  )
  
  return filter

def gen_price_div():
  price_div = html.Div(
    [
      gen_filter(),
      dcc.Graph(
        id = "price-graph",
        figure={'data': [], 'layout': {}},
        style={"height": "300px"}
      )
    ],
    id="price-div"
  )
  return price_div

def gen_info(unittrust_info):
  
  if unittrust_info is not None:
        
    row1 = html.Tr([
        html.Td("Currency: " + unittrust_info.currency), 
        html.Td("Type: " + unittrust_info.fund_type), 
        html.Td("Dividend Type: " + unittrust_info.dividend_type),
    ])

    row2 = html.Tr([
        html.Td("Launch Date: " + unittrust_info.launch_date.strftime("%Y-%m")), 
        html.Td("Total Net Asset: " + unittrust_info.total_net_asset), 
        html.Td("Dividend Period: " + unittrust_info.dividend_period),
    ])
      
    info_table = dbc.Table([html.Tbody([row1, row2])],bordered=1)
  else:
    info_table = dbc.Row()
  return info_table 

def gen_rsi_div():

  rsi_div = html.Div(
    children = [
      dbc.Row(
        [
          dbc.Col(
            dbc.InputGroup(
              [
                dbc.InputGroupText("RSI Window:"), 
                dbc.Input(
                  value=7,
                  id="rsi-window-input",
                  type="number",
                  min=1, max=31, step=1,
                )
              ], 
              size="sm"
            ),
            width=2
          ),
          dbc.Col([
          dbc.Checkbox(
              id="second-rsi-line",
              label="Add second RSI line",
              value=False,
          )],
          width=2
          ),
          dbc.Col(
            dbc.InputGroup(
              [
                dbc.InputGroupText("2nd RSI Window:"), 
                dbc.Input(
                  value=14,
                  id="rsi-window-input-2",
                  type="number",
                  min=1, max=31, step=1, 
                  disabled=True
                )
              ], 
              size="sm"
            ),
            width=2
          ),
        ]
      ),    
      html.Small("RSI window a number between 1 to 30. A typical value is 7 or 14."),  
      dcc.Graph(
        id="rsi-graph",
        figure={'data': [], 'layout': {}},
        style={"height": "300px"}
      ),
    ],
    id="rsi-block"
  )  
  return rsi_div

def gen_wrsi_div():
  wrsi_div = html.Div(
    children = [
      dbc.Row(
      [
        dbc.Col(
          dbc.InputGroup(
            [
              dbc.InputGroupText("WRSI Window:"), 
              dbc.Input(
                value=7,
                id="wrsi-window-input",
                type="number",
                min=1, max=31, step=1                
              )
            ],
            size="sm"
          ),
          width=2
        ),
        dbc.Col(
          dbc.InputGroup(
            [
              dbc.InputGroupText("WRSI decay factor:"),             
              dbc.Input(
                value=0.94,
                id="wrsi-decay-input",
                type="number",
                min=0.5, max=0.99, step=0.01   
              )
            ],
            size="sm"
          ),
          width=2
        ),
      ]),
      dcc.Graph(
        id="wrsi-graph",
        figure={'data': [], 'layout': {}},
        style={"height": "300px"}
      ),
    ],
    id="wrsi-block"
  )
  return wrsi_div

def gen_macd_div():
  macd_div = html.Div(
    children = [
      dbc.Row([
        dbc.Col(
          dbc.InputGroup(
            [
              dbc.InputGroupText("Fast MA Period:"), 
              dbc.Input(
                value=12,
                id="macd-fast-ma-period-input",
                type="number",
                min=1, max=31, step=1,                
              )
            ],
            size="sm"
          ),
          width=2
        ),
        dbc.Col(
          dbc.InputGroup(
            [
              dbc.InputGroupText("Slow MA Period:"),
              dbc.Input(
                value=26,
                id="macd-slow-ma-period-input",
                type="number",
                min=1, max=31, step=1
              )
            ],
            size="sm"
          ),
          width=2
        ),
        dbc.Col(
          dbc.InputGroup(
            [
              dbc.InputGroupText("Signal Period:"),
              dbc.Input(
                value=9,
                id="macd-signal-period-input",
                type="number",
                min=1, max=31, step=1,
                
              )
            ],
            size="sm"
          ),
          width=2
        ),
      ]),
      dcc.Graph(
        id="macd-graph",
        figure={'data': [], 'layout': {}},
        style={"height": "300px"}
      )
    ],            
    id="macd-block"
  )
  return macd_div

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

    fig.update_layout(
      margin=dict(l=20, r=20, t=20, b=20)
    )
    
    ymin = df[price_type].min()
    ymax = df[price_type].max()
    padding = (ymax - ymin) * 0.05
    fig.update_yaxes(range=[ymin - padding, ymax + padding])

    fig.update_xaxes(
        nticks=30
    )
  else:
    fig = {"data": [], "layout": {}}

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
    
    fig = px.line(df, x=df.index, y="value", color="Price",
      color_discrete_map={
        "RSI": "grey",
        "RSI-2": "blue",
        "OverBought": "red",
        "OverSold": "green",
      }
    )

    fig.update_layout(
      margin=dict(l=20, r=20, t=20, b=20),
      yaxis_range=[0,100],
      legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
      )
    )

    fig.update_xaxes(
        nticks=30
    )
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
    
    fig = px.line(df, x=df.index, y="value", color="Price",
      color_discrete_map={
        "WRSI": "grey",
        "OverBought": "red",
        "OverSold": "green",
      }
    )

    fig.update_layout(
      margin=dict(l=20, r=20, t=20, b=20),
      yaxis_range=[0,100],
      legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
      )
    )
    
    fig.update_xaxes(
        nticks=30
    )

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
        "DIF": "SpringGreen",
        "DEA": "red",
      }
    )

    fig.add_bar(x=df.index, y=df["MACD"], name="MACD", marker_color="CornflowerBlue")

    fig.update_layout(
      margin=dict(l=20, r=20, t=20, b=20),
      legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
      )
    )
    
    fig.update_xaxes(
        nticks=30
    )
  else:
    fig = {"data": [], "layout": {}}
  
  return fig