# Test dropdown arrow display
from PIL import Image, ImageDraw, ImageFont
import os

# Load the created icons
try:
    icon_path = '/Users/pb0595/workspace/project/Translator-app1/assets/icons/dropdown_arrow.png'
    icon_hover_path = '/Users/pb0595/workspace/project/Translator-app1/assets/icons/dropdown_arrow_hover.png'
    
    icon_normal = Image.open(icon_path)
    icon_hover = Image.open(icon_hover_path)
    
    print("✅ Dropdown arrow icons loaded successfully!")
    print(f"Normal icon size: {icon_normal.size}")
    print(f"Hover icon size: {icon_hover.size}")
    print(f"Normal icon mode: {icon_normal.mode}")
    print(f"Hover icon mode: {icon_hover.mode}")
    
    # Create a preview image showing both icons
    preview_width = 200
    preview_height = 100
    preview = Image.new('RGB', (preview_width, preview_height), '#3c3c3c')
    draw = ImageDraw.Draw(preview)
    
    # Add labels and icons
    draw.text((10, 10), "Normal:", fill='#cccccc')
    draw.text((10, 50), "Hover:", fill='#ffffff')
    
    # Paste icons (scaled up for visibility)
    icon_normal_scaled = icon_normal.resize((24, 24), Image.Resampling.LANCZOS)
    icon_hover_scaled = icon_hover.resize((24, 24), Image.Resampling.LANCZOS)
    
    preview.paste(icon_normal_scaled, (70, 5), icon_normal_scaled)
    preview.paste(icon_hover_scaled, (70, 45), icon_hover_scaled)
    
    # Save preview
    preview.save('/Users/pb0595/workspace/project/Translator-app1/assets/icons/dropdown_preview.png')
    print("✅ Preview image created: assets/icons/dropdown_preview.png")
    
except Exception as e:
    print(f"❌ Error loading icons: {e}")
