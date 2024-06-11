from enum import Enum


class RelativePathType(Enum):
    """Enum for Supported Relative Path Type"""

    RELATIVE_TO_WORKING_DIRECTORY = "c"
    RELATIVE_TO_CURRENT_FILE = "f"
