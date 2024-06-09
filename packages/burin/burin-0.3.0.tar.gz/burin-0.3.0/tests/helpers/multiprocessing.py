"""
Burin Test Multiprocessing Helpers

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import os

# Coverage imports
from coverage import Coverage


# Local references
_os_exit = os._exit

def coverage_safe_exit(status):
    """
    Exits a process using the provided status in a way so coverage is saved.

    :param status: The exit status of the process.
    :type status: int
    """

    cov = Coverage.current()
    cov.stop()
    cov.save() # pragma: no cover
    _os_exit(status) # pragma: no cover
