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
import unittest
from Scheduler.src.module_registry import get_function, register_function, function_registry

# Sample functions for testing
def sample_function_1():
    return "Function 1"

def sample_function_2(x):
    return f"Function 2 with {x}"

class TestFunctionRegistry(unittest.TestCase):
    def setUp(self):
        # Clear the function registry before each test
        function_registry.clear()

    def test_register_function(self):
        # Register functions
        register_function("func1", sample_function_1)
        register_function("func2", sample_function_2)
    
        # Check if functions are registered correctly
        self.assertIn("func1", function_registry)
        self.assertIn("func2", function_registry)
        
        # Check if registered functions are correct
        self.assertEqual(function_registry["func1"], sample_function_1)
        self.assertEqual(function_registry["func2"], sample_function_2)

    def test_get_function(self):
        register_function("func1", sample_function_1)

        # Retrieve function and check if it matches the registered function
        func = get_function("func1")
        self.assertEqual(func, sample_function_1)
        
        # Call function
        self.assertEqual(func(), "Function 1")

    def test_get_function_unknown(self):
        # Attempt to retrieve an unregistered function
        with self.assertRaises(ValueError) as cm:
            get_function("unknown_func")
        self.assertEqual(str(cm.exception), "Unknown function: unknown_func")

if __name__ == "__main__":
    unittest.main()