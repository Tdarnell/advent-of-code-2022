#
# File created on Wed Dec 04 2024 21:29:34 by T.Darnell
#
# The MIT License (MIT)
# Copyright (c) 2024 T.Darnell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import logging
from pathlib import Path
import time


def set_up_logger(day: int) -> logging.Logger:
    LOGGER: logging.Logger = logging.getLogger(f"day{day:02d}")
    LOGGER.setLevel(logging.INFO)
    # Create a file handler
    file_handler = logging.FileHandler(f"logs/day{day:02d}.log")
    file_handler.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    # Create a logging format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # Add the handlers to the logger
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)
    return LOGGER


def read_day_input(day: int) -> str:
    """
    Read the input file and return the contents as a string.

    Parameters
    ----------
    input_file : Path
        The path to the input file.

    Returns
    -------
    str
        The contents of the input file as a string, this is not split into lines.
    """
    input_file: Path = Path(f"inputs/day{day:02d}.txt")
    if not isinstance(input_file, Path):
        raise AttributeError(
            "Expected an input_file of type Path, got type ", type(input_file)
        )
    if not input_file.exists():
        raise FileNotFoundError(f"Input file {input_file} not found.")
    with open(input_file, "r") as f:
        return f.read().strip()


def log_execution_time(func=None, *, logger=None):
    """
    Decorator that logs the execution time of a function.

    Parameters
    ----------
    func : callable, optional
        The function to wrap.
    logger : logging.Logger, optional
        The logger to use. If not provided, the root logger will be used.

    Returns
    -------
    callable
        The wrapped function.
    """

    if func is None:
        return lambda f: log_execution_time(f, logger=logger)

    if logger is None:
        logger = logging.getLogger()

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(
            f"Function {func.__name__} executed in {end_time - start_time:.4f} seconds"
        )
        return result

    return wrapper
