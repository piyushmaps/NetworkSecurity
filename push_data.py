import os
import sys
import json

from dotenv import load_dotenv
import certifi  
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

#certifi:When your Python app makes a secure HTTPS request (e.g., using requests, urllib3, or even some LLM APIs), 
# it needs to validate the server’s SSL certificate to ensure the connection is secure and trustworthy.

load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

print(MONGO_DB_URL)

ca=certifi.where()
# ca here stands for “Certificate Authority.”
# You're assigning the path of the CA bundle to the variable ca,
# so you can pass it explicitly into an HTTP client like requests or urllib3.

class NetworkDataExtract():
    try:
        pass
    except Exception as e:
        raise NetworkSecurityException(e,sys)
# e is typically the original exception that was caught in a try-except block. It contains the error message and traceback of the actual exception that triggered the failure
# use of sys.Access system info or print the full traceback using sys


    #we need to take phisingData.csv and convert to json so we going to create a class
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            #need to remove the index as we don't want to add into mongodb
            data.reset_index(drop=True,inplace=True)
            #we need to convert data into key value pair {col1:data1, col2:data2}, so we makin data transpose and convert to json
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

     #The records which we created needs to be pushed to mongodb  ,database is mongodb db, collection is similar to table ofsql
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            #need to create a client to connect to the mongodb
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            #need to assign what database we are using
            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection]

            #to insert this above to the db
            self.collection.insert_many(self.records)

            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="PiyushAI"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)