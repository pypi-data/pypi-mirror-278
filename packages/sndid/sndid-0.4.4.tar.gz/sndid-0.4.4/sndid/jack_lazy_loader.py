# sndid/jack_lazy_loader.py
# Copyright 2024, Jeff Moe <moe@spacecruft.org>
# Licensed under the Apache License, Version 2.0
import importlib
import logging

_import_cache = {}


def jack_lazy_load(module_name):
    logging.debug(f"Starting lazy load for: {module_name}")
    if module_name in _import_cache:
        logging.debug(f"Returning cached version of {module_name}")
        return _import_cache[module_name]
    logging.debug(f"Importing and caching {module_name} for the first time")
    module = importlib.import_module(module_name)
    _import_cache[module_name] = module
    logging.debug(f"{module_name} successfully imported and cached")
    return module
