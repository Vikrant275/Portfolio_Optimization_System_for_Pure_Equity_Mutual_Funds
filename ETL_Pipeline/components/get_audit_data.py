import requests,sys
from ETL_Pipeline.components import *
from framework.exception import MyException
from framework.logger import logging


URL = BASE_URL

def get_audit_data(stock,token):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        return requests.get(f'{URL}/audit/{stock}',headers=headers).json()
    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)