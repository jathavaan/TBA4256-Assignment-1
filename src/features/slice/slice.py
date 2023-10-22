import numpy as np
import open3d as o3d
from numpy import ndarray

from ...enums import Slice as SliceParameter
from ...utils import Utilities


class Slice:
    __slices: list[ndarray]

    def __init__(self, point_cloud: o3d.geometry.PointCloud) -> None:
        points: ndarray = Utilities.point_cloud_extract_XYZ_and_RGB(point_cloud)[0]
        assert points.ndim == 2
        assert points.shape[1] == 3
        self.slice_points(points)

    @property
    def slices(self) -> list[ndarray]:
        return self.__slices

    @slices.setter
    def slices(self, slices: list[ndarray]) -> None:
        self.__slices = slices

    def slice_points(self, points: ndarray) -> None:
        z: ndarray = points[:, 2]
        z_lower_bound: float = z.min()
        z_upper_bound: float = z_lower_bound + SliceParameter.SLICE_HEIGHT.value

        slices: list[ndarray] = []

        for i in range(SliceParameter.NO_SLICES.value):
            point_slices: ndarray = np.where((z >= z_lower_bound) & (z < z_upper_bound))[0]
            print(point_slices.shape)
            slices.append(points[point_slices])
            z_lower_bound = z_upper_bound + SliceParameter.SLICE_DISTANCE.value
            z_upper_bound = z_lower_bound + SliceParameter.SLICE_HEIGHT.value

        self.slices = slices
