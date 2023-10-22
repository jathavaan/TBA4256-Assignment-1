from enum import Enum

from .. import Config


class PreProcess(Enum):
    VOXEL_SIZE: float = [0.5, 0.05][Config.PARAMETER_SET.value]
    ESTIMATE_NORMALS_RADIUS: float = [0.05, 0.05][Config.PARAMETER_SET.value]
    ESTIMATE_NORMALS_MAX_NN: int = [30, 10][Config.PARAMETER_SET.value]


class DBSCAN(Enum):
    EPS: float = [1.3, 2.][Config.PARAMETER_SET.value]
    MIN_POINTS: int = [20, 20][Config.PARAMETER_SET.value]
    MIN_POINT_FILTER_COUNT: int = [1000, 1000][Config.PARAMETER_SET.value]


class RANSAC(Enum):
    PLANE_FITTING_ITERATION: int = [1000, 10000][Config.PARAMETER_SET.value]
    SAMPLE_SIZE: int = [3, 3][Config.PARAMETER_SET.value]
    DISTANCE_THRESHOLD: float = [0.5, 0.5][Config.PARAMETER_SET.value]
    RANSAC_ITERATION_LIMIT: int = 75
    PLANE_COLOR: float = [1., .4980, .0549]  # RGB
    STANDARD_DEVIATION_THRESHOLD: float = 14
    PLANE_INLIER_RATIO_LIMIT: float = 0.07
    PLANE_POINT_COUNT_THRESHOLD: int = 1000


class Slice(Enum):
    NO_SLICES: int = 3
    SLICE_HEIGHT: float = 0.05
    SLICE_DISTANCE: float = 0.01
