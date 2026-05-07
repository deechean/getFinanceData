import os, csv
from datetime import date
from flask import request, render_template, flash, redirect, url_for, current_app, jsonify
from utils.unittrustinfo import UnitTrustInfoList
from .portfolio import Portfolio

from . import portfolio_bp
from .. import unittrust_info_list

@portfolio_bp.route("/portfolio", methods=["GET"])
def portfolio():
    data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
    portfolios = Portfolio.get_all_portfolios(data_dir)
    return render_template("portfolio_manage.html", portfolios=portfolios)

@portfolio_bp.route("/portfolio/delete/<portfolio_name>", methods=["POST"])
def delete_portfolio(portfolio_name):
    try:
        data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
        
        # Call Portfolio.delete_portfolio to mark as deleted
        result = Portfolio.delete_portfolio(portfolio_name, data_dir)
        
        if result["success"]:
            return jsonify({"success": True, "message": result["message"]})
        else:
            return jsonify({"success": False, "message": result["message"]}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@portfolio_bp.route("/portfolio/update/<portfolio_name>", methods=["POST"])
def update_portfolio(portfolio_name):
    """Update portfolio name and currency from inline changes"""
    data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
    
    data = request.get_json() or {}
    new_name = data.get("portfolio_name", "").strip()
    currency = data.get("currency", "").strip()

    if not new_name:
        return jsonify({"success": False, "message": "Portfolio name is required."}), 400
    if not currency:
        return jsonify({"success": False, "message": "Currency is required."}), 400
    
    print(f"Updating portfolio '{portfolio_name}' to new name '{new_name}' and currency '{currency}'")
    
    result = Portfolio.update_portfolio(portfolio_name, new_name, currency, data_dir)
    if result["success"]:
        return jsonify({"success": True, "message": result["message"], "portfolio_name": new_name, "currency": currency})
    return jsonify({"success": False, "message": result["message"]}), 400


@portfolio_bp.route("/portfolio/edit/<portfolio_name>", methods=["GET", "POST"])
def edit_portfolio(portfolio_name):
    """Edit an existing portfolio"""
    data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
    
    if request.method == "GET":
        portfolio = Portfolio.get_portfolio_by_name(portfolio_name, data_dir)
        if not portfolio:
            flash("Portfolio not found.", "error")
            return redirect(url_for("portfolio_bp.portfolio"))
        
        details = Portfolio.get_portfolio_details(portfolio_name, data_dir)
        
        # Get symbols for dropdown
        symbols = []
        lookup_path = os.path.join(data_dir, "UnitTrust Lookup.csv")
        
        try:
            with open(lookup_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row.get('Name', '')
                    ticker = row.get('Ticker', '')
                    if name and ticker:
                        symbols.append(f"{name} ({ticker})")

        except Exception as e:
            print(f"Error reading UnitTrust Lookup: {str(e)}")
        
        return render_template("edit_portfolio.html", portfolio=portfolio, details=details, symbols=symbols)
    
    elif request.method == "POST":
        new_name = request.form.get("portfolio_name", "").strip()
        currency = request.form.get("currency", "").strip()
        
        if not new_name:
            flash("Portfolio name is required.", "error")
            return redirect(url_for("portfolio_bp.edit_portfolio", portfolio_name=portfolio_name))
        
        if not currency:
            flash("Currency is required.", "error")
            return redirect(url_for("portfolio_bp.edit_portfolio", portfolio_name=portfolio_name))
        
        result = Portfolio.update_portfolio(portfolio_name, new_name, currency, data_dir)
        
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("portfolio_bp.edit_portfolio", portfolio_name=new_name))
        else:
            flash(result["message"], "error")
            return redirect(url_for("portfolio_bp.edit_portfolio", portfolio_name=portfolio_name))

@portfolio_bp.route("/portfolio/add_symbol/<portfolio_name>", methods=["POST"])
def add_symbol_to_portfolio(portfolio_name):
    """Add a symbol to portfolio via AJAX"""
    data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
    
    data = request.get_json() or {}
    symbol = data.get("symbol", "").strip()
    
    if not symbol:
        return jsonify({"success": False, "message": "Symbol is required."}), 400
    
    # Symbol is in format "Name (Ticker)", extract ticker
    if " (" in symbol and symbol.endswith(")"):
        ticker = symbol.split(" (")[-1].rstrip(")")
    else:
        ticker = symbol
    
    result = Portfolio.add_symbol_to_portfolio(portfolio_name, ticker, data_dir)
    return jsonify(result)


@portfolio_bp.route("/portfolio/create", methods=["GET", "POST"])
def create_portfolio():
    """Create a new portfolio"""
    data_dir = os.path.join(os.path.dirname(current_app.root_path), "data")
    
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
        
        result = Portfolio.create_portfolio(portfolio_name, currency, data_dir)

        print(result)
        
        if result["success"]:
            flash(result["message"], "success")
            return redirect(url_for("portfolio_bp.portfolio"))
        else:
            flash(result["message"], "error")
            return redirect(url_for("portfolio_bp.create_portfolio"))
