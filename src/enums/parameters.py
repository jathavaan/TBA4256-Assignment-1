from enum import Enum


class PreProcess(Enum):
    VOXEL_SIZE: float = 0.1


class DBSCAN(Enum):
    EPS: float = 0.05
    MIN_POINTS: int = 10


class RANSAC(Enum):
    pass
