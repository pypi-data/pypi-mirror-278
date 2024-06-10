import numpy as np
import cv2
import requests
from queue import Queue
from collections import deque
from loguru import logger
from pms_inference_engine.data_struct import EngineIOData

class ImageQueueObjectGenerator:
    def __init__(
        self,
        redis_data: dict,
    ):
        self.redis_data = redis_data
        
    def make_queue_object(
        self,
        frame_id: int,
        image_data: dict,
        frame_map: dict,
        enqueue: Queue
    ) -> None:
        if self.redis_data.get("model") == "M001":
            self._generate_enhance_object(
                frame_id,
                image_data,
                frame_map,
                enqueue
            )
        elif self.redis_data.get("model") == "M002":
            self._generate_sr1_object(
                frame_id,
                image_data,
                frame_map,
                enqueue
            )
        elif self.redis_data.get("model") == "M003":
            self._generate_sr2_object(
                frame_id,
                image_data,
                frame_map,
                enqueue
            )
        else:
            raise "invalid model"
        
    def _generate_enhance_object(
        self,
        frame_id: int,
        image_data: dict,
        frame_map: dict,
        enqueue: Queue
    ) -> None:
        if self.redis_data["combined"] == "N":
            file_path = self.redis_data["filePath"]
        else:
            file_path = (
                self.redis_data["filePath"]
                + image_data["file_key"]
                + "."
                + image_data["file_type"]
            )
        frame_map[str(frame_id)] = {
            "file_name": image_data["file_name"],
            "file_key": image_data["file_key"],
            "combined_file_key": image_data["combined_file_key"],
            "file_type": image_data["file_type"]
        }
        frame = self._read_frame(file_path)
        tmp = EngineIOData(frame_id=frame_id, frame=frame)
        enqueue.put(tmp)
        logger.debug(f"Enqueue {frame_map[str(frame_id)]}")
    
       
    def _generate_sr1_object(
        self,
        frame_id: int,
        image_data: dict,
        frame_map: dict,
        enqueue: Queue
    ) -> None:
        if self.redis_data["combined"] == "N":
            file_path = self.redis_data["filePath"]
        else:
            file_path = (
                self.redis_data["filePath"]
                + image_data["file_key"]
                + "."
                + image_data["file_type"]
            )
        frame_map[str(frame_id)] = {
            "file_name": image_data["file_name"],
            "file_key": image_data["file_key"],
            "combined_file_key": image_data["combined_file_key"],
            "file_type": image_data["file_type"]
        }
        frame = self._read_frame(file_path)
        input_frame = input_frame = np.concatenate(
            [frame] * 3, axis=-1
        )
        tmp = EngineIOData(frame_id=frame_id, frame=input_frame)
        enqueue.put(tmp)
        logger.debug(f"Enqueue {frame_map[str(frame_id)]}")
        
    def _generate_sr2_object(
        self,
        frame_id: int,
        image_data: dict,
        frame_map: dict,
        enqueue: Queue
    ) -> None:
        if self.redis_data["combined"] == "N":
            file_path = self.redis_data["filePath"]
        else:
            file_path = (
                self.redis_data["filePath"]
                + image_data["file_key"]
                + "."
                + image_data["file_type"]
            )
        frame_map[str(frame_id)] = {
            "file_name": image_data["file_name"],
            "file_key": image_data["file_key"],
            "combined_file_key": image_data["combined_file_key"],
            "file_type": image_data["file_type"]
        }
        frame = self._read_frame(file_path)
        input_frame = input_frame = np.concatenate(
            [frame] * 5, axis=-1
        )
        tmp = EngineIOData(frame_id=frame_id, frame=input_frame)
        enqueue.put(tmp)
        logger.debug(f"Enqueue {frame_map[str(frame_id)]}")
        
    
    def _read_frame(self, path):
        # image_np = cv2.imread(path, cv2.IMREAD_COLOR)
        #
        # if image_np is not None:
        #     image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        #     print(image_np)
        #     return image_np
        # else:
        #     raise FileNotFoundError("The specified image file could not be loaded: {}".format(path))
        response = requests.get(path)
        if response.status_code == 200:
            # image = Image.open(BytesIO(response.content))
            # image_np = np.array(image)
            image = np.fromstring(response.content, dtype=np.uint8)
            image_np = cv2.imdecode(image, cv2.IMREAD_COLOR)
            image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            return image_np
        else:
            raise Exception("Error: Image Download Fail")
        