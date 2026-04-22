import os

import pandas as pd
from typing import Tuple
import sys

from framework.exception import MyException
from framework.logger import logging

from ETL_Pipeline.entity.config_entity import FinalDataConfig
from ETL_Pipeline.entity.data_entity import Final_data

def _prepare_date_column(
        stock_df: pd.DataFrame,
        risk_df: pd.DataFrame,
        audit_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        stock_df= stock_df.copy()
        risk_df= risk_df.copy()
        audit_df= audit_df.copy()

        #convert to datetime
        stock_df['Date'] = pd.to_datetime(stock_df['Date'],errors='coerce')
        risk_df['start_date'] = pd.to_datetime(risk_df['start_date'],errors='coerce')
        risk_df['end_date'] = pd.to_datetime(risk_df['end_date'],errors='coerce')

        audit_df['start_date'] = pd.to_datetime(audit_df['start_date'],errors='coerce')
        audit_df['end_date'] = pd.to_datetime(audit_df['end_date'],errors='coerce')

        return stock_df, risk_df, audit_df

    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)

def _validate_inputs(
        stock_df: pd.DataFrame,
        risk_df: pd.DataFrame,
        audit_df: pd.DataFrame,
)->None:
    try:
        '''Basic schema validation.'''
        logging.info("Basic schema validation.")
        required_stock_cols = {'Date','stock'}
        required_risk_cols = {'stock','start_date','end_date'}
        required_audit_cols = {'stock','start_date','end_date'}

        if not required_stock_cols.issubset(stock_df.columns):
            logging.error(f"{required_stock_cols} columns not present in stock dataframe.")
            raise ValueError(f"{required_stock_cols} columns not present in stock dataframe.")

        if not required_risk_cols.issubset(risk_df.columns):
            logging.error(f"{required_risk_cols} columns not present in risk dataframe.")
            raise ValueError(f"{required_risk_cols} columns not present in risk dataframe.")

        if not required_audit_cols.issubset(audit_df.columns):
            logging.error(f"{required_audit_cols} columns not present in audit dataframe.")
            raise ValueError(f"{required_audit_cols} columns not present in audit dataframe.")

    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)

def _range_merge(
        left:pd.DataFrame,
        right:pd.DataFrame,
        date_col:str,
        prefix:str
) ->pd.DataFrame :
    try:
        logging.info('Perform efficient range join using merge_asof + filtering')

        right = right.sort_values(['stock','start_date'])
        left = left.sort_values(['stock',date_col])

        merged = pd.merge_asof(
            left,
            right,
            left_on=date_col,
            right_on='start_date',
            by='stock',
            direction='backward',
            suffixes=("",f'_{prefix}')
        )

        merged = merged[merged[date_col] <= merged['end_date']]

        return merged

    except Exception as e:
        logging.error(e)
        raise MyException(e,sys)




class MergeDataFrame:
    def __init__(self,final_data_config:FinalDataConfig):
        self.final_data_config = final_data_config

    def build_merge_dataframe(self,
            stock_df: pd.DataFrame,
            risk_df: pd.DataFrame,
            audit_df: pd.DataFrame,
    ) -> Final_data:
        try:
            """
               Enrich stock data with risk and audit metrics using time-window joins.

               Returns:
                   pd.DataFrame: merged dataset
               """
            stock_df, risk_df, audit_df = _prepare_date_column(
                stock_df, risk_df, audit_df
            )
            logging.info('successfully datetime convert')

            _validate_inputs(stock_df, risk_df, audit_df)
            logging.info('successfully validate inputs')

            # merged risk df
            merged = _range_merge(stock_df, risk_df, date_col='Date', prefix='risk')

            # merge audit df
            merged = _range_merge(merged, audit_df, date_col='Date', prefix='audit')

            final_df = merged.reset_index(drop=True)

            # save in file path
            os.makedirs(self.final_data_config.final_data_dir, exist_ok=True)
            logging.info('successfully create final data frame')

            final_df.to_csv(self.final_data_config.final_data_file_path, index=False)

            final_data = Final_data(
                Final_df=self.final_data_config.final_data_file_path
            )

            return final_data

        except Exception as e:
            logging.error(e)
            raise MyException(e, sys)
