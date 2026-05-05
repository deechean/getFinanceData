import os
from datetime import date
from flask import request, render_template, flash, redirect, url_for, current_app

from . import home_bp
from .. import unittrust_info_list

@home_bp.route("/", methods=["GET"])
def home():
    global unittrust_info_list

    unit_trust_list = []
    for unittrust in unittrust_info_list:
        unit_trust_list.append(unittrust)
    print(unittrust_info_list)
    return render_template("index.html", unittrustlist = unit_trust_list)
