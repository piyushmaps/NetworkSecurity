from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging  

#configuration of The Data Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pymongo
from typing import List
import pandas as pd
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
#first will reteieve data from mongodb and start reading from it
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
#we need to read data from mongodb for that we need function 
    def export_collection_as_dataframe(self):
        """
        Read data from mongodb
        """
        try:
            database_name= self.data_ingestion_config.database_name    #so you can reteive database name from dataingestionconfig class
            collection_name=self.data_ingestion_config.collection_name #to connect to the mongodb and getting name of client
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) #calling mongodb client for the connection
            collection=self.mongo_client[database_name][collection_name] 

            df=pd.DataFrame(list(collection.find())) #retrieves all documents from the MongoDB collection,returns a cursor (a generator-like object) containing all documents.
        #data when retrieved from mongodb "_id " is always being added so needed to removed that
            if "_id" in df.columns.tolist():
                df=df.drop(columns=["_id"],axis=1)       

            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    
        

    def export_data_to_feature_Store(self,dataframe: pd.DataFrame):
        try:
            feature_Store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path=os.path.dirname(feature_Store_file_path) #This function returns only the directory portion of the path "/Users/piyush/project/data/feature_store
            #otherwise if we have done dir_path=os.path.dirname(feature_Store_file_path),it would have took phising.csv as folder
            os.makedirs(dir_path)
            dataframe.to_csv(feature_Store_file_path,index=False,header=True)

            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(
                "performed trained test split on the dataframe"
            )

            logging.info(
                "Exited split_data_as_train_test method of Data_ingestion_Class "
            )

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe() #we use above function to intitate dataframe  
            dataframe=self.export_data_to_feature_Store(dataframe)
            self.split_data_as_train_test(dataframe)  

            #we require the o/p of train and test to be use so we created class in artifact entity dataartifactentity
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)