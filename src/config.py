import os
from enum import Enum


class Config(Enum):
    # Paths
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(ROOT_DIR, 'data')
    INPUT_DIR = os.path.join(DATA_DIR, 'input')
    OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

    # Plotting
    COLOR_MAP: str = 'tab20'
