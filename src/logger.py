import logging
import os
import sys
from datetime import datetime


log_name=f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
log_path=os.path.join('logs',log_name)


os.makedirs(log_path,exist_ok=True)
log_file_path=os.path.join(log_path,log_name)
logging.basicConfig(filename=log_file_path,level=logging.DEBUG,format="[%(asctime)s] %(levelname)s %(lineno)d %(message)s")

