from sys import platform
from datetime import date, timedelta,datetime
from django.forms.models import model_to_dict
from user.file_encryptor import FileEncryptor
import math, random
import hashlib
import uuid
import os 
from pathlib import Path
allowed_image_types = ["JPEG", "PNG", "GIF", "JPG"]
allowed_file_types = ["JPEG", "PNG", "GIF", "JPG", "HTML", "PDF", "ZIP", "HTM" ,"ALL"]

def site_url():
    if "linux" in platform:
        site_url="http://takeaway.ai-being.com/api/"
        return site_url
    else:
        # site_url="http://127.0.0.1:8000/api/"
        site_url="http://127.0.0.1:8000/api/"
        return site_url

def server_path():
    if "linux" in platform:
        BASE_DIR = Path(__file__).resolve().parent.parent
        media_dir=os.path.join(BASE_DIR,'media',)
        server_path=media_dir
        return server_path
    else:
        BASE_DIR = Path(__file__).resolve().parent.parent
        media_dir=os.path.join(BASE_DIR,'media',)
        server_path=media_dir
        return server_path

def storage():
    storage = 1000
    return storage

def token_secret_key():
    secret_key = "drop-share@jeeva$kani*vichu&69_7#%%^"
    return secret_key
    
def files_encryptor():
    custom_string = 'Thamarai&kani$1997'
    # Use SHA-256 hash function to create a secure key
    hashed = hashlib.sha256(custom_string.encode('utf-8')).digest()
    encryptor = FileEncryptor(hashed)
    return encryptor

def my_hash(value):
    if value =='random':
        # Generate a random UUID
        value = uuid.uuid4()
    my_string = str(value)
    hashed_string = hashlib.sha256(my_string.encode()).hexdigest()
    return(hashed_string)

def image_check(file):
    default_img='profile_images/Default.jpg'
    if file.size>100:
        if not "." in str(file):
            return {'old_name':'Default.jpg','file':default_img}

        ext=str(file).rsplit(".",1)[1]
        
        if ext.upper() in allowed_image_types:
            unique_file_name = f"profile_images/{my_hash('random')}.{ext}"
            old_name = file.name
            file.name = unique_file_name
            return {'old_name':old_name,'file':file}
        else:
            return {'old_name':'Default.jpg','file':default_img}
    else:
        return {'old_name':'Default.jpg','file':default_img}

def file_validation(file):
    if file.size>100:
        if not "." in str(file):
            return {'message':'Invalid File','status':400}

        ext=str(file).rsplit(".",1)[1]
        if 'ALL' in allowed_file_types:
            unique_file_name = f"data_storage/{my_hash('random')}.{ext}"
            old_name = file.name
            file.name = unique_file_name
            file.size = (file.size / (1024.0 * 1024.0))
            return {'old_name':old_name,'file':file,'file_size':file.size,'status':200}
        elif ext.upper() in allowed_file_types:
            unique_file_name = f"data_storage/{my_hash('random')}.{ext}"
            old_name = file.name
            file.name = unique_file_name
            file.size = (file.size / (1024.0 * 1024.0))
            return {'old_name':old_name,'file':file,'file_size':file.size,'status':200}
        else:
            print(ext.upper())
            return {'message':'Invalid File Type','status':400}
    else:
        {'message':'Empty File','status':400}

def json_fetch_all(value):
    # Convert the 'users' model instance to a dictionary
    data_dict=[]
    for i in value:
        data_dict.append(model_to_dict(i))

    # Print the JSON representation
    return (data_dict)

def json_fetch_one(value):
    # Convert the 'users' model instance to a dictionary
    data_dict=(model_to_dict(value))
    
    # Print the JSON representation
    return (data_dict)

def today():
    return date.today()

def  last_change():
    return datetime.now()

def current_time():
    return str(datetime.today().strftime("%I:%M %p"))

def free_plan_date():
    three_months_from_now = datetime.now() + timedelta(days=3*30)
    return three_months_from_now

def str_date(dates):
    return datetime.strptime(dates, '%Y-%m-%d')