from enum import Enum


class PreProcess(Enum):
    VOXEL_SIZE: float = 0.25
    ESTIMATE_NORMALS_RADIUS: float = 0.05
    ESTIMATE_NORMALS_MAX_NN: int = 30


class DBSCAN(Enum):
    EPS: float = 0.46  # [0.4, 0.5]
    MIN_POINTS: int = 10
    MIN_POINT_FILTER_COUNT: int = 1000


class RANSAC(Enum):
    PLANE_FITTING_ITERATION: int = 1000
    SAMPLE_SIZE: int = 3
    DISTANCE_THRESHOLD: float = 0.01
    RANSAC_ITERATION_LIMIT: int = 75
    PLANE_COLOR: list[float] = [0., 0., 1.]  # RGB
    STANDARD_DEVIATION_THRESHOLD: float = 14
    PLANE_INLIER_RATIO_LIMIT: float = 0.15
