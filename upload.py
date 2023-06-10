import os
import sys
import pandas as pd
from src.logger import logging
import json
from pymongo.mongo_client import MongoClient
import certifi
ca = certifi.where()

uri = "mongodb+srv://abhisheknishad:abhisheknishad@cluster0.rgawbxa.mongodb.net/?retryWrites=true&w=majority"
client=MongoClient(uri,tlsCAFile=ca)

logging.info("Connection with mongo db is established")

db_name='Gemstone'
collection_name='gems_price'
collection=client[db_name][collection_name]

df=pd.DataFrame(list(collection.find()))
logging.info("Dataframe has been loaded in df variable")

if '_id' in df.columns:
    df=df.drop('_id',axis=1)
df.to_csv('files/gems.csv',index=False)
logging.info("File is saved in folder")
print(df.head())




def upload_data(df):
    if '_id' in df.columns:
        df=df.drop('_id',axis=1)
    logging.info("Dataframe has been loaded in df variable")
    #print(df.head())

    db_name='Gemstone'
    collection_name='gems_price'
    collection=client[db_name][collection_name]
    logging.info("Saving in Mongo is initiated")

    json_reocrd=list(json.loads(df.T.to_json()).values())
    collection.insert_many(json_reocrd)
    logging.info("File is saved in Mongo DB")

# upload_data(df_gem)
# logging.info("gems is uploaded")
