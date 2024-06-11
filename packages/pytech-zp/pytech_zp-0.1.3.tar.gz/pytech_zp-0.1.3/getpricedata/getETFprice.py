#%%
import numpy as np
import pyodbc
import pandas as pd
class Params:
    def __init__(self):
        self.host = '172.24.144.128'
        self.user = 'fsb'
        self.password = 'fsb'
        self.database = 'wind_db'
        self.port = 1433
        self.driver = '{ODBC Driver 17 for SQL Server}'

class GetETFprice:
    def __init__(self,params):
        self.params=params
        self.connection_string = f'''
        DRIVER={self.params.driver};  
        SERVER={self.params.host},{self.params.port};  
        DATABASE={self.params.database};  
        UID={self.params.user};  
        PWD={self.params.password};  
        '''
    def getETFprice(self,ETFcode,startDate,endDate):
        
        conn = pyodbc.connect(self.connection_string)  
        cursor = conn.cursor() 
        cursor.execute(f"SELECT S_DQ_ADJHIGH H,S_DQ_ADJLOW L,S_DQ_ADJCLOSE C,S_DQ_ADJOPEN O,S_DQ_VOLUME V,TRADE_DT t FROM ChinaClosedFundEODPrice where S_INFO_WINDCODE='{ETFcode}' and convert(DATE,TRADE_DT,120) >= convert(DATE,'{startDate}',120) and convert(DATE,TRADE_DT,120)<=convert(DATE,'{endDate}',120) order by TRADE_DT asc")
        columns=[column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data=[dict(zip(columns,row)) for row in rows]
        df=pd.DataFrame(data)
        cursor.close()  
        conn.close()
        return df