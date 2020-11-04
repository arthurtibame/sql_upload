import os
import argparse
import pandas as pd
from datetime import datetime
from utils.c_carname import (
    extract_mp4_details, mp4_rename
)
from utils.jpg_utils import extract_jpg_details
from sqlalchemy import create_engine, types
from utils.secret import mysql_con_info
from tqdm import tqdm

OUTPUT_PATH = "./outputs"
MP4_OUTPUT_CSV = OUTPUT_PATH + "/mp4_" + datetime.now().strftime("%Y%m%d%H") + ".csv"

def check_output_csv(methods):     
    """
    if csv not existed create it !
        column:
            mp4timestamp, model, year, color, labedate, inputdate,        
    """
    if methods == 'mp4':           
        if os.path.isfile(MP4_OUTPUT_CSV):
            return True
        else:
            columns=["mp4timestamp", "model", "year", "color", "labedate"]
            return pd.DataFrame(columns=columns).to_csv(MP4_OUTPUT_CSV, encoding='utf-8-sig', index=None)
    else:
        raise ModuleNotFoundError

def write_in_csv(methods, car_details):    
    if methods == 'mp4':
        global MP4_OUTPUT_CSV
        df = pd.read_csv(MP4_OUTPUT_CSV)
        df.loc[0] = car_details    
        df.to_csv(MP4_OUTPUT_CSV, encoding='utf-8-sig', index=None, mode='a', header=False)
        return True
    else:
        raise "please input write csv method"

def mp4_process(opt):
    check_output_csv(opt.type)
    DIR_PATH = opt.input
    FILE_LIST = os.listdir(DIR_PATH)    

    for _ in tqdm(FILE_LIST):
        if _ != '.DS_Store':
            # STEP 1. get information from the file name        
            car_details =  extract_mp4_details(_)       
            
            if car_details != False: 
            # STEP 2. rename the mp4 file
                original_path = DIR_PATH + "/" + _             
                save_path = DIR_PATH + "/" + car_details["mp4timestamp"] + ".mp4"
                res = mp4_rename(original_path, save_path)
            
            # STEP 3. write in the csv file
                if res == True: # if respond successful and write into csv file
                    write_in_csv(methods='mp4', car_details=car_details.values())
    # STEP 4. insert the output csv to db
    engine = create_engine(mysql_con_info)
    df = pd.read_csv(MP4_OUTPUT_CSV,sep=',',quotechar='\'',encoding='utf8') 
    df.to_sql("carmp4",con=engine,index=False,if_exists='append') 
    # STEP 5. rename csv
    new_name = MP4_OUTPUT_CSV[:-4] + "_OK.csv"
    os.rename(MP4_OUTPUT_CSV, new_name)
    return True

def jpg_process(opt):        
    DIR_PATH = opt.input
    FILE_LIST = os.listdir(DIR_PATH)  
    
    a = [ extract_jpg_details(f).values() for f in tqdm(FILE_LIST) if f!='.DS_Store' ]
    df = pd.DataFrame(a, columns=["jpgtimestamp", "jpg_no"])

    engine = create_engine(mysql_con_info)
    # df = pd.read_csv(JPG_OUTPUT_CSV,sep=',',quotechar='\'',encoding='utf8') 
    df.to_sql("carjpg",con=engine,index=False,if_exists='append') 
    # STEP 5. rename csv
    # new_name = JPG_OUTPUT_CSV[:-4] + "_OK.csv"
    # os.rename(JPG_OUTPUT_CSV, new_name)
    return True


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str,help='input of mp4 files folder')
    parser.add_argument('--type', type=str, help='input of mp4 files folder')
    opt = parser.parse_args()
    
    if opt.input != None: 
        if opt.type == "mp4":        
            res = mp4_process(opt)        
        elif opt.type == "jpg":
            jpg_process(opt)   
    else:
        print("please input the folder path")