from enum import Enum

from .. import Config


class PreProcess(Enum):
    VOXEL_SIZE: float = [0.5, 0.15][Config.PARAMETER_SET.value]
    ESTIMATE_NORMALS_RADIUS: float = [0.05, 0.15][Config.PARAMETER_SET.value]
    ESTIMATE_NORMALS_MAX_NN: int = [30, 10][Config.PARAMETER_SET.value]


class DBSCAN(Enum):
    EPS: float = [1.3, 0.37][Config.PARAMETER_SET.value]
    MIN_POINTS: int = [20, 5][Config.PARAMETER_SET.value]
    MIN_POINT_FILTER_COUNT: int = [1000, -1][Config.PARAMETER_SET.value]


class RANSAC(Enum):
    ITERATIONS: int = [1000, 200][Config.PARAMETER_SET.value]
    SAMPLE_SIZE: int = [3, 3][Config.PARAMETER_SET.value]
    DISTANCE_THRESHOLD: float = [0.5, .05][Config.PARAMETER_SET.value]
    RANSAC_ITERATION_LIMIT: int = 75
    PLANE_COLOR: float = [1., .4980, .0549]  # RGB
    STANDARD_DEVIATION_THRESHOLD: float = 14
    INLIER_RATIO_LIMIT: float = [0.07, .30][Config.PARAMETER_SET.value]
    PLANE_POINT_COUNT_THRESHOLD: int = 1000
    CYLINDER_POINT_COUNT_THRESHOLD: int = 0
    MIN_RADIUS: float = .15
    MAX_RADIUS: float = .4


class Slice(Enum):
    NO_SLICES: int = 7
    NO_SKIP_SLICES: int = 4
    SLICE_HEIGHT: float = .30
    SLICE_DISTANCE: float = .30


class BoundingBox(Enum):
    X_THRESH: float = 3.
    Y_THRESH: float = 3.
    Z_THRESH: float = 30.
