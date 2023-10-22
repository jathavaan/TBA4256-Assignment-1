import os
from enum import Enum


class Config(Enum):
    # Paths
    ROOT_DIR: str = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(__file__)))))
    DATA_DIR: str = os.path.join(ROOT_DIR, 'data')
    INPUT_DIR: str = os.path.join(DATA_DIR, 'input')
    OUTPUT_DIR: str = os.path.join(DATA_DIR, 'output')

    # Plotting
    COLOR_MAP: str = 'tab20'

    PARAMETER_SET: int = 1
