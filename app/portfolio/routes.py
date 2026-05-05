import os
from datetime import date
from flask import request, render_template, flash, redirect, url_for, current_app, jsonify
from utils.unittrustinfo import UnitTrustInfoList
from .portfolio import Portfolio

from . import portfolio_bp
from .. import unittrust_info_list

@portfolio_bp.route("/portfolio", methods=["GET"])
def portfolio():
    # data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
    portfolios = Portfolio.get_all_portfolios()
    return render_template("portfolio_manage.html", portfolios=portfolios)

@portfolio_bp.route("/portfolio/delete/<portfolio_name>", methods=["POST"])
def delete_portfolio(portfolio_name):
    try:
        # Get data directory path
        # data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
        
        # Call Portfolio.delete_portfolio to mark as deleted
        result = Portfolio.delete_portfolio(portfolio_name)
        
        if result["success"]:
            return jsonify({"success": True, "message": result["message"]})
        else:
            return jsonify({"success": False, "message": result["message"]}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@portfolio_bp.route("/portfolio/update/<portfolio_name>", methods=["POST"])
def update_portfolio(portfolio_name):
    """Update portfolio name and currency from inline changes"""
    data = request.get_json() or {}
    new_name = data.get("portfolio_name", "").strip()
    currency = data.get("currency", "").strip()

    if not new_name:
        return jsonify({"success": False, "message": "Portfolio name is required."}), 400
    if not currency:
        return jsonify({"success": False, "message": "Currency is required."}), 400
    
    print(f"Updating portfolio '{portfolio_name}' to new name '{new_name}' and currency '{currency}'")
    
    result = Portfolio.update_portfolio(portfolio_name, new_name, currency)
    if result["success"]:
        return jsonify({"success": True, "message": result["message"], "portfolio_name": new_name, "currency": currency})
    return jsonify({"success": False, "message": result["message"]}), 400


@portfolio_bp.route("/portfolio/edit/<portfolio_name>", methods=["GET", "POST"])
def edit_portfolio(portfolio_name):
    """Edit an existing portfolio"""
    pass


@portfolio_bp.route("/portfolio/create", methods=["GET", "POST"])
def create_portfolio():
    """Create a new portfolio"""
    if request.method == "GET":
        return render_template("create_portfolio.html")
    
    elif request.method == "POST":
        portfolio_name = request.form.get("portfolio_name", "").strip()
        currency = request.form.get("currency", "").strip()
        
        if not portfolio_name:
            flash("Portfolio name is required.", "error")
            return redirect(url_for("portfolio_bp.create_portfolio"))
        
        if not currency:
            flash("Currency is required.", "error")
            return redirect(url_for("portfolio_bp.create_portfolio"))
        
        # Get data directory path (relative to the project root)
        # data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
        
        result = Portfolio.create_portfolio(portfolio_name, currency)

        print(result)
        
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("portfolio_bp.portfolio"))
        else:
            flash(result["message"], "error")
            return redirect(url_for("portfolio_bp.create_portfolio"))
