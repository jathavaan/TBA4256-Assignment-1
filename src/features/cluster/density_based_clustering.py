from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np
import open3d as o3d

from ...enums import DBSCAN as DBSCANparameters
from ...utils import Utillities


class DensityBasedClustering:
    __dbscan_object: DBSCAN = None
    __labels: np.ndarray = None

    def __init__(self) -> None:
        self.dbscan_object = DBSCAN(
            eps=DBSCANparameters.EPS.value,
            min_samples=DBSCANparameters.MIN_POINTS.value,
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

    def cluster(self, point_cloud: o3d.geometry.PointCloud) -> None:
        XYZ: np.ndarray = Utillities.point_cloud_extract_XYZ_and_RGB(
            point_cloud=point_cloud
        )[0]

        X: pd.DataFrame = pd.DataFrame(XYZ, columns=["X", "Y", "Z"])

        print(X)

        # dbscan: DBSCAN = self.dbscan_object
        # labels: np.ndarray = dbscan.fit_predict(X=X)

        # cluster_count: int = np.unique(labels).size
