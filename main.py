import open3d as o3d

from src import Config
from src.enums import Files
from src.features.point_cloud_handler import Handler


class Main:
    @staticmethod
    def run() -> None:
        point_cloud: o3d.geometry.PointCloud = Handler.open(
            Files.OFF_GROUND_POINTS
        )

        Handler.display(point_cloud=point_cloud)


if __name__ == "__main__":
    Main.run()
