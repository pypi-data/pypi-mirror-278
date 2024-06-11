import os
import asyncio
import ffmpeg
import json
import pms_inference_engine as E

from loguru import logger
from queue import Queue
from .processor import _video_processor as v_processor
from .repository._file_status_repo import *
from .repository._video_meta_repo import insert_inferenced_file_meta
from .utils import _delete_file_util as dfu
from .redis._progress import save_progress

if os.getenv("COMPUTE_UNIT") == "NPU":
    import pms_furiosa_processor
elif os.getenv("COMPUTE_UNIT") == "GPU":
    import pms_nvidia_processor


class VideoEncoder:
    def __init__(
        self,
        processor_type: str,
        number_of_processors: int,
        processor_kwargs: dict,
    ):
        logger.debug("initiate video encoder")
        self.processor_type = processor_type
        self.number_of_processors = number_of_processors
        self.processor_kwargs=processor_kwargs
        self.enqueue = Queue(
            maxsize=int(os.getenv("MAX_QUEUE_SIZE")),
        )
        self.dequeue = Queue(
            maxsize=int(os.getenv("MAX_QUEUE_SIZE")),
        )
        self.spand_queue = Queue(
            maxsize=int(os.getenv("MAX_QUEUE_SIZE")),
        )
        self.redis_data = None  # json.dumps(data)
        self.meta_data = None
        self.audio = "N"
        
    async def __call__(self, redis_data) -> None:
        logger.debug("Video Encoder Call")
        self.redis_data = redis_data
        
        # change status start
        set_start_status(redis_data["fileKey"])

        probe = ffmpeg.probe(self.redis_data["filePath"])
        self.audio = next(
            ("Y" for stream in probe["streams"] if stream["codec_type"] == "audio"),
            "N"
        )
        
        self.meta_data = next(s for s in probe["streams"] if s["codec_type"] == "video")
        # Calc framerate
        frame_rate_fraction = self.meta_data["r_frame_rate"]
        frame_rate_numerator, frame_rate_denominator = map(
            int, frame_rate_fraction.split("/")
        )
        frame_rate = frame_rate_numerator / frame_rate_denominator
        self.meta_data["frame_rate"] = frame_rate
        
        # initiate engine
        engine = E.Engine(
            processor_type=self.processor_type,
            number_of_processors=self.number_of_processors,
            processor_kwargs=self.processor_kwargs,
        )
        
        # processing
        await asyncio.gather(
            asyncio.to_thread(
                v_processor.split_frames,
                redis_data=self.redis_data,
                meta_data=self.meta_data,
                audio=self.audio,
                enqueue=self.enqueue
            ),
            asyncio.to_thread(
                engine.run,
                dequeue=self.enqueue,
                enqueue=self.dequeue
            ),
            asyncio.to_thread(
                v_processor.spand_frames,
                n_worker=engine.n_worker,
                dequeue=self.dequeue,
                spand_queue=self.spand_queue,
            ),
            asyncio.to_thread(
                v_processor.merge_frames,
                redis_data=self.redis_data,
                meta_data=self.meta_data,
                spand_queue=self.spand_queue,
            ),
            return_exceptions=False,
        )

        # set progress 100
        save_progress(
            self.redis_data["fileKey"],
            json.dumps({"progress": "100", "time": "0"}),
        )
        
        # two_pass_encoding
        if self.redis_data["bestQuality"] == "N" and self.redis_data["twoPass"] == "Y":
            await asyncio.to_thread(
                v_processor.two_pass_encoding,
                redis_data=self.redis_data,
                meta_data=self.meta_data,
            )
            
        # merge audio
        v_processor.merge_audio(self.redis_data, self.audio)
        
        # inferenced metadata save
        v_processor.save_inferenced_meta(self.redis_data, self.meta_data, self.audio)
        
        # downscale file & move download folder
        v_processor.downscale_and_upload(self.redis_data, self.meta_data)
        
        # delete worked files
        dfu.delete_video_temp_files(self.redis_data)
        
        # delete original files
        # dfu.delete_upload_files(self.redis_data)
        
        # change status end
        set_success_status(redis_data["fileKey"])
        