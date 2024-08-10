# Copyright 2024 Sola Richard Olorunfemi
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable, Dict

function_registry: Dict[str, Callable] = {}


def register_function(name: str, func: Callable) -> None:
    """Register a function dynamically."""
    function_registry[name] = func


def get_function(name: str) -> Callable:
    """Retrieve a function by name."""
    if name not in function_registry:
        raise ValueError(f"Unknown function: {name}")
    return function_registry[name]
