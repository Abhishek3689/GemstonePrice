import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.utils import get_dataframe
from sklearn.model_selection import train_test_split
import certifi
ca = certifi.where()

@dataclass
class DataIngestionConfig:
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','raw.csv')
    

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion is initiated")
        os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)
        df=get_dataframe(db_name='Gemstone',collection_name='gems_price')
        logging.info("Dataframe has been loaded as dataframe")
        train_df,test_df=train_test_split(df,test_size=.25,random_state=21)
        df.to_csv(self.data_ingestion_config.raw_data_path,index=False)
        train_df.to_csv(self.data_ingestion_config.train_data_path,index=False)
        test_df.to_csv(self.data_ingestion_config.test_data_path,index=False)
        logging.info("Files are saved in respective folders")
        return (self.data_ingestion_config.train_data_path,self.data_ingestion_config.test_data_path)

