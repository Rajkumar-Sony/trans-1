"""
Styles Package

This package contains all styling definitions for the Excel Translator application.
"""

from .global_style import get_application_stylesheet, get_theme_color, get_typography_value
from .component_styles import get_all_styles, get_component_style

__all__ = [
    'get_application_stylesheet',
    'get_theme_color',
    'get_typography_value',
    'get_all_styles',
    'get_component_style'
]
