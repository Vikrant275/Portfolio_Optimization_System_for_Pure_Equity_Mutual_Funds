import sys

from framework.exception import MyException
from framework.logger import logging

from ETL_Pipeline.components.login_auth import login
from ETL_Pipeline.components.get_risk_data import get_risk_data
from ETL_Pipeline.components.get_trading_Data import GetTradingData
from ETL_Pipeline.entity.config_entity import TradingDataConfig,ETL_Pipeline_Data


class ETLPipeline:
    def __init__(self):
        self.etl_pipeline_config = ETL_Pipeline_Data()

    def start_get_trading_data(self,stock,start_date,end_date):
        try:
            logging.info("Start getting trading data")
            print('Start getting trading data')

            trading_data_config = TradingDataConfig(self.etl_pipeline_config)
            get_data = GetTradingData(trading_data_config)
            trading_data = get_data.get_trading_data(stock, start_date, end_date)
            logging.info(f"End getting trading data {trading_data} ")
            print(f'End getting trading data {trading_data}')

            return trading_data

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)




if __name__ == '__main__':
    try:

        # ETLPipeline().start_get_trading_data('TCS','2015-01-01','2020-12-31')
        token = login("vikrant", "password123")

        data = get_risk_data(
            "TCS",
            token,
            "2024-01-01",
            "2025-01-01"
        )

        print(data)

    except Exception as e:
        raise MyException(e,sys)




