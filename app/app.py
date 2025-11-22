from tkinter.font import names
import pandas as pd

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, SelectField
from wtforms.validators import InputRequired

from unittrustinfo import UnitTrustInfo, unittrust_info_list

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisisasecret!"
   

@app.route("/", methods=["GET"])
def home():

    return "display a table of unit trusts. "

@app.route("/edit", methods=["GET", "POST"])
def edit():
    # form=UnitTrustForm()
    # if form.validate_on_submit():
    #     return render_template("result.html", email=form.email.data, password=form.password.data, \
    #                         textarea = form.textarea.data, radios= form.radios.data, \
    #                         selects = form.selects.data)
    # return render_template("form.html", form=form)
    return "edit a unit trust"

if __name__ == "__main__":
    app.run(debug=True)