from typing import Tuple

import numpy as np
import open3d as o3d
import pandas as pd
from numpy import ndarray


class Utilities:
    @staticmethod
    def point_cloud_extract_XYZ_and_RGB(
            point_cloud: o3d.geometry.PointCloud
    ) -> tuple[ndarray, ndarray]:
        XYZ: np.ndarray = np.asarray(point_cloud.points)
        RGB: np.ndarray = np.asarray(point_cloud.colors)

        return XYZ, RGB

    @staticmethod
    def dataframe_extract_XYZ_and_RGB(
            dataframe: pd.DataFrame
    ) -> tuple[ndarray, ndarray]:
        XYZ: np.ndarray = np.array(
            dataframe[["X", "Y", "Z"]],
        )

        RGB: np.ndarray = np.array(
            dataframe[["R", "G", "B"]],
        )

        return XYZ, RGB
