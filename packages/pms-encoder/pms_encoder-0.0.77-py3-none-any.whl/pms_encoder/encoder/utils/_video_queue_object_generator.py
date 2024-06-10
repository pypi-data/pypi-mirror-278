import subprocess
import numpy as np
from queue import Queue
from collections import deque
from loguru import logger
from pms_inference_engine.data_struct import EngineIOData

class VideoQueueObjectGenerator:
    def __init__(
        self,
        process: subprocess.Popen,
        redis_data: dict,
        meta_data: dict,
    ):
        self.process = process
        self.redis_data = redis_data
        self.meta_data = meta_data
        self.sr01_queue = deque(maxlen=3)
        self.sr02_queue = deque(maxlen=5)
        
    def make_queue_object(
        self,
        frame_id: int,
        enqueue: Queue
    ) -> bool:
        if self.redis_data.get("model") == "M001":
            return self._generate_enhance_object(
                frame_id,
                enqueue
            )
        elif self.redis_data.get("model") == "M002":
            return self._generate_sr1_object(
                frame_id,
                enqueue
            )
        elif self.redis_data.get("model") == "M003":
            return self._generate_sr2_object(
                frame_id,
                enqueue
            )
        else:
            return self._generate_enhance_object(
                frame_id,
                enqueue
            )
            # raise "invalid model"
        
    def _generate_enhance_object(
        self,
        frame_id: int,
        enqueue: Queue
    ) -> bool:
        frame = self._read_frame()
        
        if frame is None:
            # end of frames
            logger.debug(">>> Frame is None")
            return False
        
        enqueue.put(
            EngineIOData(frame_id=frame_id, frame=frame)
        )
        return True
    
    def _generate_sr1_object(
        self,
        frame_id: int,
        enqueue: Queue
    ) -> bool:
        frame = self._read_frame()
        if frame is None:
            # end of frames
            logger.debug(">>> Frame is None")
            return False
        
        if frame_id == 1:
            for _ in range(0,2):
                self.sr01_queue.append(frame)
        
        if frame_id > 2:
            self.sr01_queue.popleft()
        
        self.sr01_queue.append(frame)
        
        # 1 1 2
        if len(self.sr01_queue) == 3:
            input_frame = np.concatenate(
                [image for image in self.sr01_queue], axis=-1
            )
            input_io_data = EngineIOData(frame_id=frame_id-1, frame=input_frame)
            enqueue.put(input_io_data)
        
        if frame_id == self.meta_data["nb_frames"]:
            for i in range(1, 2):
                self.sr01_queue.popleft()
                self.sr01_queue.append(frame)
                
                input_frame = np.concatenate(
                    [image for image in self.sr01_queue], axis=-1
                )
                input_io_data = EngineIOData(frame_id=frame_id-1+i, frame=input_frame)
                enqueue.put(input_io_data)
        
        return True

    def _generate_sr2_object(
        self,
        frame_id: int,
        enqueue: Queue
    ) -> bool:
        frame = self._read_frame()
        if frame is None:
            # end of frames
            logger.debug(">>> Frame is None")
            return False
        
        if frame_id == 1:
            for _ in range(0,3):
                self.sr02_queue.append(frame)
        
        if frame_id > 3:
            self.sr02_queue.popleft()
        
        self.sr02_queue.append(frame)
        
        # 1 1 1 1 2 3 4 -> 1 1 1 2 3
        if len(self.sr02_queue) == 5:
            input_frame = np.concatenate(
                [image for image in self.sr02_queue], axis=-1
            )
            input_io_data = EngineIOData(frame_id=frame_id-2, frame=input_frame)
            enqueue.put(input_io_data)
        
        if frame_id == self.meta_data["nb_frames"]:
            for i in range(1, 3):
                self.sr02_queue.popleft()
                self.sr02_queue.append(frame)
                
                input_frame = np.concatenate(
                    [image for image in self.sr02_queue], axis=-1
                )
                input_io_data = EngineIOData(frame_id=frame_id-2+i, frame=input_frame)
                enqueue.put(input_io_data)
        
        return True

    def _read_frame(
        self,
    ):
        in_bytes = self.process.stdout.read(self.meta_data["width"] * self.meta_data["height"] * 3)
        if not in_bytes:
            return None
        in_frame = np.frombuffer(in_bytes, np.uint8).reshape([self.meta_data["height"], self.meta_data["width"], 3])
        return in_frame

    
    

    