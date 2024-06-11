from typing import Union
import numpy as np
from dataclasses import dataclass, field
from .common import create_uuid


@dataclass
class EngineIOData:
    frame_id: int
    frame: Union[np.ndarray, None]
    uuid: str = field(default_factory=lambda: create_uuid())
