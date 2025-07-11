"""
Component-specific styles for the Excel Translator application.

This module contains styling definitions for individual UI components
to maintain a consistent and modern appearance throughout the application.
"""

from .button_styles import BUTTON_STYLES
from .combo_box_styles import COMBO_BOX_STYLES
from .progress_bar_styles import PROGRESS_BAR_STYLES
from .check_box_styles import CHECK_BOX_STYLES
from .drag_drop_styles import DRAG_DROP_STYLES
from .main_window_styles import MAIN_WINDOW_STYLES

# Combine all component styles
COMPONENT_STYLES = f"""
{BUTTON_STYLES}

{COMBO_BOX_STYLES}

{PROGRESS_BAR_STYLES}

{CHECK_BOX_STYLES}

{DRAG_DROP_STYLES}

{MAIN_WINDOW_STYLES}
"""

# Individual style getters for specific components
def get_button_styles():
    """Get button component styles."""
    return BUTTON_STYLES

def get_combo_box_styles():
    """Get combo box component styles."""
    return COMBO_BOX_STYLES

def get_progress_bar_styles():
    """Get progress bar component styles."""
    return PROGRESS_BAR_STYLES

def get_check_box_styles():
    """Get check box component styles."""
    return CHECK_BOX_STYLES

def get_drag_drop_styles():
    """Get drag and drop component styles."""
    return DRAG_DROP_STYLES

def get_main_window_styles():
    """Get main window component styles."""
    return MAIN_WINDOW_STYLES

def get_component_style(component_name: str) -> str:
    """
    Get styles for a specific component.
    
    Args:
        component_name: Name of the component
        
    Returns:
        CSS styles for the component
    """
    style_getters = {
        'button': get_button_styles,
        'combo_box': get_combo_box_styles,
        'progress_bar': get_progress_bar_styles,
        'check_box': get_check_box_styles,
        'drag_drop': get_drag_drop_styles,
        'main_window': get_main_window_styles,
    }
    
    getter = style_getters.get(component_name)
    return getter() if getter else ""

def get_all_styles() -> str:
    """
    Get all component styles combined.
    
    Returns:
        All CSS styles combined
    """
    return COMPONENT_STYLES
