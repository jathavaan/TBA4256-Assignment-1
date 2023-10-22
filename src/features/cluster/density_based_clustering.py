import numpy as np
import open3d as o3d
import pandas as pd
from sklearn.cluster import DBSCAN

from ...enums import DBSCAN as DBScanParameters
from ...enums import PreProcess
from ...utils import Conversion, Utilities
from ..display import Visualize


class DensityBasedClustering:
    __dbscan_object: DBSCAN = None
    __labels: np.ndarray = None
    __labeled_points: pd.DataFrame = None
    __clustered_point_clouds: list[o3d.geometry.PointCloud] = None

    def __init__(self) -> None:
        self.dbscan_object = DBSCAN(
            eps=DBScanParameters.EPS.value,
            min_samples=DBScanParameters.MIN_POINTS.value,
        )

        self.clustered_point_clouds = []
        self.labels = np.array([])

        self.labeled_points = pd.DataFrame(
            columns=["X", "Y", "Z", "R", "G", "B", "label"]
        )

    @property
    def dbscan_object(self) -> DBSCAN:
        return self.__dbscan_object

    @dbscan_object.setter
    def dbscan_object(self, dbscan_object: DBSCAN) -> None:
        self.__dbscan_object = dbscan_object

    @property
    def labels(self) -> np.ndarray:
        return self.__labels

    @labels.setter
    def labels(self, labels: np.ndarray) -> None:
        self.__labels = labels

    @property
    def labeled_points(self) -> pd.DataFrame:
        return self.__labeled_points

    @labeled_points.setter
    def labeled_points(self, labeled_point_cloud: pd.DataFrame) -> None:
        self.__labeled_points = labeled_point_cloud

    @property
    def clustered_point_clouds(self) -> list[o3d.geometry.PointCloud]:
        return self.__clustered_point_clouds

    @clustered_point_clouds.setter
    def clustered_point_clouds(self, clustered_point_clouds: list[o3d.geometry.PointCloud]) -> None:
        self.__clustered_point_clouds = clustered_point_clouds

    def add_clustered_point_cloud(
        self,
        clustered_point_cloud: o3d.geometry.PointCloud
    ) -> None:
        self.clustered_point_clouds.append(clustered_point_cloud)

    def cluster(self, point_cloud: o3d.geometry.PointCloud) -> None:
        XYZ, RGB = Utilities.point_cloud_extract_XYZ_and_RGB(
            point_cloud
        )

        self.dbscan_object.fit(XYZ)
        self.labels: pd.DataFrame = np.array(self.dbscan_object.labels_)

        print(f"Number of clusters found: {len(np.unique(self.labels))}")

        labeled_dataframe: pd.DataFrame = pd.DataFrame(
            columns=["X", "Y", "Z", "R", "G", "B", "label"],
        )

        X: np.ndarray = XYZ[:, 0]
        Y: np.ndarray = XYZ[:, 1]
        Z: np.ndarray = XYZ[:, 2]

        R: np.ndarray = RGB[:, 0]
        G: np.ndarray = RGB[:, 1]
        B: np.ndarray = RGB[:, 2]

        labeled_dataframe["X"] = X
        labeled_dataframe["Y"] = Y
        labeled_dataframe["Z"] = Z

        labeled_dataframe["R"] = R
        labeled_dataframe["G"] = G
        labeled_dataframe["B"] = B

        labeled_dataframe["label"] = self.labels
        self.labeled_points = labeled_dataframe

    def create_clustered_point_clouds(self) -> o3d.geometry.PointCloud:
        for dataframe in self.__label_based_segmentation():
            clustered_point_cloud: o3d.geometry.PointCloud = Conversion.dataframe_to_point_cloud(
                dataframe=dataframe
            )

            self.add_clustered_point_cloud(
                clustered_point_cloud=clustered_point_cloud
            )

    def view_clusters(self) -> None:
        for clustered_point_cloud in self.clustered_point_clouds:
            Visualize.display(clustered_point_cloud)

    def __label_based_segmentation(self) -> list[pd.DataFrame]:
        dataframe: pd.DataFrame = self.labeled_points
        labels: np.ndarray = self.labels
        segmented_dataframes: list[pd.DataFrame] = []

        for label in labels:
            segmented_dataframes.append(
                dataframe[dataframe["label"] == label].drop(columns=["label"])
            )

        return segmented_dataframes
