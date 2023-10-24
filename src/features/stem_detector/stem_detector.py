import numpy as np
import open3d as o3d

from ..cluster import PointCloudDBSCAN
from ...enums import BoundingBox


class StemDetector:
    trees: o3d.geometry.PointCloud
    dbscan: 'PointCloudDBSCAN'
    stems: list[o3d.geometry.AxisAlignedBoundingBox]

    def __init__(self, trees: o3d.geometry.PointCloud, dbscan: 'PointCloudDBSCAN') -> None:
        self.trees = trees
        self.dbscan = dbscan
        self.find_stems()

    def find_stems(self) -> None:
        label_indexes: dict[int, np.ndarray] = StemDetector.__extract_label_indexes(
            labels=self.dbscan.labels
        )

        indexes: list[np.ndarray] = list(label_indexes.values())
        bounding_boxes: list[o3d.geometry.AxisAlignedBoundingBox] = []

        for idxs in indexes:
            clustered_point_cloud: o3d.geometry.PointCloud = self.trees.select_by_index(idxs)
            bounding_box: o3d.geometry.AxisAlignedBoundingBox = clustered_point_cloud.get_axis_aligned_bounding_box()
            bounding_boxes.append(bounding_box)

        stems: list[o3d.geometry.AxisAlignedBoundingBox] = []
        for bounding_box in bounding_boxes:
            min_point: np.ndarray = bounding_box.get_min_bound()
            max_point: np.ndarray = bounding_box.get_max_bound()

            min_X: float = min_point[0] - BoundingBox.X_THRESH.value
            min_Y: float = min_point[1] - BoundingBox.Y_THRESH.value
            min_Z: float = min_point[2] - BoundingBox.Z_THRESH.value

            max_X: float = max_point[0] + BoundingBox.X_THRESH.value
            max_Y: float = max_point[1] + BoundingBox.Y_THRESH.value
            max_Z: float = max_point[2] + BoundingBox.Z_THRESH.value

            lower_bound: np.ndarray = np.array([min_X, min_Y, min_Z])
            upper_bound: np.ndarray = np.array([max_X, max_Y, max_Z])

            stem: o3d.geometry.AxisAlignedBoundingBox = o3d.geometry.AxisAlignedBoundingBox(
                min_bound=lower_bound,
                max_bound=upper_bound
            )

            stem.color = (1, 0, 0)
            stems.append(stem)

        self.stems = stems

    @staticmethod
    def __extract_label_indexes(labels: np.ndarray) -> dict[int, np.ndarray]:
        label_indexes: dict[int, np.ndarray] = {}

        for label in np.unique(labels):
            matching_label_indexes: np.ndarray = np.where(labels == label)[0]
            label_indexes[label] = matching_label_indexes

        return label_indexes
