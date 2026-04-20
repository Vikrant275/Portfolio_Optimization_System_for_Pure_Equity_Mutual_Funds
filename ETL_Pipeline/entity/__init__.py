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