import os
import csv
from datetime import datetime

class Portfolio:
    """Portfolio management class"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    @staticmethod
    def create_portfolio(portfolio_name, currency, data_dir="data"):
        """
        Create a new portfolio CSV file and record in manage_portfolio.csv
        
        Args:
            portfolio_name (str): Name of the portfolio
            currency (str): Currency type (e.g., USD, SGD, EUR)
            data_dir (str): Directory to store portfolio files
            
        Returns:
            dict: Success status and message
        """
        try:
            # Update manage_portfolio.csv with portfolio summary
            manage_portfolio_path = os.path.join(data_dir, "manage_portfolio.csv")
            
            # Check if portfolio name already exists
            if os.path.exists(manage_portfolio_path):
                with open(manage_portfolio_path, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        # Only check active portfolios
                        if row.get('Status', 'active').lower() != 'deleted':
                            if row.get('Portfolio Name', '').strip() == portfolio_name.strip():
                                return {
                                    "success": False,
                                    "message": f"Portfolio name '{portfolio_name}' already exists. Please choose a different name."
                                }
            
            # Headers for manage_portfolio.csv
            manage_headers = [
                "Portfolio Name",
                "Currency",
                "Symbols",
                "Status",
                "Cost Basis",
                "Market Value",
                "Day Change",
                "Unrealized Gain/Loss",
                "Realized Gain/Loss",
                "Created Date"
            ]
            
            # Check if manage_portfolio.csv exists
            file_exists = os.path.exists(manage_portfolio_path)
            
            with open(manage_portfolio_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write headers if file is new
                if not file_exists:
                    writer.writerow(manage_headers)
                
                # Write portfolio summary row
                created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                summary_row = [
                    portfolio_name,           # Portfolio Name
                    currency,                  # Currency
                    "0",                       # Symbols (initially 0)
                    "active",                  # Status
                    "0.0",                        # Cost Basis
                    "0.0",                        # Market Value
                    "0.0",                        # Day Change
                    "0.0",                        # Unrealized Gain/Loss
                    "0.0",                        # Realized Gain/Loss
                    created_date               # Created Date
                ]
                writer.writerow(summary_row)
            
            return {
                "success": True,
                "message": f"Portfolio '{portfolio_name}' created successfully with currency '{currency}'.",
                "filepath": manage_portfolio_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creating portfolio: {str(e)}"
            }
    
    @staticmethod
    def get_all_portfolios(data_dir="data"):
        """
        Get all portfolios from manage_portfolio.csv (only active ones)
        
        Args:
            data_dir (str): Directory containing portfolio files
            
        Returns:
            list: List of portfolio dictionaries containing metadata
        """
        portfolios = []
        manage_portfolio_path = os.path.join(data_dir, "manage_portfolio.csv")
        
        try:
            if not os.path.exists(manage_portfolio_path):
                return portfolios
            
            # Read portfolios from manage_portfolio.csv
            with open(manage_portfolio_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Only include active portfolios (skip deleted ones)
                    if row.get('Status', 'active').lower() != 'deleted':
                        portfolio_info = {
                            'portfolio_name': row.get('Portfolio Name', ''),
                            'currency': row.get('Currency', ''),
                            'symbols': row.get('Symbols', '0'),
                            'cost_basis': row.get('Cost Basis', ''),
                            'shares': row.get('Shares', ''),
                            'market_value': row.get('Market Value', ''),
                            'day_change': row.get('Day Change', ''),
                            'unrealized_gain_loss': row.get('Unrealized Gain/Loss', ''),
                            'realized_gain_loss': row.get('Realized Gain/Loss', ''),
                            'created_date': row.get('Created Date', '')
                        }
                        portfolios.append(portfolio_info)
            
            return portfolios
        
        except Exception as e:
            print(f"Error reading portfolios from manage_portfolio.csv: {str(e)}")
            return []
    
    @staticmethod
    def get_portfolio_by_name(portfolio_name, data_dir="data"):
        """
        Get a single active portfolio by name.
        """
        manage_portfolio_path = os.path.join(data_dir, "manage_portfolio.csv")
        try:
            if not os.path.exists(manage_portfolio_path):
                return None

            with open(manage_portfolio_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get('Status', 'active').lower() != 'deleted' and row.get('Portfolio Name', '').strip() == portfolio_name.strip():
                        return {
                            'portfolio_name': row.get('Portfolio Name', ''),
                            'currency': row.get('Currency', ''),
                            'symbols': row.get('Symbols', '0'),
                            'cost_basis': row.get('Cost Basis', ''),
                            'shares': row.get('Shares', ''),
                            'market_value': row.get('Market Value', ''),
                            'day_change': row.get('Day Change', ''),
                            'unrealized_gain_loss': row.get('Unrealized Gain/Loss', ''),
                            'realized_gain_loss': row.get('Realized Gain/Loss', ''),
                            'created_date': row.get('Created Date', '')
                        }
            return None
        except Exception as e:
            print(f"Error reading portfolio from manage_portfolio.csv: {str(e)}")
            return None

    @staticmethod
    def update_portfolio(portfolio_name, new_name, currency, data_dir="data"):
        """
        Edit portfolio name and currency in manage_portfolio.csv.
        """
        manage_portfolio_path = os.path.join(data_dir, "manage_portfolio.csv")
        try:
            if not os.path.exists(manage_portfolio_path):
                return {
                    "success": False,
                    "message": "Manage portfolio file not found."
                }

            rows = []
            with open(manage_portfolio_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                for row in reader:
                    rows.append(row)
            print(f">>>update_portfolio before update:{rows}")

            found = False
            if new_name.strip().lower() != portfolio_name.strip().lower():
                for row in rows:
                    if row.get('Status', 'active').lower() != 'deleted' and row.get('Portfolio Name', '').strip().lower() == new_name.strip().lower():
                        return {
                            "success": False,
                            "message": f"Portfolio name '{new_name}' already exists."
                        }

            for row in rows:
                if row.get('Status', 'active').lower() != 'deleted' and row.get('Portfolio Name', '').strip() == portfolio_name.strip():
                    found = True
                    row['Portfolio Name'] = new_name
                    row['Currency'] = currency
                    break

            if not found:
                return {
                    "success": False,
                    "message": f"Portfolio '{portfolio_name}' not found."
                }
            
            print(f">>>update_portfolio after update:{rows}")

            with open(manage_portfolio_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)

            return {
                "success": True,
                "message": f"Portfolio '{portfolio_name}' has been updated successfully."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error editing portfolio: {str(e)}"
            }
    
    @staticmethod
    def delete_portfolio(portfolio_name, data_dir="data"):
        """
        Mark a portfolio as deleted in manage_portfolio.csv
        
        Args:
            portfolio_name (str): Portfolio name to delete
            data_dir (str): Directory containing portfolio files
            
        Returns:
            dict: Success status and message
        """
        manage_portfolio_path = os.path.join(data_dir, "manage_portfolio.csv")
          
        try:
            if not os.path.exists(manage_portfolio_path):
                return {
                    "success": False,
                    "message": f"Manage portfolio file not found."
                }
            
            # Read all rows from manage_portfolio.csv
            rows = []
            with open(manage_portfolio_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames
                for row in reader:
                    rows.append(row)
            
            
            # Update the status of the portfolio to 'deleted'
            found = False
            for row in rows:
                if row.get('Portfolio Name', '').strip() == portfolio_name.strip():
                    row['Status'] = 'deleted'
                    found = True
                    break
            
            if not found:
                return {
                    "success": False,
                    "message": f"Portfolio '{portfolio_name}' not found."
                }
            
            # Write back the updated rows to manage_portfolio.csv
            with open(manage_portfolio_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(rows)
            
            return {
                "success": True,
                "message": f"Portfolio '{portfolio_name}' has been deleted successfully."
            }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting portfolio: {str(e)}"
            }
