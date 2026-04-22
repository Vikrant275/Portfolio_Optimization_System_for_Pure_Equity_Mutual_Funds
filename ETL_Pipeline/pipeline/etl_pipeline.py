import sys

import pandas as pd

from ETL_Pipeline.components.get_audit_data import GetAuditData
from framework.exception import MyException
from framework.logger import logging

from ETL_Pipeline.components.login_auth import login

from ETL_Pipeline.components.get_risk_data import GetRiskData
from ETL_Pipeline.components.get_trading_Data import GetTradingData
from ETL_Pipeline.components.merge_data_frame import MergeDataFrame

from ETL_Pipeline.entity.config_entity import TradingDataConfig,ETL_Pipeline_Data,RiskDataConfig,AuditDataConfig,FinalDataConfig

from src.utils.utils import generate_semesters




class ETLPipeline:
    def __init__(self,stock):
        self.stock = stock
        self.etl_pipeline_config = ETL_Pipeline_Data(self.stock)

    def start_get_trading_data(self,start_date,end_date):
        try:
            logging.info("Start getting trading data")
            print('Start getting trading data')

            trading_data_config = TradingDataConfig(self.etl_pipeline_config)
            get_data = GetTradingData(trading_data_config)
            trading_data = get_data.get_trading_data(self.stock, start_date, end_date)
            logging.info(f"End getting trading data {trading_data} ")
            print(f'End getting trading data {trading_data}')

            return trading_data

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def start_get_risk_data(self,token,start_date,end_date):
        try:
            logging.info(f"Start getting risk data {start_date}-{end_date}")
            print(f'Start getting risk data {start_date}-{end_date}')

            risk_data_config = RiskDataConfig(self.etl_pipeline_config)
            get_data = GetRiskData(risk_data_config)
            risk_data = get_data.get_risk_data(self.stock,token, start_date, end_date)
            logging.info(f"End getting risk data {risk_data} ")
            return risk_data

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def start_get_audit_data(self,token,start_date,end_date):
        try:
            logging.info("Start getting audit data")
            print('Start getting audit data')
            audit_data_config = AuditDataConfig(self.etl_pipeline_config)
            get_data = GetAuditData(audit_data_config)

            audit_data = get_data.get_audit_data(self.stock, token,start_date,end_date)
            logging.info(f"End getting audit data {audit_data} ")
            return audit_data

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


    def join_data(self,trading_data,risk_data,audit_data):
        try:
            logging.info("Joining data")
            trading_df = pd.read_csv(trading_data.stock_data_path)
            trading_df = trading_df.iloc[1:]
            logging.info("load successfully trading csv file in dataframe")

            risk_df = pd.read_csv(risk_data.risk_data_path)
            logging.info("load successfully risk csv file in dataframe")

            audit_df = pd.read_csv(audit_data.audit_file_path)
            logging.info("load successfully audit csv file in dataframe")

            merge_df_config  = FinalDataConfig(self.etl_pipeline_config)
            merge_df_obj = MergeDataFrame(merge_df_config)
            merged_df = merge_df_obj.build_merge_dataframe(trading_df, risk_df, audit_df)
            logging.info(f"merge successfully merged dataframe at [{merged_df}] ")

            return merged_df

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)


if __name__ == '__main__':
    try:

        stocks = input('Enter stock code: ').split(',')
        in_start = input("Enter the start date: ")
        in_end = input("Enter the end date: ")

        for stock in stocks:
            data_trading = ETLPipeline(stock).start_get_trading_data(in_start, in_end)

            # Risk Data
            token = login("vikrant", "password123")
            semesters = generate_semesters(start_date=in_start, end_date=in_end)
            for sem in semesters:
                data_risk = ETLPipeline(stock).start_get_risk_data(token, sem[0], sem[1])
                data_audit = ETLPipeline(stock).start_get_audit_data(token, sem[0], sem[1])

            final_data = ETLPipeline(stock).join_data(data_trading, data_risk, data_audit)

            print(
                f"trading artifact config : {data_trading} \n risk artifact config : {data_risk} \n audit artifact config : {data_audit}\n final data artifact config : {final_data}")

        # # Trading Data
        # data_trading = ETLPipeline().start_get_trading_data(stock,in_start,in_end)
        #
        # # Risk Data
        # token = login("vikrant", "password123")
        # semesters = generate_semesters(start_date=in_start,end_date=in_end)
        # for sem in semesters:
        #     data_risk = ETLPipeline().start_get_risk_data(stock,token,sem[0],sem[1])
        #     data_audit = ETLPipeline().start_get_audit_data(stock, token,sem[0],sem[1])
        #
        #
        # final_data = ETLPipeline().join_data(data_trading,data_risk,data_audit)
        #
        # print(
        #     f"trading artifact config : {data_trading} \n risk artifact config : {data_risk} \n audit artifact config : {data_audit}\n final data artifact config : {final_data}")

    except Exception as e:
        raise MyException(e,sys)




