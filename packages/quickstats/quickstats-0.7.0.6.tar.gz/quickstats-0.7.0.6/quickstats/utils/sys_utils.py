import os
import sys
import shlex

from typing import Optional

def add_python_path(path:str):
    """
    Add a path to the Python search path and the PYTHONPATH environment variable if not already present.
    
    Parameters:
    - path (str): Path to add.
    """
    if path not in sys.path:
        sys.path.insert(0, path)
    PYTHONPATH = os.environ.get("PYTHONPATH", "")
    if path not in PYTHONPATH.split(":"):
        os.enviro['PYTHONPATH'] = f"{path}:{PYTHONPATH}"

def remove_python_path(path:str):
    """
    Remove a path from the Python search path and the PYTHONPATH environment variable if present.
    """
    if path in sys.path:
        sys.path.remove(path)
    PYTHONPATHS = os.environ.get("PYTHONPATH", "").split(":")
    if path in PYTHONPATHS:
        PYTHONPATHS.remove(path)
        os.environ["PYTHONPATH"] = ":".join(PYTHONPATHS)

def set_argv(cmd: str, expandvars:bool=True):
    """
    Modifies sys.argv based on a given command line string.

    Parameters:
    - cmd (str): The command line string to parse into sys.argv.
    - expandvars (bool, optional): Whether to expand environment variables in cmd. Defaults to False.
    """
    if expandvars:
        cmd = os.path.expandvars(cmd)
    # Use shlex.split to correctly parse the command line string into arguments,
    # handling cases with quotes and escaped characters appropriately.
    parsed_args = shlex.split(cmd)
    sys.argv = parsed_args

def bytes_to_readable(size_in_bytes, digits=2):
    """
    Convert the number of bytes to a human-readable string format.

    Parameters:
    size_in_bytes (int): The size in bytes that you want to convert.
    digits (int, optional): The number of decimal places to format the output. Default is 2.

    Returns:
    str: A string representing the human-readable format of the size.

    Examples:
    >>> bytes_to_readable(123456789)
    '117.74 MB'

    >>> bytes_to_readable(9876543210)
    '9.20 GB'

    >>> bytes_to_readable(123456789, digits=4)
    '117.7383 MB'

    >>> bytes_to_readable(999, digits=1)
    '999.0 B'
    """
    for unit in ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        if abs(size_in_bytes) < 1024.0:
            return f"{size_in_bytes:.{digits}f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.{digits}f} YB"