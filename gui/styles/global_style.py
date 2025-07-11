"""
Global styles for the Excel Translator application.

This module provides the main styling system that combines all component
styles and applies them consistently across the application.
"""

from typing import Dict, Optional
from .component_styles import get_all_styles

# Base application theme colors
THEME_COLORS = {
    'primary': '#007bff',
    'secondary': '#6c757d', 
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'white': '#ffffff',
    'transparent': 'transparent'
}

# Typography settings
TYPOGRAPHY = {
    'font_family': "'Segoe UI', 'SF Pro Display', system-ui, sans-serif",
    'font_size_xs': '10px',
    'font_size_sm': '12px',
    'font_size_base': '14px',
    'font_size_lg': '16px',
    'font_size_xl': '18px',
    'font_size_xxl': '24px',
    'font_weight_normal': '400',
    'font_weight_medium': '500',
    'font_weight_semibold': '600',
    'font_weight_bold': '700'
}

# Spacing and layout
SPACING = {
    'xs': '4px',
    'sm': '8px',
    'md': '12px',
    'lg': '16px',
    'xl': '20px',
    'xxl': '24px'
}

# Border radius
BORDER_RADIUS = {
    'sm': '3px',
    'base': '6px',
    'lg': '8px',
    'xl': '12px',
    'full': '50%'
}

# Global base styles
GLOBAL_BASE_STYLES = f"""
/* Global Application Styles */
* {{
    font-family: {TYPOGRAPHY['font_family']};
    outline: none;
}}

QWidget {{
    background-color: {THEME_COLORS['white']};
    color: #495057;
    font-size: {TYPOGRAPHY['font_size_base']};
    selection-background-color: {THEME_COLORS['primary']};
    selection-color: {THEME_COLORS['white']};
}}

/* Tooltips */
QToolTip {{
    background-color: #343a40;
    color: #ffffff;
    border: 1px solid #495057;
    border-radius: {BORDER_RADIUS['base']};
    padding: {SPACING['sm']} {SPACING['md']};
    font-size: {TYPOGRAPHY['font_size_sm']};
}}

/* Focus styles for accessibility */
*:focus {{
    outline: 2px solid #80bdff;
    outline-offset: 2px;
}}

/* Disabled widget styles */
*:disabled {{
    color: #6c757d;
    background-color: #e9ecef;
}}

/* Animation support */
* {{
    transition: all 0.2s ease-in-out;
}}

/* Scrollbar base styles */
QScrollBar {{
    background-color: {THEME_COLORS['light']};
    border-radius: {BORDER_RADIUS['base']};
}}

QScrollBar::handle {{
    background-color: #ced4da;
    border-radius: {BORDER_RADIUS['base']};
    min-height: 20px;
    margin: 2px;
}}

QScrollBar::handle:hover {{
    background-color: #adb5bd;
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0;
    width: 0;
}}

QScrollBar::add-page, QScrollBar::sub-page {{
    background: none;
}}
"""

def apply_global_styles() -> str:
    """
    Generate and return the complete global stylesheet.
    
    Returns:
        Complete CSS stylesheet string
    """
    component_styles = get_all_styles()
    
    return f"""
    {GLOBAL_BASE_STYLES}
    
    {component_styles}
    """

def get_theme_color(color_name: str) -> str:
    """
    Get a theme color by name.
    
    Args:
        color_name: Name of the color
        
    Returns:
        Color hex value or default
    """
    return THEME_COLORS.get(color_name, THEME_COLORS['primary'])

def get_typography_value(property_name: str) -> str:
    """
    Get a typography value by property name.
    
    Args:
        property_name: Name of the typography property
        
    Returns:
        Typography value or default
    """
    return TYPOGRAPHY.get(property_name, TYPOGRAPHY['font_size_base'])

def get_spacing_value(size_name: str) -> str:
    """
    Get a spacing value by size name.
    
    Args:
        size_name: Name of the spacing size
        
    Returns:
        Spacing value or default
    """
    return SPACING.get(size_name, SPACING['md'])

def get_border_radius_value(size_name: str) -> str:
    """
    Get a border radius value by size name.
    
    Args:
        size_name: Name of the border radius size
        
    Returns:
        Border radius value or default
    """
    return BORDER_RADIUS.get(size_name, BORDER_RADIUS['base'])

def create_custom_stylesheet(
    base_styles: bool = True,
    components: Optional[list] = None,
    custom_styles: str = ""
) -> str:
    """
    Create a custom stylesheet with specific components.
    
    Args:
        base_styles: Whether to include base global styles
        components: List of component names to include
        custom_styles: Additional custom CSS
        
    Returns:
        Custom stylesheet string
    """
    stylesheet_parts = []
    
    if base_styles:
        stylesheet_parts.append(GLOBAL_BASE_STYLES)
    
    if components:
        from .component_styles import get_component_style
        for component in components:
            component_style = get_component_style(component)
            if component_style:
                stylesheet_parts.append(component_style)
    else:
        # Include all component styles if none specified
        stylesheet_parts.append(get_all_styles())
    
    if custom_styles:
        stylesheet_parts.append(custom_styles)
    
    return "\n\n".join(stylesheet_parts)

def get_dark_theme_styles() -> str:
    """
    Generate dark theme styles.
    
    Returns:
        Dark theme CSS styles
    """
    return """
    /* Dark Theme Overrides */
    QWidget[darkTheme="true"] {
        background-color: #343a40;
        color: #f8f9fa;
    }
    
    QWidget[darkTheme="true"]:disabled {
        color: #6c757d;
        background-color: #495057;
    }
    
    QToolTip[darkTheme="true"] {
        background-color: #212529;
        color: #f8f9fa;
        border-color: #495057;
    }
    
    QScrollBar[darkTheme="true"] {
        background-color: #495057;
    }
    
    QScrollBar[darkTheme="true"]::handle {
        background-color: #6c757d;
    }
    
    QScrollBar[darkTheme="true"]::handle:hover {
        background-color: #868e96;
    }
    """

# Main stylesheet function for easy import
def get_application_stylesheet() -> str:
    """
    Get the complete application stylesheet.
    
    Returns:
        Complete application stylesheet
    """
    return apply_global_styles()
