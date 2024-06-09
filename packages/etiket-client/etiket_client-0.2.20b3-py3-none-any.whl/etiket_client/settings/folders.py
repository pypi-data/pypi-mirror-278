import platform
import platformdirs as pd
import os, sys, hashlib

# TODO :: general question, should data and sql by linked to a folder on the system rather than a user folder?

def __get_base_dir():
    if platform.system() == 'Darwin':
        return os.path.expanduser("~/Library/Containers/com.qdrive.dataQruiser/Data/qdrive")
    return f"{pd.user_data_dir()}/qdrive"

def get_sql_url():
    path  = f"{__get_base_dir()}/sql/"
    if not os.path.exists(path):
        os.makedirs(path)
    return f"sqlite+pysqlite:///{path}etiket_db.sql"

def get_data_dir():
    path  = f"{__get_base_dir()}/data/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_file_dir(scope_uuid, dataset_uuid, file_uuid, version_id):
    fpath = f'{get_data_dir()}{scope_uuid}/{dataset_uuid}/{file_uuid}/{version_id}/'            
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    return fpath

def get_user_data_dir():
    python_env = hashlib.md5(sys.prefix.encode('utf-8')).hexdigest()
    path  = f"{__get_base_dir()}/user_data/{python_env}/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_log_dir():
    path  = f"{__get_base_dir()}/logs/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path