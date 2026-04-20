import requests,sys
from ETL_Pipeline.components import *
from framework.exception import MyException
from framework.logger import logging

URL = BASE_URL

def login(username,password):
    try:
        res = requests.post(
            f"{URL}/login",
            json={'username':username, 'password':password}
        )
        print(res.json())
        return res.json()['token']
    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)
