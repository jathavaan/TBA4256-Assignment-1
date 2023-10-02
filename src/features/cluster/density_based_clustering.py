import numpy as np
import open3d as o3d
import pandas as pd
from sklearn.cluster import DBSCAN

from ...enums import DBSCAN as DBScanParameters
from ...enums import PreProcess
from ...utils import Conversion, Utillities
from ..display import Visualize


class DensityBasedClustering:
    __dbscan_object: DBSCAN = None
    __labels: np.ndarray = None
    __labeled_points: pd.DataFrame = pd.DataFrame(
        columns=["X", "Y", "Z", "R", "G", "B", "label"]
    )

    def __init__(self) -> None:
        self.dbscan_object = DBSCAN(
            eps=DBScanParameters.EPS.value,
            min_samples=DBScanParameters.MIN_POINTS.value,
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

    def cluster(self, point_cloud: o3d.geometry.PointCloud) -> None:
        XYZ, RGB = Utillities.point_cloud_extract_XYZ_and_RGB(
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

    def view_clusters(self) -> None:
        labeled_dataframe: pd.DataFrame = self.labeled_points
        labels: np.ndarray = self.labels

        for label in labels:
            filtered_dataframe: pd.DataFrame = labeled_dataframe[
                labeled_dataframe["label"] == label
            ].drop(columns=["label"])

            point_cloud: o3d.geometry.PointCloud = Conversion.dataframe_to_point_cloud(
                filtered_dataframe
            )

            Visualize.display(point_cloud=point_cloud)
