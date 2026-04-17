
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

from dash_app.dash_layout import gen_layout, gen_title, gen_close_price_graph, gen_RSI_graph


from  datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px

unittrust_info_list = UnitTrustInfoList("./data/unitTrust Lookup.csv")   
unittrust_data = UnitTrustData("./data/unit_trust_history_data-20260226.csv") 

# print(f"unittrust_data length: {len(unittrust_data)}")

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Charts of Unit Trusts"
unittrust_list = [{'label': item.name, 'value': item.ticker} for item in unittrust_info_list]

# Generate test data
start_date = '2026-04-01'
end_date = datetime.now().strftime('%Y-%m-%d')
date_index = pd.date_range(start=start_date, end=end_date)
n = len(date_index)
# 第一组：WRSI，随机 0-1
df_wrsi = pd.DataFrame({'value': np.random.rand(n), 'Price': 'WRSI'}, index=date_index)

# 第二组：OverBought，固定值 0.8
df_ob = pd.DataFrame({'value': 0.8, 'Price': 'OverBought'}, index=date_index)

# 第三组：OverSold，固定值 0.2
df_os = pd.DataFrame({'value': 0.2, 'Price': 'OverSold'}, index=date_index)

# 3. 合并数据
df = pd.concat([df_wrsi, df_ob, df_os])

print(df)

app.layout = html.Div(
  [
    # html.Div(
    #   id="unit-trust-container",
    #   children = [
    #       dcc.Dropdown(options=unittrust_list),
    #     ]
    # ),

    # # dcc.Location(id="url", refresh=True),
    # dcc.Store(id="ticker-value"),
    # dcc.Store(id="start-date"),
    # dcc.Store(id="end-date"),
    dcc.Graph(id="w-rsi-graph", figure=px.line(df, x=df.index, y="value", color="Price")),
  ]
)

if __name__ == '__main__':
    app.run(debug=True)