"""
Functions and routines associated with Enasis Network Common Library.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""



from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from .logger import LOGLEVELS
from ..crypts import CryptsParams



class ConfigParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    :param paths: Complete or relative path to config paths.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    paths: Optional[list[str]] = None



class LoggerParams(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    :param stdo_level: Minimum level for the message to pass.
    :param file_level: Minimum level for the message to pass.
    :param file_path: Enables writing to the filesystem path.
    """

    stdo_level: Optional[LOGLEVELS] = None
    file_level: Optional[LOGLEVELS] = None
    file_path: Optional[str] = None


    def __init__(
        self,
        stdo_level: Optional[LOGLEVELS] = None,
        file_level: Optional[LOGLEVELS] = None,
        file_path: Optional[str | Path] = None,
    ) -> None:
        """
        Initialize instance for class using provided parameters.
        """

        if file_path is not None:
            file_path = str(file_path)

        super().__init__(
            stdo_level=stdo_level,
            file_level=file_level,
            file_path=file_path)



class Params(BaseModel, extra='forbid'):
    """
    Process and validate the core configuration parameters.

    :param enconfig: Configuration for the Config instance.
    :param enlogger: Configuration for the Logger instance.
    :param encrypts: Configuration for the Crypts instance.
    :param data: Keyword arguments passed to Pydantic model.
        Parameter is picked up by autodoc, please ignore.
    """

    enconfig: Optional[ConfigParams] = None
    enlogger: Optional[LoggerParams] = None
    encrypts: Optional[CryptsParams] = None
