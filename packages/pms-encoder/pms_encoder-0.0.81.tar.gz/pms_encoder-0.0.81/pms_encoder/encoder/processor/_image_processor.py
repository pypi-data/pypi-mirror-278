import time
import os
import shutil
from loguru import logger
from queue import Queue
from PIL import Image
from ..redis._progress import save_progress
from ..utils._calculate_progress import check_progress
from ..utils._image_queue_object_generator import ImageQueueObjectGenerator
from ..utils._image_ffmpeg_cmd_generator import get_media_metadata
from ..utils._zip_util import zip_directory
from ..repository._image_meta_repo import get_images_meta, get_upload_file, insert_image_file_pixell_meta
from ...common._config import *
from ...common._s3_client import S3Client
from ...common._encrypt import Encrypt

def insert_image_enqueue(
    redis_data: dict,
    frame_map: dict,
    enqueue: Queue
) -> None:
    logger.info("INIT || insert_image_enqueue")
    
    images = get_images_meta(redis_data["fileKey"], redis_data["combined"])
    logger.debug("image count {}".format(len(images)))
    object_generator = ImageQueueObjectGenerator(
        redis_data,
    )
    
    frame_id = 0
    for image in images:
        frame_id += 1
        object_generator.make_queue_object(
            frame_id=frame_id,
            image_data=image,
            frame_map=frame_map,
            enqueue=enqueue
        )
    enqueue.put(None)
    logger.info("COMPLETE || insert_image_enqueue")
    
def spand_frames(
    n_worker: int,
    dequeue: Queue,
    spand_queue: Queue,
):
    logger.info("INIT || spand_frames")
    idx = 1
    temp_state = {}
    while True:
        data: EngineIOData = dequeue.get()
        if data == None:
            n_worker -= 1
            if n_worker == 0:
                spand_queue.put(None)
                break
            else:
                continue
        key = data.frame_id
        temp_state[key] = data
        while idx in temp_state:
            target_item: EngineIOData = temp_state.pop(idx)
            assert target_item.frame_id == idx
            spand_queue.put(target_item)
            logger.debug(f"spand queue put {target_item.frame_id}")
            idx += 1
    logger.info("COMPLETE || spand_frames")
    

def save_frames(
    redis_data: dict,
    frame_map: dict,
    spand_queue: Queue,
):
    logger.info("INIT || save_frames")
    t1 = time.time()
    frame_id = 0
    while True:
        if spand_queue.qsize() == 0:
            logger.debug("spand_queue empty")
            time.sleep(0.3)
            continue
        frame_id += 1
        image_data: EngineIOData = spand_queue.get()
        if image_data is None:
            logger.debug(">>> EngineIOData is None Break loop")
            break
        
        idx = image_data.frame_id
        row_data = image_data.frame
        
        if redis_data["combined"] == "N":
            upload_file = get_upload_file(
                file_key=redis_data["fileKey"]
            )
            save_file_path = "{}{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], upload_file["file_type"].lower())
        else:
            if not os.path.exists("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"])):
                os.makedirs("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]))
                
            save_file_path = "{}{}/{}".format(
                WORK_ROOT_DIR,
                redis_data["fileKey"],
                frame_map[str(idx)]["file_name"]
            )
        save_image = Image.fromarray(row_data)
        save_image.save(save_file_path)
        
        inferenced_meta_data = get_media_metadata(
            save_file_path
        )
        inferenced_size = os.path.getsize(save_file_path)
        
        insert_image_file_pixell_meta(
            frame_id=image_data.frame_id,
            frame_map=frame_map,
            meta_data=inferenced_meta_data,
            file_size=inferenced_size,
        )
        
        # if redis_data["combined"] == "Y":
        #     save_progress(
        #         redis_data["fileKey"],
        #         check_progress(
        #             redis_data["fileKey"], frame_id, count, t1, time.time()
        #         )
        #     )

def upload_workdone_files(
    redis_data: dict,
):

    s3_client = S3Client()


    if redis_data["combined"] == "N":

        output_file_path = f"{WORK_ROOT_DIR}{redis_data['fileKey']}.{redis_data['format'].lower()}"
        upload_response = s3_client.upload_file(
            file_name=output_file_path,
            original_file_name=redis_data["fileName"],
            object_name=os.getenv("S3_UPLOAD_PATH").format(
                Encrypt().base62_encode(redis_data["company"]),
                redis_data["fileKey"],
                redis_data["format"].lower(),
            ),
        )

        logger.debug(">>> Upload Response {}", upload_response)
        os.remove(
            "{}{}.{}".format(
                WORK_ROOT_DIR,
                redis_data["fileKey"],
                redis_data["format"].lower(),
            )
        )
    else:
        last_dot_index = redis_data['fileName'].rfind('.')

        original_file_name = redis_data['fileName'][:last_dot_index]
        file_name_format = "{}.zip"
        upload_response = s3_client.upload_file(
            file_name="{}{}.zip".format(WORK_ROOT_DIR, redis_data["fileKey"]),
            original_file_name=file_name_format.format(
                original_file_name
            ),
            object_name=os.getenv("S3_UPLOAD_PATH").format(
                Encrypt().base62_encode(redis_data["company"]),
                redis_data["fileKey"],
                "zip",
            ),
        )
        logger.debug(">>> Upload Response {}", upload_response)
        shutil.rmtree("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]))

def zip_combined_files(
    redis_data: dict,
):
    zip_directory(
        "{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]),
        "{}{}.zip".format(WORK_ROOT_DIR, redis_data["fileKey"])
    )
    
        