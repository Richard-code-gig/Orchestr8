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
