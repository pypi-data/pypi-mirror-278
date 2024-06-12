
# -- import packages: ---------------------------------------------------------
import ABCParse
import inspect
from functools import wraps
import logging
import numpy as np


# -- set typing: --------------------------------------------------------------
from typing import Any, Dict, Callable


# -- Operational class: -------------------------------------------------------
class FunctionCallLogger(ABCParse.ABCParse):
    """
    A class for logging the details of function calls.

    This class extends ABCParse and logs function names and their arguments
    when called. It also handles class methods and provides formatted logging
    messages.

    Attributes:
        logger (logging.Logger): The logger instance to be used for logging.
    """
    def __init__(self, logger):
        """
        Initialize the FunctionCallLogger with a logger.

        Args:
            logger (logging.Logger): Logger to log the function calls.
        """
        self.__parse__(locals())
        self._ARGS_IGNORE = ['self']

    @property
    def arg_values(self) -> Dict[str, Any]:
        """
        Return the bound arguments of the logged function.

        Returns:
            dict: A dictionary of the arguments and their values.
        """
        return self.bound.arguments

    @property
    def cls_method(self):
        """
        Check if the logged function is a method of a class.

        Returns:
            bool: True if the logged function is a class method, otherwise False.
        """
        return self._args and hasattr(self._args[0], self._logged_func.__name__)

    @property
    def bound(self):
        """
        Bind the arguments to the function signature.

        Returns:
            inspect.BoundArguments: The bound arguments for the function.
        """
        if self.cls_method:
            self._bound = inspect.signature(self._logged_func).bind(*self._args, **self._kwargs)
        else:
            self._bound = inspect.signature(self._logged_func).bind_partial(*self._args, **self._kwargs)
        self._bound.apply_defaults()
        return self._bound

    @property
    def func_name(self):
        """
        Get the name of the logged function, including class name if it's a method.

        Returns:
            str: The function name with class name if applicable.
        """
        if "self" in self.arg_values:
            cls = self.arg_values.pop("self").__class__.__name__
            return f"{cls}.{self._logged_func.__name__}"
        return self._logged_func.__name__
    
    @property
    def _arg_message(self):
        """
        Create a formatted string of the function's arguments and their values.

        Returns:
            str: A formatted string of arguments and values.
        """
        return_str = ""
        for key, val in self.arg_values.items():
            if not key in self._ARGS_IGNORE:
                if isinstance(val, np.ndarray):
                    val = f"np.ndarray of shape: {val.shape}"
                return_str += f"{key}={val}, "
        return return_str[:-2] # rm final comma
    
    @property
    def log_message(self):
        """
        Generate a log message for the function call.

        Returns:
            str: A formatted log message with function name and arguments.
        """
        return f"Called: {self.func_name} with args: {self._arg_message}"


    def __call__(self, logged_func: Callable, *args, **kwargs):
        """
        Log the function call.

        Args:
            logged_func (Callable): The function being logged.
            *args: Positional arguments passed to the function.
            **kwargs: Keyword arguments passed to the function.
        """
        self.__update__(locals())
        self._logger.debug(self.log_message)


# -- API-facing decorator function: -------------------------------------------
def log_function_call(logger):
    """
    A decorator to log function calls with provided logger.

    Args:
        logger (logging.Logger): The logger to use for logging the function calls.

    Returns:
        Callable: A decorator function that logs the calls of the decorated function.
    """
    def decorator(logged_func: Callable):
        @wraps(logged_func)
        def wrapper(*args, **kwargs):
            function_call_logger = FunctionCallLogger(logger=logger)
            function_call_logger(logged_func, *args, **kwargs)
            return logged_func(*args, **kwargs)
        return wrapper
    return decorator
