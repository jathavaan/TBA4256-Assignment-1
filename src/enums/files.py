from enum import Enum


class Files(Enum):
    RAW_POINT_CLOUD = 'raw_point_cloud.laz'
    OFF_GROUND_POINTS = 'off_ground_points.las'
    GROUND_POINTS = 'ground_points.las'
