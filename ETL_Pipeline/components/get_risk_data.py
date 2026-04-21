import os
import sys
import pandas as pd
import requests
from ETL_Pipeline.components import *
from framework.exception import MyException
from framework.logger import logging
from ETL_Pipeline.entity.config_entity import RiskDataConfig
from ETL_Pipeline.entity.data_entity import Risk_data

URL = BASE_URL



class GetRiskData:
    def __init__(self,risk_data_config:RiskDataConfig):
        try:
            self.risk_data_config = risk_data_config
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def get_risk_data(self,stock, token, start_date, end_date) -> Risk_data:
        try:
            headers = {'Authorization': f'Bearer {token}'}
            params = {'start': start_date, 'end': end_date}

            data_json = requests.get(f'{URL}/risk/{stock}', params=params, headers=headers).json()
            logging.info(f"successfully fetched {data_json}")

            data = pd.DataFrame([data_json])
            logging.info("convert json to pandas dataframe")

            data['star_date'] = start_date
            data['end_date'] = end_date

            os.makedirs(self.risk_data_config.risk_data_dir, exist_ok=True)
            logging.info(f"successfully created {self.risk_data_config.risk_data_dir} ")

            if not os.path.isfile(self.risk_data_config.risk_data_file_path):
                data.to_csv(self.risk_data_config.risk_data_file_path, mode='w', index=False, header=True)
            else:
                data.to_csv(self.risk_data_config.risk_data_file_path,mode='a', index=False,header=False)

            logging.info(f"successfully created {self.risk_data_config.risk_data_file_path} ")

            risk_data = Risk_data(
                risk_data_path=self.risk_data_config.risk_data_file_path
            )

            return risk_data

        except Exception as e:
            logging.error(e)
            raise MyException(e, sys)


