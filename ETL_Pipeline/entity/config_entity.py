from framework.exception import MyException
from ETL_Pipeline.entity import *
import sys,os
import pandas as pd

class ETL_Pipeline_Data:
    def __init__(self):
        try:
            self.data_path = ETL_PIPELINE_DATA
        except Exception as e:
            raise MyException(e,sys)

class TradingDataConfig:
    def __init__(self,etl_pipeline_config:ETL_Pipeline_Data):
        try:
            self.etl_pipeline_config = etl_pipeline_config
            self.trading_data_dir = os.path.join(self.etl_pipeline_config.data_path,TRADING_DATA_DIR)
            # os.makedirs(self.trading_data_dir,exist_ok=True)

            self.stock_file_path = os.path.join(self.trading_data_dir,STOCK_DATA_FILE)
            self.index_file_path = os.path.join(self.trading_data_dir,INDEX_DATA_FILE)

        except Exception as e:
            raise MyException(e,sys)


