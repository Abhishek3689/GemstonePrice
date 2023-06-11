import os,sys
import pandas as pd
import numpy  as np
from src.utils import load_object
from src.exception import CustomException
from src.logger import logging

class PredictPipeline:
    def __init__(self):
        pass

    def predict(features):
        try:
            preprocessor_path=os.path.join('models','preprocessor.pkl')
            model_path=os.path.join('models','model.pkl')

            preprocessor=load_object(file_path=preprocessor_path)
            model=load_object(file_path=model_path)
            logging.info("preprocessor and model is loaded")
            data_scaled=preprocessor.transform(features)
            logging.info("prediction data is transformed ")
            pred=model.predict(data_scaled)
            return pred
            

        except Exception as e:
            logging.info("Exception occured in prediction")
            raise CustomException(e,sys)
        



class model_params:
    def __init__(self,carat:float,cut:str,color:str,clarity:str,depth:float,table:float,x:float,y:float,z:float):
        self.carat=carat
        self.cut=cut
        self.color=color
        self.clarity=clarity
        self.depth=depth
        self.table=table
        self.x=x
        self.y=y
        self.z=z

    
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'carat':[self.carat],
                'depth':[self.depth],
                'table':[self.table],
                'x':[self.x],
                'y':[self.y],
                'z':[self.z],
                'cut':[self.cut],
                'color':[self.color],
                'clarity':[self.clarity]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info('Exception Occured in prediction pipeline')
            raise CustomException(e,sys)
        
predict_df=model_params(1.52,'Premium','G','VS1',63,56,8.1,7.5,4.6)
predict_df_new=predict_df.get_data_as_dataframe()
print(predict_df_new.head())
print("==========================================================================")
result=PredictPipeline.predict(predict_df_new)
print(result)