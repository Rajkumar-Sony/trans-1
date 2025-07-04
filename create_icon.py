#!/usr/bin/env python3
"""
Simple icon generator for the Excel Translator App
Creates a simple PNG icon using Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_app_icon():
        """Create a simple app icon."""
        # Create a 256x256 image with transparent background
        size = 256
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Background circle
        margin = 20
        draw.ellipse([margin, margin, size-margin, size-margin], 
                    fill=(14, 99, 156, 255), outline=(255, 255, 255, 100), width=4)
        
        # Excel-like grid
        grid_start = 60
        grid_end = 196
        grid_spacing = 34
        
        # Draw grid lines
        for i in range(5):
            y = grid_start + i * grid_spacing
            draw.line([(grid_start, y), (grid_end, y)], fill=(255, 255, 255, 180), width=2)
            
        for i in range(5):
            x = grid_start + i * grid_spacing
            draw.line([(x, grid_start), (x, grid_end)], fill=(255, 255, 255, 180), width=2)
        
        # Add translation arrows
        arrow_y = size // 2
        arrow_left = 40
        arrow_right = size - 40
        
        # Left arrow (pointing right)
        draw.polygon([(arrow_left, arrow_y), (arrow_left + 15, arrow_y - 8), 
                     (arrow_left + 15, arrow_y + 8)], fill=(255, 255, 255, 255))
        
        # Right arrow (pointing right)  
        draw.polygon([(arrow_right - 15, arrow_y - 8), (arrow_right - 15, arrow_y + 8), 
                     (arrow_right, arrow_y)], fill=(255, 255, 255, 255))
        
        # Save as PNG
        icon_path = os.path.join('assets', 'icon.png')
        os.makedirs('assets', exist_ok=True)
        image.save(icon_path, 'PNG')
        
        # Also create a smaller version for taskbar
        small_icon = image.resize((64, 64), Image.Resampling.LANCZOS)
        small_icon.save(os.path.join('assets', 'icon_small.png'), 'PNG')
        
        print(f"✓ App icon created: {icon_path}")
        return True
        
    if __name__ == "__main__":
        create_app_icon()
        
except ImportError:
    print("Pillow not installed. Skipping icon creation.")
    print("Install with: pip install Pillow")
