import os,sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from src.utils import save_object
from src.utils import load_object
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import r2_score

@dataclass
class ModelTrainerConfig:
    model_trainer_path=os.path.join("models",'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_config=ModelTrainerConfig()

    def initiate_model_training(self,train_array,test_array):
        try:
            os.makedirs(os.path.dirname(self.model_config.model_trainer_path),exist_ok=True)
            logging.info("Model training is inititated")
            X_train,X_test,y_train,y_test=train_array[:,:-1],test_array[:,:-1],train_array[:,-1],test_array[:,-1]
        
            models={
            "Linear Regression":LinearRegression(),
            "Decision Tree":DecisionTreeRegressor(),
            "Random Forest":RandomForestRegressor(),
            "AdaBoost":AdaBoostRegressor(),
            "KNN":KNeighborsRegressor(),
            }
            def evaluate_model(models):
                report={}
                for i in range(len(models)):
                    model=list(models.values())[i]
                    model.fit(X_train,y_train)
                    y_pred=model.predict(X_test)
                    score=r2_score(y_test,y_pred)
                    report[list(models.keys())[i]]=score
                return report
            reports=evaluate_model(models)
            logging.info(f"The report of the models are \n [{reports}]")

            best_score=max(list(reports.values()))
            best_model=list(reports.keys())[np.argmax(list(reports.values()))]
            logging.info(f"Best model is {best_model} and best score is {best_score}")

            print(f"Best model is {best_model} and best score is {best_score}")

            save_object(file_path=self.model_config.model_trainer_path,obj=best_model)
            logging.info("Model is saved for prediction")

        except Exception as e:
            raise CustomException(e,sys)