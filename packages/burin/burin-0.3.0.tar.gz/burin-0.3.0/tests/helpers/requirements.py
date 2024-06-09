"""
Burin Test Requirements Helpers

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Python imports
import os
import sys
import sysconfig

# PyTest imports
import pytest


cflags = sysconfig.get_config_var("CFLAGS")
configArgs = sysconfig.get_config_var("CONFIG_ARGS")
currentPlaform = sys.platform

if cflags is None:
    cflags = ""
if configArgs is None:
    configArgs = ""


# Forking isn't supported in WASI, Emscripten, Apple Mobile OSes, or Android
noForkPlatforms = ["android", "emscripten", "ios", "tvos", "wasi", "watchos"]

hasWorkingFork = hasattr(os, "fork") and (currentPlaform not in noForkPlatforms)

requires_fork = pytest.mark.skipif(not hasWorkingFork,
                                   reason="requires fork support")

hasRegisterAtFork = hasWorkingFork and hasattr(os, "register_at_fork")

requires_register_at_fork = pytest.mark.skipif(not hasRegisterAtFork,
                                               reason="requires 'os' to have "
                                               "'register_at_fork' function")

# Threading isn't supported in WASI and is a compilation option for Emscripten
hasWorkingThreading = True

if currentPlaform == "emscripten":
    hasWorkingThreading = sys._emscripten_info.pthreads
elif currentPlaform == "wasi":
    hasWorkingThreading = False

requires_threading = pytest.mark.skipif(not hasWorkingThreading,
                                        reason="requires threading support")

# Forking with threading is inherently unsafe, but is more likely to cause
# issues with the tests if address or thread sanitizer support were compiled in
hasAddressSanitizer = "-fsanitize=address" in cflags or "--with-address-sanitizer" in configArgs
hasThreadSanitizer = "-fsanitize=thread" in cflags or "--with-thread-sanitizer" in configArgs

canForkWithThreads = hasWorkingFork and hasWorkingThreading and not (hasAddressSanitizer or hasThreadSanitizer)

requires_fork_with_threading = pytest.mark.skipif(not canForkWithThreads,
                                                 reason="requires support for "
                                                 "fork and threading together")
