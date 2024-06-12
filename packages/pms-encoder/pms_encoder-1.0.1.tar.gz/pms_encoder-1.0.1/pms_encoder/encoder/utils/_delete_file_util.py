import os
import shutil
from ...common._config import *

def delete_video_temp_files(
    redis_data: dict
) -> None:
    # best quality file
    path = "{}{}_tmp.{}".format(
        WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower()
    )
    if os.path.exists(path):
        os.remove(path)
        
    # best quality file
    path = "{}{}_max.{}".format(
        WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower()
    )
    if os.path.exists(path):
        os.remove(path)
    
    # dummy file
    path = "{}{}_dummy.{}".format(
        WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower()
    )
    if os.path.exists(path):
        os.remove(path)
        
    # two pass log file
    path = "{}{}-0.log".format(
        WORK_ROOT_DIR, redis_data["fileKey"]
    )
    if os.path.exists(path):
        os.remove(path)
        
    # two pass mbtree file
    path = "{}{}-0.log.mbtree".format(
        WORK_ROOT_DIR, redis_data["fileKey"]
    )
    if os.path.exists(path):
        os.remove(path)
        
    # audio file
    path = "{}{}_audio.{}".format(
        WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower()
    )
    if os.path.exists(path):
        os.remove(path)
        

def delete_upload_files(
    redis_data: dict
) -> None:
    if redis_data["combined"] == "Y":
        path = "{}{}".format(
            UPLOAD_ROOT_DIR, redis_data["fileKey"]
        )
        if os.path.exists(path):
            shutil.rmtree(path)
    else:
        path = redis_data["filePath"]
        if os.path.exists(path):
            os.remove(path)