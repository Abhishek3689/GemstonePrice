import os,sys
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

if __name__=='__main__':
    obj=DataIngestion()
    train_data_path,test_data_path=obj.initiate_data_ingestion()
    data_transform=DataTransformation()
    train_arr,test_arr=data_transform.initiate_data_transformer(train_data_path,test_data_path)
    model_train=ModelTrainer()
    model_train.initiate_model_training(train_arr,test_arr)
    

