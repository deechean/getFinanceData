import datetime, os
from datetime import datetime
from numpy import int16
import pandas as pd

class UnitTrustInfo():
    def __init__(
            self, ISIN, 
            name=None, 
            fund_type=None, 
            currency=None, 
            dividend_type=None, 
            dividend_period=None, 
            ticker=None, 
            launch_date=None,
            credit_rating=None,
            total_net_asset=None,
            desc = None,
            ret = None,
            risk = None
        ):
        
        self._ISIN = ISIN
        self._name = name
        self._fund_type = fund_type
        self._currency = currency
        self._dividend_type = dividend_type
        self._dividend_period = dividend_period
        self._ticker = ticker
        self._launch_date = launch_date    
        self._credit_rating = credit_rating
        self._total_net_asset = total_net_asset
        self._desc = desc
        self._ret = ret
        self._risk = risk

    @property
    def ISIN(self):
        """Get the ISIN"""
        return self._ISIN

    @ISIN.setter
    def ISIN(self, value: str):
        """Set the ISIN"""
        if len(value) != 12:
            raise ValueError("Invalid ISIN. ISIN is a 12-character string.")
        self._ISIN = value

    @property
    def name(self):
        """Get the name"""
        return self._name
    
    @name.setter
    def name(self, value: str):
        """Set the name"""
        self._name = value

    @property
    def fund_type(self):
        """Get the fund_type"""
        return self._fund_type
    
    @fund_type.setter
    def fund_type(self, value: str):
        """Set the fund_type"""
        if value.lower() not in ["equities","bonds"]:
            raise ValueError("Invalid fund type. Fund type can be either Equities or Bonds.")
        if value.lower() == "equities":
            self._fund_type = "Equities"
        else:
            self._fund_type = "Bonds"

    @property
    def currency(self):
        """Get the currency"""
        return self._currency
    
    @currency.setter
    def currency(self, value: str):
        """Set the currency"""
        if value.upper() not in ["SGD","USD","JPY"]:
            raise ValueError("Invalid currency type. Currency can only be SGD, USD or JPY.")
        self._currency = value.upper()

    @property
    def dividend_type(self):
        """Get the dividend type"""
        return self._dividend_type
    
    @dividend_type.setter
    def dividend_type(self, value: str):
        """Set the dividend type"""
        if (value is not None) or (value.upper() not in ["CASH","UNIT"]):
            raise ValueError("Invalid divident type. Dividend type can only be Cash, Unit or None.")
        
        if value is None:
            self._dividend_type = None
        elif value.upper() == "CASH":
            self._dividend_type = "Cash"
        else:
            self._dividend_type = "Unit"

    @property
    def dividend_period(self):
        """Get the dividend period"""
        return self._dividend_period
    
    @dividend_period.setter
    def dividend_period(self, value: str):
        """Set the dividend period"""
        if (value is not None) or (value.upper() not in ("YEARLY","QUATERLY","MONTHLY")):
            raise ValueError("Invalid divident period. Dividend period can only be Yearly, Quarterly, Monthly or None.")
        
        if value is None:
            self._dividend_type = None
        elif value.upper() == "YEARLY":
            self._dividend_type = "Yearly"
        elif value.upper() == "QUATERLY":
            self._dividend_type = "Quaterly"
        else:
            self._dividend_type = "Monthly"
    
    @property
    def ticker(self):
        """Get the ticker"""
        return self._ticker
    
    @ticker.setter
    def ticker(self, value: str):
        """Set the ticker"""
        self._ticker = value

    @property
    def launch_date(self):
        """Get the launch date"""
        return self._launch_date
    
    @launch_date.setter
    def launch_date(self, value: datetime):
        """Set the launch date"""
        self._launch_date = value

    @property
    def credit_rating(self):
        """Get the credit rating"""
        return self._credit_rating
    
    @credit_rating.setter
    def credit_rating(self, value: int):
        """Set the credit rating"""
        if value < 1 or value > 15:
            raise ValueError("Invalid credit rating. Credit rating is a number between 1 to 15.")
        
        self._credit_rating = value


    @property
    def desc(self):
        """Get the desc"""
        return self._desc
    
    @desc.setter
    def desc(self, value: str):
        """Set the desc"""
        self._desc = value

    @property
    def total_net_asset(self):
        """Get the total net asset"""
        return self._total_net_asset
    
    @total_net_asset.setter
    def total_net_asset(self, value: str):
        """Set the total net asset"""
        self._total_net_asset = value

    @property
    def ret(self):
        """Get the return"""
        return self._ret
    
    @ret.setter
    def ret(self, value: str):
        """Set the return"""
        if value not in ("*", "**","***", "****", "*****"):
            raise ValueError("Invalid return rating. Return rating is from * (low) to ***** (high).")
        self._ret = value

    @property
    def risk(self):
        """Get the risk"""
        return self._risk
    
    @risk.setter
    def risk(self, value: str):
        """Set the risk"""
        if value not in ("*", "**","***", "****", "*****"):
            raise ValueError("Invalid risk rating. Risk rating is from * (low) to ***** (high).")
        self._risk = value

class UnitTrustInfoList():
    def __init__(self, filename):
        self._filename = filename
        self._df_unitTrustInfo = pd.read_csv(filename)
        self._index = 0 

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._df_unitTrustInfo):
            raise StopIteration  # Signal the end of iteration
        row = self._df_unitTrustInfo.iloc[self._index]
        unit_trust = UnitTrustInfo(
            ISIN = row["ISIN"], 
            name=row["Name"], 
            fund_type=row["Fund Type"], 
            currency=row["Currency"], 
            dividend_type=row["Dividend Type"], 
            dividend_period=row["Dividend Period"], 
            ticker=row["Ticker"], 
            launch_date=row["Launch Date"],
            credit_rating=row["Credit Rating"],
            total_net_asset=row["Total Net Assets"],
            desc = row["Desc"],
            ret = row["return"],
            risk = row["risk"]
        )
        self._index += 1
        return unit_trust  
    
    def get_unittrust_by_isin(self, ISIN: str):
        
        row = self._df_unitTrustInfo[self._df_unitTrustInfo["ISIN"]==ISIN]
        unit_trust = UnitTrustInfo(
            ISIN = ISIN, 
            name=row["Name"].values[0], 
            fund_type=row["Fund Type"].values[0], 
            currency=row["Currency"].values[0], 
            dividend_type=row["Dividend Type"].values[0], 
            dividend_period=row["Dividend Period"].values[0], 
            ticker=row["Ticker"].values[0], 
            launch_date=row["Launch Date"].values[0],
            credit_rating=row["Credit Rating"].values[0],
            total_net_asset=row["Total Net Assets"].values[0],
            desc = row["Desc"].values[0],
            ret = row["return"].values[0],
            risk = row["risk"].values[0]
        )
        return unit_trust
    
    def set_unittrust_by_isin(self, unit_trust_info: UnitTrustInfo):
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Name"] = unit_trust_info.name
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Fund Type"] = unit_trust_info.fund_type
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Currency"] = unit_trust_info.currency
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Dividend Type"] = unit_trust_info.dividend_type
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Dividend Period"] = unit_trust_info.dividend_period
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Ticker"] = unit_trust_info.ticker
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Launch Date"] = unit_trust_info.launch_date
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Credit Rating"] = unit_trust_info.credit_rating        
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Total Net Assets"] = unit_trust_info.total_net_asset
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"Desc"] = unit_trust_info.desc
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"return"] = unit_trust_info.ret
        self._df_unitTrustInfo.loc[self._df_unitTrustInfo["ISIN"]==unit_trust_info.ISIN,"risk"] = unit_trust_info.risk        

        # Save the original file as another name
        old_name = self._filename
        new_name = old_name[:-4]+"_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".csv"

        if os.path.exists(self._filename):
            os.rename(old_name, new_name)
        
        self._df_unitTrustInfo.to_csv(self._filename)


if __name__ == "__main__":

    unittrust_info_list = UnitTrustInfoList("./data/unitTrust Lookup.csv")
    # unit_trust = unittrust_info_list.get_unittrust_by_isin("SG9999010490")
    for unit_trust in unittrust_info_list:
        print(f"Name: {unit_trust.name}")
        print(f"ISIN: {unit_trust.ISIN}")
        print(f"Fund Type: {unit_trust.fund_type}")
        print(f"Currency: {unit_trust.currency}")
        print(f"Dividend Type: {unit_trust.dividend_type}")
        print(f"Dividend Period: {unit_trust.dividend_period}")
        print(f"Ticker: {unit_trust.ticker}")
        print(f"Launch Date: {unit_trust.launch_date}")
        print(f"Credit Rating: {unit_trust.credit_rating}")
        print(f"Total Net Assets: {unit_trust.total_net_asset}")
        print(f"Desc: {unit_trust.desc}")
        print(f"Return: {unit_trust.ret}")
        print(f"Risk: {unit_trust.risk}")
    # unit_trust.risk = "****"
    # unittrust_info_list.set_unittrust_by_isin(unit_trust)
