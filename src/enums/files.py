from enum import Enum


class Files(Enum):
    RAW_POINT_CLOUD = 'raw_point_cloud.laz'
    UNPROCESSED_OFF_GROUND_POINTS = 'unprocessed_off_ground_points.las'
    OFF_GROUND_POINTS = 'off_ground_points.las'
    GROUND_POINTS = 'ground_points.las'
    TREE_POINT_CLOUD: str = 'tree_point_cloud.las'
    TREE_POINT_CLOUD_STRICT_SOR: str = 'tree_point_cloud_strict_sor.las'
