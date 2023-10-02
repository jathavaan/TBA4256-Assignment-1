import numpy as np
import open3d as o3d
import pandas as pd
from laspy.lasdata import LasData

from . import Utillities


class Conversion:
    @staticmethod
    def dataframe_to_point_cloud(dataframe: pd.DataFrame) -> o3d.geometry.PointCloud:
        XYZ, RGB = Utillities.dataframe_extract_XYZ_and_RGB(dataframe)

        point_cloud: o3d.geometry.PointCloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(XYZ)
        point_cloud.colors = o3d.utility.Vector3dVector(RGB)

        return point_cloud

    def point_format_3_to_df(las: 'LasData') -> pd.DataFrame:
        x_coordinates: np.ndarray = np.array(las.x)
        y_coordinates: np.ndarray = np.array(las.y)
        z_coordinates: np.ndarray = np.array(las.z)

        red_channel: np.ndarray = las.red
        green_channel: np.ndarray = las.green
        blue_channel: np.ndarray = las.blue

        points: pd.DataFrame = pd.DataFrame(
            columns=['X', 'Y', 'Z', 'red', 'green', 'blue'],
        )

        points["X"] = x_coordinates
        points["Y"] = y_coordinates
        points["Z"] = z_coordinates

        points["red"] = Conversion.color_16_bit_to_color_8_bit(red_channel)
        points["green"] = Conversion.color_16_bit_to_color_8_bit(green_channel)
        points["blue"] = Conversion.color_16_bit_to_color_8_bit(blue_channel)

        return points

    @staticmethod
    def color_16_bit_to_color_8_bit(colors: np.ndarray) -> np.ndarray:
        return np.divide(colors, 65535)
