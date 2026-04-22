from framework.exception import MyException
from ETL_Pipeline.entity import *
import sys,os
import pandas as pd

class ETL_Pipeline_Data:
    def __init__(self,stock):
        try:
            self.data = ETL_PIPELINE_DATA
            self.stock_data_path = f"{stock}_DATA"
            self.data_path = os.path.join(self.data,self.stock_data_path
                                          )
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

class RiskDataConfig:
    def __init__(self,etl_pipeline_config:ETL_Pipeline_Data):
        try:
            self.etl_pipeline_config = etl_pipeline_config
            self.risk_data_dir = os.path.join(self.etl_pipeline_config.data_path,RISK_DATA_DIR)
            self.risk_data_file_path = os.path.join(self.risk_data_dir,RISK_DATA_FILE)

        except Exception as e:
            raise MyException(e,sys)


class AuditDataConfig:
    def __init__(self,etl_pipeline_config:ETL_Pipeline_Data):
        try:
            self.etl_pipeline_config = etl_pipeline_config
            self.audit_data_dir = os.path.join(self.etl_pipeline_config.data_path,AUDIT_DATA_DIR)
            self.audit_file_path = os.path.join(self.audit_data_dir,AUDIT_DATA_FILE)

        except Exception as e:
            raise MyException(e,sys)
class FinalDataConfig:
    def __init__(self,etl_pipeline_config:ETL_Pipeline_Data):
        try:
            self.etl_pipeline_config = etl_pipeline_config
            self.final_data_dir = os.path.join(self.etl_pipeline_config.data_path,FINAL_DATAFRAME)
            self.final_data_file_path = os.path.join(self.final_data_dir,FINAL_DATAFRAME_FILE)
        except Exception as e:
            raise MyException(e,sys)


