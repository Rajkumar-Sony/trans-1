# Create professional dropdown arrow icons
from PIL import Image, ImageDraw
import os

# Create assets directory if it doesn't exist
os.makedirs('/Users/pb0595/workspace/project/Translator-app1/assets/icons', exist_ok=True)

def create_professional_arrow(size=16, color='#cccccc', direction='down'):
    """Create a professional, crisp arrow icon"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate arrow dimensions for a more professional look
    center_x = size // 2
    center_y = size // 2
    arrow_width = size // 2  # Wider arrow
    arrow_height = size // 4  # Shorter height for better proportion
    
    # Convert hex color to RGB
    if color.startswith('#'):
        color = color[1:]
    rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    if direction == 'down':
        # Create a clean triangular arrow pointing down
        points = [
            (center_x - arrow_width, center_y - arrow_height),
            (center_x + arrow_width, center_y - arrow_height),
            (center_x, center_y + arrow_height)
        ]
    else:  # up
        # Create a clean triangular arrow pointing up
        points = [
            (center_x - arrow_width, center_y + arrow_height),
            (center_x + arrow_width, center_y + arrow_height),
            (center_x, center_y - arrow_height)
        ]
    
    # Draw filled triangle for professional look
    draw.polygon(points, fill=rgb + (255,))
    
    # Add subtle anti-aliasing by drawing a slightly smaller triangle on top
    if direction == 'down':
        inner_points = [
            (center_x - arrow_width + 1, center_y - arrow_height + 1),
            (center_x + arrow_width - 1, center_y - arrow_height + 1),
            (center_x, center_y + arrow_height - 1)
        ]
    else:
        inner_points = [
            (center_x - arrow_width + 1, center_y + arrow_height - 1),
            (center_x + arrow_width - 1, center_y + arrow_height - 1),
            (center_x, center_y - arrow_height + 1)
        ]
    
    # Draw the inner triangle with slightly darker color for smooth edges
    inner_rgb = tuple(max(0, c - 10) for c in rgb)
    draw.polygon(inner_points, fill=inner_rgb + (255,))
    
    return img

# Create professional arrow icons
arrow_down_normal = create_professional_arrow(16, '#cccccc', 'down')
arrow_down_hover = create_professional_arrow(16, '#ffffff', 'down')
arrow_up_normal = create_professional_arrow(16, '#cccccc', 'up')
arrow_up_hover = create_professional_arrow(16, '#ffffff', 'up')

# Save the icons
arrow_down_normal.save('/Users/pb0595/workspace/project/Translator-app1/assets/icons/dropdown_arrow.png')
arrow_down_hover.save('/Users/pb0595/workspace/project/Translator-app1/assets/icons/dropdown_arrow_hover.png')
arrow_up_normal.save('/Users/pb0595/workspace/project/Translator-app1/assets/icons/dropdown_arrow_up.png')
arrow_up_hover.save('/Users/pb0595/workspace/project/Translator-app1/assets/icons/dropdown_arrow_up_hover.png')

print("Professional dropdown arrow icons created successfully!")
print("- dropdown_arrow.png (▼ down, normal)")
print("- dropdown_arrow_hover.png (▼ down, hover)")
print("- dropdown_arrow_up.png (▲ up, normal)")
print("- dropdown_arrow_up_hover.png (▲ up, hover)")
