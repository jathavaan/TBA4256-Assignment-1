from collections import Counter

import numpy as np
import open3d as o3d
import pandas as pd

from ...enums import DBSCAN
from ...utils import Utilities


class PointCloudDBSCAN:
    __labels: np.ndarray = None
    __point_cloud: o3d.geometry.PointCloud = None
    __labled_dataframe: pd.DataFrame = None
    eps: float
    min_points: int

    def __init__(
            self,
            point_cloud: o3d.geometry.PointCloud,
            eps: float = DBSCAN.EPS.value,
            min_points: int = DBSCAN.MIN_POINTS.value
    ) -> None:
        self.labels = np.array([])
        self.point_cloud = point_cloud
        self.labeled_dataframe = pd.DataFrame(
            columns=["X", "Y", "Z", "R", "G", "B", "label"]
        )
        self.eps = eps
        self.min_points = min_points

    @property
    def labels(self) -> np.ndarray:
        return self.__labels

    @labels.setter
    def labels(self, labels: np.ndarray) -> None:
        self.__labels = labels

    @property
    def point_cloud(self) -> o3d.geometry.PointCloud:
        return self.__point_cloud

    @point_cloud.setter
    def point_cloud(self, point_cloud: o3d.geometry.PointCloud) -> None:
        self.__point_cloud = point_cloud

    @property
    def labeled_dataframe(self) -> pd.DataFrame:
        return self.__labeled_dataframe

    @labeled_dataframe.setter
    def labeled_dataframe(self, labeled_dataframe: pd.DataFrame) -> None:
        self.__labeled_dataframe = labeled_dataframe

    def cluster(self) -> None:
        self.labels = np.array(self.point_cloud.cluster_dbscan(
            eps=self.eps,
            min_points=self.min_points
        ))

        label_counts: 'Counter' = Counter(self.labels)

        for label, count in label_counts.items():
            if count < DBSCAN.MIN_POINT_FILTER_COUNT.value:
                self.labels[self.labels == label] = -1

        cluster_count: int = np.unique(self.labels).size
        print(f"Point cloud has {cluster_count} clusters")

        self.__label_dataframe()

    def __label_dataframe(self) -> None:
        XYZ, RGB = Utilities.point_cloud_extract_XYZ_and_RGB(
            point_cloud=self.point_cloud
        )

        X: np.ndarray = XYZ[:, 0]
        Y: np.ndarray = XYZ[:, 1]
        Z: np.ndarray = XYZ[:, 2]

        R: np.ndarray = RGB[:, 0]
        G: np.ndarray = RGB[:, 1]
        B: np.ndarray = RGB[:, 2]

        self.labeled_dataframe["X"] = X
        self.labeled_dataframe["Y"] = Y
        self.labeled_dataframe["Z"] = Z

        self.labeled_dataframe["R"] = R
        self.labeled_dataframe["G"] = G
        self.labeled_dataframe["B"] = B

        self.labeled_dataframe["label"] = self.labels
