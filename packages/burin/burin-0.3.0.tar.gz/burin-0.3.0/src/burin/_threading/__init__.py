"""
Burin Threading Utilities

Copyright (c) 2022-2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Package contents
from ._fork_protection import _register_at_fork_reinit_lock
from ._lock import _BurinLock


__all__ = []
