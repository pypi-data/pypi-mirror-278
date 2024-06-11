# sndid/jack_lazy_loader.py
"""
jack_lazy_loader.py

Copyright 2024, Jeff Moe <moe@spacecruft.org>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
