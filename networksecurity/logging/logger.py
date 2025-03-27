import logging
import os
from datetime import datetime


#create the date time of now, strftime will give the  format in month,date,year is mentioned inside
#  The .log extension is appended to create a unique log file name for each run.
# 03_25_2025_14_30_45.log

LOG_FILE=f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log"

#getcwd ,will give the currrent directory path,"logs" folder where log wil be stored
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)

#exist_ok mean if logs_path exist then do not create,this will create logs directory
os.makedirs(logs_path, exist_ok=True)


#This ensures that the log file is stored in a structured directory instead of cluttering the main project folder.

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

# Where to store logs (LOG_FILE_PATH)
# ✅ What format to use for log messages
# ✅ What level of logs to capture, we can capture error ,warnings etc

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)