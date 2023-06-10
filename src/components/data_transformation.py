import os,sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.components.data_ingestion import DataIngestion
from src.utils import save_object

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from sklearn.impute import SimpleImputer

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('models','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info("Object Creation for preprocessing is initiated")

            num_col=['carat', 'depth', 'table', 'x', 'y', 'z']
            cat_col=['cut', 'color', 'clarity']

            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            num_pipeline=Pipeline(steps=
                        [('imputer',SimpleImputer(strategy='median')),
                        ('scaler',StandardScaler())])
            cat_pipeline=Pipeline(steps=
                        [('imputer',SimpleImputer(strategy='most_frequent')),
                        ('Encoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                        ('scaler',StandardScaler())])
            preprocessor=ColumnTransformer([("numerical Pipeline",num_pipeline,num_col),
                                    ("Categorical Pipeline",cat_pipeline,cat_col)])
            
            return preprocessor
        except Exception as e:
            logging.info("Error Occured in getting preprocessing Object")
            raise CustomException(e,sys)
    
    def initiate_data_transformer(self,train_path,test_path):
        try:
            os.makedirs(os.path.dirname(self.data_transformation_config.preprocessor_obj_file_path),exist_ok=True)
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Train and test df is loaded")
            preprocessing_obj=self.get_data_transformation_object()
            target_col='price'
            drop_col=[target_col,'id']

            input_feature_train_df=train_df.drop(target_col,axis=1)
            target_feature_train_df=train_df[target_col]

            input_feature_test_df=test_df.drop(target_col,axis=1)
            target_feature_test_df=test_df[target_col]

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocssing obj on train and test df")

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("preprocssor pikcle file is created and saved")
            return(
                train_arr,
                test_arr,
               
            )
        except Exception as e:
            logging.info("Error in transformation of preprocessor")
            raise CustomException(e,sys)



        