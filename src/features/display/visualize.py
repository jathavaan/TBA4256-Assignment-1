import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d

from ... import Config


class Visualize:
    @staticmethod
    def display(*point_clouds: o3d.geometry.PointCloud) -> None:
        point_count: int = sum(len(pcd.points) for pcd in point_clouds if isinstance(pcd, o3d.geometry.PointCloud))
        window_name: str = f"Point Cloud with {point_count} points"

        o3d.visualization.draw_geometries(
            [*point_clouds],
            window_name=window_name
        )

    @staticmethod
    def display_colored_clusters(
        point_cloud: o3d.geometry.PointCloud,
        labels: np.ndarray
    ) -> None:
        copy_point_cloud: o3d.geometry.PointCloud = point_cloud
        max_label: int = labels.max()

        colors = plt.get_cmap(Config.COLOR_MAP.value)(
            labels / (max_label if max_label > 0 else 1)
        )
        colors[labels < 0] = 0

        copy_point_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
        Visualize.display(copy_point_cloud)
