import uvloop
import cv2
import asyncio
import ray

import os

from loguru import logger
from .encoder._video_encoder import VideoEncoder
from .encoder._image_encoder import ImageEncoder
from pms_inference_engine import SleepAndPassProcessor, register, EngineIOData, Engine, EngineIOData, is_wrapped_ray, get_local_processor_type
from ._config import *

@register
class RzSleepAndPassProcessor(SleepAndPassProcessor):
    def __init__(self, concurrency: int, index: int, scale:float, sleep_time: float = 0.1) -> None:
        super().__init__(concurrency, index, sleep_time)
        self.scale = scale
        
    async def _run(self, input_data: EngineIOData) -> EngineIOData:
        await asyncio.sleep(self._sleep_time)
        frame = input_data.frame
        h, w, c = frame.shape
        resize_width = int(w*self.scale)
        resize_height = int(h*self.scale)
        frame_rz = cv2.resize(frame[:,:,:3], (resize_width, resize_height))
        return EngineIOData(input_data.frame_id, frame_rz)


class EncoderFactory:
    @staticmethod
    def create_encoder(
        redis_data: dict,
        number_of_processors: int,
        processor_kwargs: dict,
    ):
        processor_type_map = {
            "M001": "Ray_DPIRProcessor",
            "M002": "Ray_DRURBPNSRF3Processor",
            "M003": "Ray_DRURBPNSRF5Processor"
        }
        processor_type = processor_type_map.get(redis_data.get("model"), "Ray_SleepAndPassProcessor")

        if redis_data.get("contentType") == "image":
            logger.debug("image encoder")
            return ImageEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs
            )
        else:
            logger.debug("video encoder")
            # if redis_data.get("model") != "M001":
            #     processor_kwargs = {
            #         "concurrency": 2,
            #         "sleep_time": 0.1,
            #         "scale": 2,
            #     }
            return VideoEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs
            )
        
        logger.debug("encoder init end")
    

@ray.remote(**RAY_ENCODER_ACTOR_OPTIONS)
class RayEncoderFactory:
    def __init__(
        self, 
        redis_data: dict,
        number_of_processors: int,
        processor_kwargs: dict,
    ) -> None:
        import pms_model_manager as mml
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        if redis_data["model"] == "M001":
            processor_type = "Ray_DPIRProcessor"
        elif redis_data["model"] == "M002":
            processor_type = "Ray_DRUASMSRF3Processor" #"Ray_DRURBPNSRF3Processor"
        elif redis_data["model"] == "M003":
            processor_type = "Ray_DRURBPNSRF5Processor"
        else:
            processor_type = "Ray_SleepAndPassProcessor"
            
        model_manager = mml.ModelManager(ROOT_DIR)
        model_key = (
            get_local_processor_type(processor_type)
            if is_wrapped_ray(processor_type)
            else processor_type
        )
        if model_key == "SleepAndPassProcessor":
            processor_kwargs = {
                "sleep_time": 0.1,
                "concurrency": os.getenv("PROCESSOR_CONCURRENCY"),  # concurrency,
            }
        else:
            model_info = MODEL_MAP[model_key]
            model_manager.download(**model_info)
            model_extension = ""
            if model_info["alias"].startswith("onnx"):
                model_extension = "onnx"
            elif model_info["alias"].startswith("trt"):
                model_extension = "plan"
            else:
                raise ValueError(
                    f"""ERROR! model_info["suffix_or_alias"]={model_info["alias"]} is not supported."""
                )
            model_dir = model_manager.get_local_model_dir(model_name=model_info["model_name"], alias=model_info["alias"]) # model_key.replace("Processor", "")
            model_path = os.path.join(model_dir, "model.plan")
            processor_kwargs = {
                "model_path": model_path,
                "concurrency": int(os.getenv("PROCESSOR_CONCURRENCY")),  # concurrency,
            }
        
        logger.debug(f"Processor kwargs : {processor_kwargs}")
        if redis_data["contentType"] == "video":
            self.encoder = VideoEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs
            )
        else:
            self.encoder = ImageEncoder(
                processor_type=processor_type,  # processor_key,
                number_of_processors=number_of_processors,
                processor_kwargs=processor_kwargs
            )
            
        # self.video_encoder = VideoEncoder(
        #     processor_type=processor_type,  # processor_key,
        #     number_of_processors=number_of_processors,
        #     processor_kwargs=processor_kwargs
        # )
        # self.image_encoder = ImageEncoder(
        #     processor_type=processor_type,  # processor_key,
        #     number_of_processors=number_of_processors,
        #     processor_kwargs=processor_kwargs
        # )
    async def run(self, *args, **kwrags) -> None:
        encoder = self.encoder
        await encoder(*args, **kwrags)

    # async def run(self, *args, **kwrags) -> bool:
    #     encoder = self.video_encoder
    #     try:
    #         await encoder(*args, **kwrags)
    #     except Exception as ex:
    #         logger.error(ex)
    #         return False
    #     return True

    # async def run_image(self, *args, **kwrags) -> bool:
    #     encoder = self.image_encoder
    #     try:
    #         await encoder(*args, **kwrags)
    #     except Exception as ex:
    #         logger.error(ex)
    #         return False
    #     return True

