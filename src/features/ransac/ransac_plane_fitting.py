import math

import numpy as np
import open3d as o3d
from tqdm import tqdm

from ...enums import DBSCAN
from ...enums import RANSAC as RANSACParameter
from ...utils import Timer
from ..cluster import PointCloudDBSCAN
from ..display import Visualize


class RANSACPlaneFitting:
    __point_cloud: o3d.geometry.PointCloud = None
    __dbscan: 'PointCloudDBSCAN' = None
    __roof_point_cloud: o3d.geometry.PointCloud = None
    __non_roof_point_cloud: o3d.geometry.PointCloud = None

    def __init__(
        self,
        point_cloud: o3d.geometry.PointCloud,
        dbscan: 'PointCloudDBSCAN'
    ) -> None:
        self.point_cloud = point_cloud
        self.dbscan = dbscan

    @property
    def point_cloud(self) -> o3d.geometry.PointCloud:
        return self.__point_cloud

    @point_cloud.setter
    def point_cloud(self, point_cloud: o3d.geometry.PointCloud) -> None:
        self.__point_cloud = point_cloud

    @property
    def dbscan(self) -> 'PointCloudDBSCAN':
        return self.__dbscan

    @dbscan.setter
    def dbscan(self, dbscan: 'PointCloudDBSCAN') -> None:
        self.__dbscan = dbscan

    @property
    def roof_point_cloud(self) -> o3d.geometry.PointCloud:
        return self.__roof_point_cloud

    @roof_point_cloud.setter
    def roof_point_cloud(self, roof_point_cloud: o3d.geometry.PointCloud) -> None:
        self.__roof_point_cloud = roof_point_cloud

    @property
    def non_roof_point_cloud(self) -> o3d.geometry.PointCloud:
        return self.__non_roof_point_cloud

    @non_roof_point_cloud.setter
    def non_roof_point_cloud(self, non_roof_point_cloud: o3d.geometry.PointCloud) -> None:
        self.__non_roof_point_cloud = non_roof_point_cloud

    def find_planes(
        self,
        point_cloud: o3d.geometry.PointCloud
    ) -> list[int]:
        inliers: list[int] = []
        point_cloud_size: int = len(point_cloud.points)

        if point_cloud_size < RANSACParameter.SAMPLE_SIZE.value:
            return inliers

        max_inlier_ratio: float = 0.0
        for _ in range(RANSACParameter.RANSAC_ITERATION_LIMIT.value):
            distance_function, ransac_inliers = RANSACPlaneFitting.__ransac_plane_fitting(
                point_cloud=point_cloud
            )

            # outlier_point_cloud = point_cloud.select_by_index(
            #     inliers,
            #     invert=True
            # )

            inlier_ratio: float = len(ransac_inliers) / point_cloud_size
            if inlier_ratio > max_inlier_ratio:
                max_inlier_ratio = inlier_ratio

            if inlier_ratio > RANSACParameter.PLANE_INLIER_RATIO_LIMIT.value:
                for index in ransac_inliers:
                    inliers.append(index)

                # Visualize.display(point_cloud.select_by_index(inliers))

            continue

            outlier_points: np.ndarray = np.asarray(outlier_point_cloud.points)
            x: np.ndarray = outlier_points[:, 0]
            y: np.ndarray = outlier_points[:, 1]
            z: np.ndarray = outlier_points[:, 2]

            distances: np.ndarray = distance_function(x, y, z)

            if distances.std() < RANSACParameter.STANDARD_DEVIATION_THRESHOLD.value:
                for index in ransac_inliers:
                    inliers.append(index)

        return inliers

    def run(self) -> None:
        print(
            f"""Running RANSAC Plane Fitting with the following parameters:
            - Plane Fitting Iteration: {RANSACParameter.PLANE_FITTING_ITERATION.value}
            - Sample Size: {RANSACParameter.SAMPLE_SIZE.value}
            - Distance Threshold: {RANSACParameter.DISTANCE_THRESHOLD.value}
            - RANSAC Iteration Limit: {RANSACParameter.RANSAC_ITERATION_LIMIT.value}
            - Standard Deviation Threshold: {RANSACParameter.STANDARD_DEVIATION_THRESHOLD.value}
            - Plane Inlier Ratio Limit: {RANSACParameter.PLANE_INLIER_RATIO_LIMIT.value}
            """
        )
        label_indexes: dict[int, np.ndarray] = self.__extract_label_indexes(
            self.dbscan.labels
        )

        roof_indexes: list[int] = []

        labels: list[int] = list(label_indexes.keys())
        label_indexes: list[np.ndarray] = list(label_indexes.values())

        for i in tqdm(
            range(len(labels)),
            desc="RANSAC Plane Fitting for clusters",
            unit="cluster"
        ):
            label: int = labels[i]
            indexes: np.ndarray = label_indexes[i]

            if label == -1:
                continue

            clustered_point_cloud: o3d.geometry.PointCloud = self.point_cloud.select_by_index(
                indexes
            )

            inliers_indexes: list[int] = self.find_planes(
                point_cloud=clustered_point_cloud
            )

            for index in inliers_indexes:
                roof_indexes.append(index)

        roof_indexes: np.ndarray = np.unique(np.asarray(roof_indexes))
        ratio: float = len(roof_indexes) / len(self.point_cloud.points)
        print(
            f"Roof point cloud has {ratio * 100}% of the original point cloud"
        )

        roof_pcd: o3d.geometry.PointCloud = self.point_cloud.select_by_index(
            roof_indexes
        )

        roof_pcd.paint_uniform_color(RANSACParameter.PLANE_COLOR.value)

        non_roof_pcd: o3d.geometry.PointCloud = self.point_cloud.select_by_index(
            roof_indexes,
            invert=True
        )

        self.roof_point_cloud = roof_pcd
        self.non_roof_point_cloud = non_roof_pcd

    @staticmethod
    def __extract_label_indexes(labels: np.ndarray) -> dict[int, np.ndarray]:
        label_indexes: dict[int, np.ndarray] = {}

        for label in np.unique(labels):
            matching_label_indexes: np.ndarray = np.where(labels == label)[0]
            label_indexes[label] = matching_label_indexes

        return label_indexes

    @staticmethod
    def __ransac_plane_fitting(
        point_cloud: o3d.geometry.PointCloud
    ) -> tuple['function', np.ndarray]:
        plane_model, inliers = point_cloud.segment_plane(
            distance_threshold=RANSACParameter.DISTANCE_THRESHOLD.value,
            ransac_n=RANSACParameter.SAMPLE_SIZE.value,
            num_iterations=RANSACParameter.PLANE_FITTING_ITERATION.value
        )

        a: float = plane_model[0]
        b: float = plane_model[1]
        c: float = plane_model[2]
        d: float = plane_model[3]

        distance_function = RANSACPlaneFitting.__point_plane_distance_function(
            a=a,
            b=b,
            c=c,
            d=d
        )

        return distance_function, inliers

    @staticmethod
    def __point_plane_distance_function(
        a: float,
        b: float,
        c: float,
        d: float
    ) -> 'function':
        return lambda x, y, z: np.divide(
            np.abs(a * x + b * y + c * z + d),
            np.sqrt(math.pow(a, 2) + math.pow(b, 2) + math.pow(c, 2))
        )
