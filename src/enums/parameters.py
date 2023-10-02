from enum import Enum


class PreProcess(Enum):
    VOXEL_SIZE: float = 0.1
    ESTIMATE_NORMALS_RADIUS: float = 0.1
    ESTIMATE_NORMALS_MAX_NN: int = 30


class DBSCAN(Enum):
    EPS: float = 0.25
    MIN_POINTS: int = 30


class RANSAC(Enum):
    PLANE_FITTING_ITERATION: int = 1000
    SAMPLE_SIZE: int = 3
    DISTANCE_THRESHOLD: float = 0.01
    RANSAC_ITERATION_LIMIT: int = 1000
