
# -- import packages: ---------------------------------------------------------
import ABCParse
import logging
import pathlib


# -- set typing: --------------------------------------------------------------
from typing import Union


# -- operational class: LogConfig ---------------------------------------------
class LogConfig(ABCParse.ABCParse):
    """
    A class to configure logging for a package.

    This class extends ABCParse and sets up logging with both file and console
    handlers. It provides flexible options for log file paths, directories, and
    logging levels.

    Attributes:
        name (Union[pathlib.Path, str]): The name of the logger.
        log_file (Union[pathlib.Path, str]): The name of the log file.
        log_dir (Union[pathlib.Path, str]): The directory where log files will
            be stored.
        dirname (Union[pathlib.Path, str]): The subdirectory within the log_dir
            for storing logs.
        file_level (int): The logging level for the file handler.
        console_level (int): The logging level for the console handler.
    """
    def __init__(
        self,
        name: Union[pathlib.Path, str] = "py_pkg_logger",
        log_file: Union[pathlib.Path, str] = "log.log",
        log_dir: Union[pathlib.Path, str] = pathlib.Path.cwd(),
        dirname: Union[pathlib.Path, str] = ".log_cache",
        file_level: int = logging.DEBUG,
        console_level: int = logging.INFO,
        *args,
        **kwargs
    ):
        """
        Initialize the LogConfig with the specified parameters.

        Args:
            name (Union[pathlib.Path, str]): The name of the logger.
                Default: ``"py_pkg_logger"``

            log_file (Union[pathlib.Path, str]): The name of the log file.
                Default: ``"log.log"``

            log_dir (Union[pathlib.Path, str]): The directory for logs.
                Default: ``pathlib.Path.cwd()``

            dirname (Union[pathlib.Path, str]): The subdirectory within the log directory.
                Default: ``".log_cache"``

            file_level (int): The logging level for the file handler.
                Default: ``logging.DEBUG``

            console_level (int): The logging level for the console handler.
                Default: ``logging.INFO``

        Returns:
            None
        """
        self.__parse__(locals())

        if not self.log_dir.exists():
            self.log_dir.mkdir()

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)

    @property
    def log_dir(self) -> pathlib.Path:
        """
        Get the full path to the log directory.

        Returns:
            pathlib.Path: The full path to the log directory including the subdirectory.
        """
        return pathlib.Path(self._log_dir).joinpath(self._dirname)

    @property
    def log_fpath(self) -> pathlib.Path:
        """
        Get the full path to the log file.

        Returns:
            pathlib.Path: The full path to the log file within the log directory.
        """
        return self.log_dir.joinpath(self._log_file)

    @property
    def logger(self):
        """
        Get or initialize the logger.

        Returns:
            logging.Logger: The logger object.
        """
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(self._name)
            self._logger.setLevel(logging.DEBUG)
        return self._logger

    @property
    def file_formatter(self):
        """
        Get the formatter for the file handler.

        Returns:
            logging.Formatter: The formatter with timestamp, logger name, and message.
        """
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    @property
    def file_handler(self):
        """
        Get or initialize the file handler.

        Returns:
            logging.FileHandler: The file handler configured with the formatter and logging level.
        """
        if not hasattr(self, "_file_handler"):
            self._file_handler = logging.FileHandler(self.log_fpath)
            self._file_handler.setFormatter(self.file_formatter)
            self._file_handler.setLevel(self._file_level)
        return self._file_handler

    @property
    def console_formatter(self):
        """
        Get the formatter for the console handler.

        Returns:
            logging.Formatter: The formatter with logger name and message.
        """
        return logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    @property
    def console_handler(self):
        """
        Get or initialize the console handler.

        Returns:
            logging.StreamHandler: The console handler configured with the formatter and logging level.
        """
        if not hasattr(self, "_console_handler"):
            self._console_handler = logging.StreamHandler()
            self._console_handler.setFormatter(self.console_formatter)
            self._console_handler.setLevel(self._console_level)
        return self._console_handler
