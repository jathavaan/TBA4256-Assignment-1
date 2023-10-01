from matplotlib.figure import Figure, Axes
import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np

from ...utils import Utillities


class Plot:
    @staticmethod
    def point_cloud(point_cloud: o3d.geometry.PointCloud) -> None:
        XYZ, RGB = Utillities.point_cloud_extract_XYZ_and_RGB(
            point_cloud=point_cloud
        )  # Datatype is np.ndarray

        X: np.ndarray = XYZ[:, 0]
        Y: np.ndarray = XYZ[:, 1]
        Z: np.ndarray = XYZ[:, 2]

        figure: Figure = plt.figure()
        axes: Axes = figure.add_subplot(projection="3d")

        axes.scatter(X, Y, Z, c=RGB)

        axes.set_xlabel("X")
        axes.set_ylabel("Y")
        axes.set_zlabel("Z")

        plt.show()
