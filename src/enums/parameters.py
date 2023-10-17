from enum import Enum


class PreProcess(Enum):
    VOXEL_SIZE: float = 0.5
    ESTIMATE_NORMALS_RADIUS: float = 0.05
    ESTIMATE_NORMALS_MAX_NN: int = 30


class DBSCAN(Enum):
    EPS: float = 1.3  # [0.4, 0.5]
    MIN_POINTS: int = 20
    MIN_POINT_FILTER_COUNT: int = 1000


class RANSAC(Enum):
    PLANE_FITTING_ITERATION: int = 1000
    SAMPLE_SIZE: int = 3
    DISTANCE_THRESHOLD: float = 0.5
    RANSAC_ITERATION_LIMIT: int = 75
    PLANE_COLOR: list[float] = [1., .4980, .0549]  # RGB
    STANDARD_DEVIATION_THRESHOLD: float = 14
    PLANE_INLIER_RATIO_LIMIT: float = 0.07
    PLANE_POINT_COUNT_THRESHOLD: int = 1000
