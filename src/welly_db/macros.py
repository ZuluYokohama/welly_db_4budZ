"""
macros.py

Macro registry and decorator support for FancyWellDatabaseObject.

In this Phase 1 harness the actual @register_macro lives on the FancyWellDatabaseObject
instance (for simplicity and to keep the object as the single source of truth).

This module can be expanded to hold standalone @register_macro and a global registry
if needed for Power Automate / FastAPI surfaces (F5).
"""

from __future__ import annotations
from typing import Callable, Dict

# Placeholder for future standalone registry
_macro_registry: Dict[str, Callable] = {}

def register_macro(name: str):
    def deco(fn: Callable):
        if name in _macro_registry:
            raise ValueError(f"Macro already registered: {name}")
        _macro_registry[name] = fn
        return fn
    return deco

def get_macro(name: str):
    return _macro_registry.get(name)
