# sndid/__init__.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import importlib.metadata

try:
    __version__ = importlib.metadata.version("sndid")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.1"
