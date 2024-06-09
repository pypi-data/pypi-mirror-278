"""
Burin Test Helpers

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Package imports
from .multiprocessing import coverage_safe_exit
from .requirements import (requires_fork, requires_fork_with_threading,
                           requires_register_at_fork, requires_threading)

__all__ = ["coverage_safe_exit", "requires_fork",
           "requires_fork_with_threading", "requires_register_at_fork",
           "requires_threading"]
