import requests,sys,os
import pandas as pd
from ETL_Pipeline.components import *
from framework.exception import MyException
from framework.logger import logging

from ETL_Pipeline.entity.config_entity import AuditDataConfig
from ETL_Pipeline.entity.data_entity import Audit_data


URL = BASE_URL



class GetAuditData:
    def __init__(self,audit_data_config:AuditDataConfig):
        try:
            self.audit_data_config = audit_data_config
        except Exception as e:
            logging.error(e)
            raise MyException(e,sys)

    def get_audit_data(self,stock, token,start_date,end_date):
        try:
            headers = {'Authorization': f'Bearer {token}'}
            data_json = requests.get(f'{URL}/audit/{stock}', headers=headers).json()
            logging.info(f'successfully fetched audit data for stock {stock}')

            data = pd.DataFrame([data_json])
            logging.info('successfully convert audit data to dataframe')

            data['start_date'] = start_date
            data['end_date'] = end_date

            os.makedirs(self.audit_data_config.audit_data_dir, exist_ok=True)
            logging.info(f'Audit data directory created at :{self.audit_data_config.audit_data_dir}')

            if not os.path.isfile(self.audit_data_config.audit_file_path):
                data.to_csv(self.audit_data_config.audit_file_path, mode='w', index=False, header=True)
            else:
                data.to_csv(self.audit_data_config.audit_file_path, mode='a', index=False, header=False)
            logging.info('successfully save audit data')

            audit_data = Audit_data(
                audit_file_path=self.audit_data_config.audit_file_path
            )

            return audit_data

        except Exception as e:
            logging.error(e)
            raise MyException(e, sys)
