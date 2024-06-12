import time
import json
from loguru import logger

def check_progress(
    file_key: str,
    n_frame: int,
    t_frames: int,
    t1: float,
    t2: float,
) -> str:
    t3 = t2 - t1
    progress = int((n_frame / t_frames) * 100)
    time = int(t3 * (t_frames - n_frame) / n_frame)
    logger.debug(f"{file_key} progress {progress} time {time}")
    return json.dumps(
        {"progress": "{}".format(progress), "time": "{}".format(time)}
    )