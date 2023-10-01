import open3d as o3d


class Visualize:
    @staticmethod
    def display(point_cloud: o3d.geometry.PointCloud) -> None:
        o3d.visualization.draw_geometries([point_cloud])
