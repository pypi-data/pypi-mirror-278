
# -- import packages ----------------------------------------------------------
import ABCParse as ABCParse
import logging as logging
import pathlib as pathlib


# -- import local dependencies ------------------------------------------------
from ._log_config import LogConfig


# -- Operational class: PackageLogging ----------------------------------------
class PackageLogging(ABCParse.ABCParse):
    """
    A class to handle logging configurations for a package.

    This class sub-classes ABCParse.ABCParse and sets up logging for a given
    package, ensuring that logs are stored in a specified location and format.

    Attributes:
        name (str): The name of the package for which logging is configured.
        file (str): The file path from where the logging is initialized.
    """

    def __init__(self, name: str, file: str, *args, **kwargs):
        """
        Initialize the PackageLogging with the package name and file path.

        Args:
            name (str): The name of the package.
            file (str): The file path of the script.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        self.__parse__(locals())

        self.logger.info(
            f"Logs for {self._name} will be saved to: {self.log_config.log_fpath}"
        )
        self.logger.debug(f"Importing from local install location: {self._file}")

    @property
    def fname(self) -> str:
        """
        Get the name of the parent directory of the file path.

        Returns:
            str: The name of the parent directory.
        """
        return pathlib.Path(self._file).parent.name

    @property
    def _log_fpath(self) -> str:
        """
        Generate the log file path using the package name.

        Returns:
            str: The log file path.
        """
        return f"{self._name}.log"

    @property
    def log_config(self) -> LogConfig:
        """
        Get or initialize the log configuration for the package.

        Returns:
            LogConfig: The log configuration object.
        """
        if not hasattr(self, "_log_config"):
            self._log_config = LogConfig(name=self._name, log_file=self._log_fpath)
        return self._log_config

    @property
    def logger(self) -> logging.Logger:
        """
        Get or initialize the logger for the package.

        Returns:
            logging.Logger: The logger object.
        """
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(f"{self._name}.{self.fname}")
        return self._logger
