import open3d as o3d

from src.enums import Files
from src.features.point_cloud_handler import Handler
from src.features.display import Visualize
from src.features.pre_process import Reduce


class Main:
    @staticmethod
    def run() -> None:
        point_cloud: o3d.geometry.PointCloud = Handler.open(
            Files.OFF_GROUND_POINTS
        )

        point_cloud = Reduce.voxel_downsample(point_cloud=point_cloud)
        Visualize.display(point_cloud=point_cloud)


if __name__ == "__main__":
    Main.run()
