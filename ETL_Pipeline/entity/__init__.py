from framework.fetch_config import GetConfig


'''
Constants of ETL pipeline main dir
'''

ETL_PIPELINE_DATA :str = GetConfig(config_file='dir_path.yaml',variables='data').get()


'''
constants for trading data dir 
'''

TRADING_DATA_DIR = 'Trading_data'
STOCK_DATA_FILE = 'Stock.csv'
INDEX_DATA_FILE = 'Index.csv'

'''
constants for risk data dir 
'''

RISK_DATA_DIR = 'Risk_data'
RISK_DATA_FILE = 'Risk.csv'

'''
constant for Audit data dir
'''

AUDIT_DATA_DIR = 'Audit_data'
AUDIT_DATA_FILE = 'Audit.csv'

'''
constants for Portfolio data dir
'''
FINAL_DATAFRAME = 'Final_data'
FINAL_DATAFRAME_FILE = 'Final_data.csv'
