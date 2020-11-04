from datetime import datetime
import os, time

def extract_mp4_details(filename: str) -> dict:
    """
    extract file details to upload to DB
        mp4timestamp -> the id of DB
        model -> car model
        year -> car's year
        color -> car's color
        labedate -> the time of the mp4 gotten        
    
    if extract the file failed the log will be 
    written in "[today's date].log"
    """
    try:
        mp4timestamp = str(time.time()) # id of db

        details = filename.split("-")    
        model = details[0] 
        year = details[1]
        color = details[2]
        labedate = details[3][:4]        

        return {"mp4timestamp": mp4timestamp, "model":model,  
                "year": year, "color": color, "labedate":labedate                
            }

    except Exception as e:
        path = "./logs"
        file_name = path + "/" + datetime.now().strftime("%Y%m%d") + ".log"
        with open(file_name, mode='a', encoding= 'utf-8') as f:
            f.write(filename + "\n")        
        return False

def mp4_rename(original_path: str, save_path: str) -> bool:
    """
    original_path -> the file wanna rename
    save_path -> the renamed file to save ( with filename )
    """
    try:
        os.rename(original_path, save_path)
        return True
    except FileNotFoundError as e:
        print(e)
        return False

