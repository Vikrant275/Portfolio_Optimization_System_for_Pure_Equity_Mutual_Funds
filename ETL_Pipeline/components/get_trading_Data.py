import os,sys

import yfinance as yf
import pandas as pd
from ETL_Pipeline.entity.data_entity import Trading_data
from ETL_Pipeline.entity.config_entity import TradingDataConfig
from framework.exception import MyException
from framework.logger import logging


class GetTradingData:
    def __init__(self,trading_data_config:TradingDataConfig):
        try:
            self.trading_data_config = trading_data_config

        except MyException as e:
            raise MyException(e,sys)


    def get_trading_data(self,stock,start,end) -> Trading_data :
        try:
            stock_df = yf.download(f"{stock}.NS", start=start, end=end,interval='1d')

            if stock_df.empty:
                logging.fatal(f"No data found for {stock} for {start} to {end}")
                raise MyException(f"{stock} is empty data for {start} to {end}")

            market_df = yf.download("^NSEI", start=start, end=end)

            if market_df.empty:
                logging.fatal(f"No data found NSE_INDEX for {start} to {end}")
                raise MyException(f"{stock} is empty data for {start} to {end}")

            stock_df.reset_index(inplace=True)
            market_df.reset_index(inplace=True)
            stock_df['stock'] = stock



            os.makedirs(self.trading_data_config.trading_data_dir, exist_ok=True)
            logging.info(f"successfully created {self.trading_data_config.trading_data_dir} ")

            stock_df.to_csv(self.trading_data_config.stock_file_path, index=False)
            logging.info(f"successfully created {self.trading_data_config.stock_file_path} ")

            market_df.to_csv(self.trading_data_config.index_file_path, index=False)
            logging.info(f"successfully created {self.trading_data_config.index_file_path} ")

            trading_data = Trading_data(
                stock_data_path=self.trading_data_config.stock_file_path,
                nse_index_data_path=self.trading_data_config.index_file_path
            )

            return trading_data

        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)









