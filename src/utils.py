import os
import sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
import json
import pickle
from pymongo.mongo_client import MongoClient
import certifi
ca = certifi.where()


def get_dataframe(db_name,collection_name):
    uri = "mongodb+srv://abhisheknishad:abhisheknishad@cluster0.rgawbxa.mongodb.net/?retryWrites=true&w=majority"
    client=MongoClient(uri,tlsCAFile=ca)

    logging.info("Connection with mongo db is established")

    # db_name='Gemstone'
    # collection_name='gems_price'
    collection=client[db_name][collection_name]

    df=pd.DataFrame(list(collection.find()))
    if '_id' in df.columns:
        df=df.drop('_id',axis=1)
    logging.info("Dataframe has been loaded in df variable")
    return df

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        logging.info("Error occured during loading of object")
        raise CustomException(e,sys)
    