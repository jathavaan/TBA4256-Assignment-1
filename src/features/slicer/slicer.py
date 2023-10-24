import numpy as np
import open3d as o3d
from numpy import ndarray

from ...enums import Slice


class Slicer:
    __point_cloud_slices: list[o3d.geometry.PointCloud]

    def __init__(self, point_cloud: o3d.geometry.PointCloud) -> None:
        self.slice_point_cloud(point_cloud)

    @property
    def point_cloud_slices(self) -> list[o3d.geometry.PointCloud]:
        return self.__point_cloud_slices

    @point_cloud_slices.setter
    def point_cloud_slices(self, slices: list[o3d.geometry.PointCloud]) -> None:
        self.__point_cloud_slices = slices

    def slice_point_cloud(self, point_cloud: o3d.geometry.PointCloud) -> None:
        point_cloud_slices: list[o3d.geometry.PointCloud] = []
        point_cloud_bounding_box: o3d.geometry.PointCloud = point_cloud.get_axis_aligned_bounding_box()

        # Get the minimum and maximum z-coordinates of the bounding box
        x_lower_bound: float = point_cloud_bounding_box.get_min_bound()[0]
        x_upper_bound: float = point_cloud_bounding_box.get_max_bound()[0]

        y_lower_bound: float = point_cloud_bounding_box.get_min_bound()[1]
        y_upper_bound: float = point_cloud_bounding_box.get_max_bound()[1]

        z_lower_bound: float = point_cloud_bounding_box.get_min_bound()[2] + Slice.SLICE_DISTANCE.value
        z_upper_bound: float = z_lower_bound + Slice.SLICE_HEIGHT.value

        for i in range(Slice.NO_SLICES.value + Slice.NO_SKIP_SLICES.value):
            min_bound: ndarray = np.array([x_lower_bound, y_lower_bound, z_lower_bound])
            max_bound: ndarray = np.array([x_upper_bound, y_upper_bound, z_upper_bound])

            if i >= Slice.NO_SKIP_SLICES.value:
                slice_bounding_box: o3d.geometry.AxisAlignedBoundingBox = o3d.geometry.AxisAlignedBoundingBox(
                    min_bound=min_bound,
                    max_bound=max_bound
                )

                # Get the points within the bounding box
                sliced_point_cloud: o3d.geometry.PointCloud = point_cloud.crop(slice_bounding_box)
                point_cloud_slices.append(sliced_point_cloud)

            # Update the z-coordinates of the bounding box
            z_lower_bound = z_upper_bound + Slice.SLICE_DISTANCE.value
            z_upper_bound = z_lower_bound + Slice.SLICE_HEIGHT.value

        self.point_cloud_slices = point_cloud_slices
