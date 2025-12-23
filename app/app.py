from tkinter.font import names
import pandas as pd

from flask import Flask, request, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms.validators import InputRequired

from unittrustinfo import UnitTrustInfo, UnitTrustInfoList

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisisasecret!"

global unittrust_info_list
unittrust_info_list = UnitTrustInfoList("./data/unitTrust Lookup.csv")   

@app.route("/", methods=["GET"])
def home():
    global unittrust_info_list

    unit_trust_list = []
    for unittrust in unittrust_info_list:
        unit_trust_list.append(unittrust)
    print(unittrust_info_list)
    return render_template("index.html", unittrustlist = unit_trust_list)

@app.route("/edit/<ISIN>", methods=["GET", "POST"])
def edit(ISIN):

    global unittrust_info_list
    unittrust = unittrust_info_list.get_unittrust_by_isin(ISIN)
    
    if request.method == "GET": # Open the edit form  
        return render_template("edit.html", unittrust=unittrust)
    elif request.method == "POST": # Submit the changes
        # if request.form['isin'] != ISIN: 
        #     print(f"Change the ISIN from {ISIN} to {request.form['isin']}")
        
        if request.form['name'] != unittrust.name:
            print(f"Change the name from {unittrust.name} to {request.form['name']}")
            unittrust.name = request.form['name']
        
        if request.form['fund_type'] != unittrust.fund_type:
            print(f"Change the fund_type from {unittrust.fund_type} to {request.form['fund_type']}")
            unittrust.fund_type = request.form['fund_type']

        if request.form['currency'] != unittrust.currency:
            print(f"Change the currency from {unittrust.currency} to {request.form['currency']}")
            unittrust.currency = request.form['currency']
        
        if request.form['dividend_type'] != unittrust.dividend_type:
            print(f"Change the dividend_type from {unittrust.dividend_type} to {request.form['dividend_type']}")
            unittrust.dividend_type = request.form['dividend_type']
        
        if request.form['dividend_period'] != unittrust.dividend_period:
            print(f"Change the dividend_period from {unittrust.dividend_period} to {request.form['dividend_period']}")
            unittrust.dividend_period = request.form['dividend_period']

        if request.form['ticker'] != unittrust.ticker:
            print(f"Change the ticker from {unittrust.ticker} to {request.form['ticker']}")
            unittrust.ticker = request.form['ticker']

        if request.form['launch_date'] != unittrust.launch_date:
            unittrust.launch_date = request.form['launch_date']

        if request.form['total_net_asset'] != unittrust.total_net_asset:
            unittrust.total_net_asset = request.form['total_net_asset']
        
        if request.form['desc'] != unittrust.desc:
            unittrust.desc = request.form['desc']

        if request.form['ret'] != unittrust.ret:
            unittrust.ret = request.form['ret']

        if request.form['risk'] != unittrust.risk:
            unittrust.risk = request.form['risk']

        UnitTrustInfoList.set_unittrust_by_isin(unittrust)
        return redirect(url_for("home")) 

@app.route("/view/<ISIN>", methods=["GET"])
def view(ISIN):
    global unittrust_info_list
    unittrust = unittrust_info_list.get_unittrust_by_isin(ISIN)
    if request.method == "GET": # Open the view chart  
        return f"Viewing unit trust with ISIN: {ISIN}"

if __name__ == "__main__":
    app.run(debug=True)