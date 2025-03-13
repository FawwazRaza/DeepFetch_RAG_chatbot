
import shutil
import os

shutil.rmtree('./data_store', ignore_errors=True)
os.makedirs('./data_store')