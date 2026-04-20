import sys

import requests
from ETL_Pipeline.components import *
from framework.exception import MyException
from framework.logger import logging

URL = BASE_URL

def get_risk_data(stock,token,start_date,end_date):
    try:
        headers = { 'Authorization': f'Bearer {token}' }
        params = { 'start': start_date, 'end': end_date }

        return requests.get(f'{URL}/risk/{stock}',params=params,headers=headers).json()
    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)


