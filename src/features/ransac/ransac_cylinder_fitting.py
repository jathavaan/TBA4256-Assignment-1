import numpy as np
import open3d as o3d
import pyransac3d as pyrsc

from ..cluster import PointCloudDBSCAN
from ...enums import RANSAC


class RANSACCylinderFitting:
    __ransac: pyrsc.Circle
    __point_cloud: o3d.geometry.PointCloud
    __dbscan: 'PointCloudDBSCAN'
    __trees: o3d.geometry.PointCloud

    def __init__(
            self,
            point_cloud: o3d.geometry.PointCloud,
            dbscan: 'PointCloudDBSCAN'
    ) -> None:
        self.ransac = pyrsc.Circle()
        self.point_cloud = point_cloud
        self.dbscan = dbscan
        self.find_circles()

    @property
    def ransac(self) -> pyrsc.Circle:
        return self.__ransac

    @ransac.setter
    def ransac(self, ransac: pyrsc.Circle) -> None:
        self.__ransac = ransac

    @property
    def dbscan(self) -> 'PointCloudDBSCAN':
        return self.__dbscan

    @dbscan.setter
    def dbscan(self, dbscan: 'PointCloudDBSCAN') -> None:
        self.__dbscan = dbscan

    @property
    def point_cloud(self) -> o3d.geometry.PointCloud:
        return self.__point_cloud

    @point_cloud.setter
    def point_cloud(self, point_cloud: o3d.geometry.PointCloud) -> None:
        self.__point_cloud = point_cloud

    @property
    def trees(self) -> o3d.geometry.PointCloud:
        return self.__trees

    @trees.setter
    def trees(self, trees: o3d.geometry.PointCloud) -> None:
        self.__trees = trees

    def find_circles(self) -> None:
        label_indexes: dict[int, np.ndarray] = self.__extract_label_indexes(
            labels=self.dbscan.labels
        )

        labels: list[int] = list(label_indexes.keys())
        label_indexes: list[np.ndarray] = list(label_indexes.values())
        trees: o3d.geometry.PointCloud = o3d.geometry.PointCloud()

        for i in range(len(labels)):
            label: int = labels[i]
            label_index: np.ndarray = label_indexes[i]

            if label == -1 or len(label_index) < RANSAC.CYLINDER_POINT_COUNT_THRESHOLD.value:
                continue

            clustered_point_cloud: o3d.geometry.PointCloud = self.point_cloud.select_by_index(
                indices=label_index
            )

            points: np.ndarray = np.asarray(clustered_point_cloud.points)

            center, axis, radius, inliers = self.ransac.fit(
                pts=np.asarray(clustered_point_cloud.points),
                thresh=RANSAC.DISTANCE_THRESHOLD.value,
                maxIteration=RANSAC.ITERATIONS.value,
            )

            no_points: int = len(points)
            no_inliers: int = len(inliers)
            inlier_ratio: float = no_inliers / no_points

            is_within_radius_interval: bool = RANSAC.MIN_RADIUS.value < radius < RANSAC.MAX_RADIUS.value
            is_within_inlier_ratio_limit: bool = inlier_ratio > RANSAC.INLIER_RATIO_LIMIT.value

            if is_within_radius_interval and is_within_inlier_ratio_limit:
                trees += clustered_point_cloud

            self.trees = trees

    @staticmethod
    def __extract_label_indexes(labels: np.ndarray) -> dict[int, np.ndarray]:
        label_indexes: dict[int, np.ndarray] = {}

        for label in np.unique(labels):
            matching_label_indexes: np.ndarray = np.where(labels == label)[0]
            label_indexes[label] = matching_label_indexes

        return label_indexes
