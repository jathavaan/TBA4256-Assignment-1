import numpy as np
import open3d as o3d


class Utillities:
    @staticmethod
    def point_cloud_extract_XYZ_and_RGB(
        point_cloud: o3d.geometry.PointCloud
    ) -> tuple[np.ndarray, np.ndarray]:
        XYZ: np.ndarray = np.asarray(point_cloud.points)
        RGB: np.ndarray = np.asarray(point_cloud.colors)

        return XYZ, RGB
