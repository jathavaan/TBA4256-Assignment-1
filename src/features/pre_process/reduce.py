import numpy as np
import open3d as o3d

from ...enums import PreProcess


class Reduce:
    @staticmethod
    def voxel_downsample(
            point_cloud: o3d.geometry.PointCloud,
            voxel_size: float = PreProcess.VOXEL_SIZE.value
    ) -> o3d.geometry.PointCloud:
        downsampled_point_cloud: o3d.geometry.PointCloud = point_cloud.voxel_down_sample(
            voxel_size=voxel_size
        )

        original_point_count: int = len(point_cloud.points)
        downsampled_point_count: int = len(downsampled_point_cloud.points)
        point_count_difference: int = original_point_count - downsampled_point_count

        print(
            f"Original point count: {original_point_count}\n"
            f"Downsampled point count: {downsampled_point_count}\n"
            f"Point cloud size reduced with "
            f"{round(np.divide(point_count_difference, original_point_count) * 100, 2)}%"
        )

        return downsampled_point_cloud

    @staticmethod
    def statistical_outlier_removal(
            point_cloud: o3d.geometry.PointCloud,
            nb_neighbors: int = 20,
            std_ratio: float = .1
    ) -> o3d.geometry.PointCloud:
        point_cloud, _ = point_cloud.remove_statistical_outlier(
            nb_neighbors=nb_neighbors,
            std_ratio=std_ratio
        )
        return point_cloud

