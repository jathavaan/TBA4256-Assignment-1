from abc import ABC, abstractmethod
import os
import time
from turtle import pd
import numpy as np
import open3d as o3d
import laspy
from laspy.lasdata import LasData

from ... import Config
from ...enums import Files
from ...utils import Conversion


class IHandler(ABC):
    @staticmethod
    @abstractmethod
    def open(file: 'Files') -> o3d.geometry.PointCloud:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def save(point_cloud: o3d.geometry.PointCloud) -> None:
        raise NotImplementedError


class Handler(IHandler):
    @staticmethod
    def open(file: 'Files') -> o3d.geometry.PointCloud:
        path: str = os.path.join(Config.INPUT_DIR.value, file.value)

        with laspy.open(path) as laspy_file:
            las: 'LasData' = laspy_file.read()

        point_count: int = len(las.points)
        print(f"Loaded {point_count} points from {file.value}")

        point_df: pd.DataFrame = Conversion.point_format_3_to_df(las=las)
        points: np.ndarray = np.array(point_df[["X", "Y", "Z"]])
        colors: np.ndarray = np.array(point_df[["red", "green", "blue"]])

        point_cloud: o3d.geometry.PointCloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)
        point_cloud.colors = o3d.utility.Vector3dVector(colors)

        return point_cloud

    @staticmethod
    def save(point_cloud: o3d.geometry.PointCloud) -> None:
        filename: str = time.strftime("%Y%m%d-%H%M%S") + ".las"
        path: str = os.path.join(Config.OUTPUT_DIR.value, filename)
        o3d.io.write_point_cloud(filename=path, pointcloud=point_cloud)
        print(f"Saved point cloud to {path}")
