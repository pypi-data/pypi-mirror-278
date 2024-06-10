import subprocess
import time
import shutil
from queue import Queue
from loguru import logger
from ..utils._video_queue_object_generator import VideoQueueObjectGenerator
from ..utils._video_ffmpeg_cmd_generator import *
from ..utils._calculate_progress import check_progress
from ..utils._zip_util import zip_directory
from ..redis._progress import save_progress
from ..repository._video_meta_repo import insert_inferenced_file_meta
from ...common._config import *
from ...common._s3_client import S3Client
from ...common._encrypt import Encrypt
from pms_inference_engine.data_struct import EngineIOData


def split_frames(
    redis_data: dict,
    meta_data: dict,
    audio: str,
    enqueue: Queue,
) -> None:
    logger.info("INIT || split_frames")
    args = split_frame_command(redis_data, audio)
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    
    object_generator = VideoQueueObjectGenerator(
        process,
        redis_data,
        meta_data,
    )

    frame_id = 0
    while True:
        if enqueue.qsize() == int(os.getenv("MAX_QUEUE_SIZE")):
            logger.debug("enqueue capacity reached")
            time.sleep(0.3)
            continue
        frame_id += 1
        executed = object_generator.make_queue_object(
            frame_id, enqueue
        )
        
        if not executed:
            # end of frames
            enqueue.put(None)
            break
    logger.info("COMPLETE || split_frames")


def spand_frames(
    n_worker: int,
    dequeue: Queue,
    spand_queue: Queue,
) -> None:
    logger.info("INIT || spand_frames")
    idx = 1
    temp_state = {}
    while True:
        data: EngineIOData = dequeue.get()
        if data == None:
            n_worker -= 1
            if n_worker == 0:
                spand_queue.put(None)
                break  # end of sequence
            else:
                continue
        logger.debug(f"receive {data.frame_id}")
        key = data.frame_id
        temp_state[key] = data
        while idx in temp_state:
            target_item: EngineIOData = temp_state.pop(idx)
            assert target_item.frame_id == idx
            spand_queue.put(target_item)
            logger.debug(f"spand queue put {target_item.frame_id}")
            idx += 1
    logger.info("COMPLETE || spand_frames")
    
    
def merge_frames(
    redis_data: dict,
    meta_data: dict,
    spand_queue: Queue,
) -> None:
    logger.info("INIT || merge_frames")
    t1 = time.time()
    args = merge_frame_command(redis_data, meta_data)
    process = subprocess.Popen(args, stdin=subprocess.PIPE)
    frame_id = 0
    while True:
        if spand_queue.qsize() == 0:
            logger.debug("spand queue empty")
            time.sleep(0.3)
            continue
        frame_id += 1
        
        image: EngineIOData = spand_queue.get()
        if image is None:
            break
        idx = image.frame_id
        row_data = image.frame
        
        process.stdin.write(row_data.tobytes())
        logger.debug(f"frame {idx} merge complete")
        
        if frame_id % 10 == 0:
            logger.warning(
                check_progress(
                    redis_data["fileKey"], frame_id, int(meta_data["nb_frames"]), t1, time.time()
                )
            )
            save_progress(
                redis_data["fileKey"],
                check_progress(
                    redis_data["fileKey"], frame_id, int(meta_data["nb_frames"]), t1, time.time()
                )
            )
            
    process.stdin.close()
    process.wait()
    logger.info("COMPLETE || merge_frames")


def two_pass_encoding(
    redis_data: dict,
    meta_data: dict,
) -> None:
    logger.info("INIT || two_pass_encoding")
    
    args = generate_two_pass_log_file_command(redis_data, meta_data)
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    process.wait()
    
    args = two_pass_encode_command(redis_data, meta_data)
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    process.wait()
    
    logger.info("COMPLETE || two_pass_encoding")
    
    
def merge_audio(
    redis_data: dict,
    audio: str,
) -> None:
    logger.info("INIT || merge_audio")
    
    if audio == "N":
        shutil.move(
            "{}{}_tmp.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower()),
            "{}{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower())
        )
    else:
        args = merge_audio_command(redis_data)
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        process.wait()
        
    logger.info("COMPLETE || merge_audio")
    
    
def save_inferenced_meta(
    redis_data: dict,
    meta_data: dict, 
    audio: str
) -> None:
    logger.info("INIT || save_inferenced_meta")
    
    probe = ffmpeg.probe("{}{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower()))
    inferenced_data = next(s for s in probe["streams"] if s["codec_type"] == "video")
    format_data = probe.get("format", {})
    inferenced_size = os.path.getsize("{}{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower()))
    
    insert_inferenced_file_meta(
        redis_data=redis_data,
        original_data=meta_data,
        inferenced_data=inferenced_data,
        format_data=format_data,
        file_size=inferenced_size,
        audio=audio,
    )
    logger.info("COMPLETE || save_inferenced_meta")
    

# def downscale_sub_output(
#     redis_data: dict,
#     meta_data: dict,
# ) -> None:
#     logger.info("INIT || downscale_sub_output")
#     output_file_path = "{}{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower())
#     zip_file_path = "{}{}.zip".format(WORK_ROOT_DIR, redis_data["fileKey"])
#     if redis_data.get("subOutput") == "Y":
#         # make temp directory
#         if not os.path.exists("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"])):
#             os.makedirs("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]))
#         # generate sub_output
#         last_dot_index = redis_data["fileName"].rfind('.')
#         original_file_name = redis_data["fileName"][:last_dot_index]
#         sub_output_path = "{}{}/{}_{}x{}.{}".format(
#             WORK_ROOT_DIR,
#             redis_data["fileKey"],
#             original_file_name,
#             redis_data["resizeWidth"],
#             redis_data["resizeHeight"],
#             redis_data["format"]
#         )
#
#         args = generate_sub_output(
#             redis_data,
#             output_file_path,
#             sub_output_path
#         )
#
#         process = subprocess.Popen(args, stdout=subprocess.PIPE)
#         process.wait()
#
#         shutil.move(
#             output_file_path,
#             "{}{}/{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], original_file_name, redis_data["format"])
#         )
#
#         # zip
#         zip_directory("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]), zip_file_path)
#
#         # move download file
#         download_zip_file_path = "{}{}.zip".format(DOWNLOAD_ROOT_DIR, redis_data["fileKey"])
#         shutil.move(
#             zip_file_path,
#             download_zip_file_path
#         )
#
#         # delete temp directory
#         shutil.rmtree("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]))
#
#     else:
#         download_file_path = "{}{}.{}".format(DOWNLOAD_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower())
#         shutil.move(
#             output_file_path,
#             download_file_path
#         )
#     logger.info("COMPLETE || downscale_sub_output")


def downscale_and_upload(
        redis_data: dict,
        meta_data: dict,
) -> None:
    logger.info("INIT || downscale_sub_output")
    output_file_path = "{}{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower())
    zip_file_path = "{}{}.zip".format(WORK_ROOT_DIR, redis_data["fileKey"])

    last_dot_index = redis_data["fileName"].rfind('.')
    original_file_name = redis_data["fileName"][:last_dot_index]
    file_name_format = "{}.{}"

    s3_client = S3Client()

    if redis_data.get("subOutput") == "Y":
        # make temp directory
        if not os.path.exists("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"])):
            os.makedirs("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]))
        # generate sub_output

        sub_output_path = "{}{}/{}_{}x{}.{}".format(
            WORK_ROOT_DIR,
            redis_data["fileKey"],
            original_file_name,
            redis_data["resizeWidth"],
            redis_data["resizeHeight"],
            redis_data["format"]
        )

        args = generate_sub_output(
            redis_data,
            output_file_path,
            sub_output_path
        )

        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        process.wait()

        shutil.move(
            output_file_path,
            "{}{}/{}.{}".format(WORK_ROOT_DIR, redis_data["fileKey"], original_file_name, redis_data["format"])
        )

        # zip
        zip_directory("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]), zip_file_path)

        # move download file
        download_zip_file_path = "{}{}.zip".format(DOWNLOAD_ROOT_DIR, redis_data["fileKey"])

        upload_response = s3_client.upload_file(
            file_name=zip_file_path,
            original_file_name=file_name_format.format(
                original_file_name,
                "zip",
            ),
            object_name=os.getenv("S3_UPLOAD_PATH").format(
                Encrypt().base62_encode(redis_data["company"]),
                redis_data["fileKey"],
                "zip",
            ),
        )

        # delete temp directory
        shutil.rmtree("{}{}".format(WORK_ROOT_DIR, redis_data["fileKey"]))

    else:
        download_file_path = "{}{}.{}".format(DOWNLOAD_ROOT_DIR, redis_data["fileKey"], redis_data["format"].lower())

        # upload to s3
        upload_response = s3_client.upload_file(
            file_name=output_file_path,
            original_file_name=file_name_format.format(
                original_file_name,
                redis_data["format"].lower(),
            ),
            object_name=os.getenv("S3_UPLOAD_PATH").format(
                Encrypt().base62_encode(redis_data["company"]),
                redis_data["fileKey"],
                redis_data["format"].lower(),
            ),
        )
        logger.debug(">>> Upload Response {}", upload_response)

        os.remove(
            output_file_path
        )
    logger.info("COMPLETE || downscale_sub_output")