from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random
import io
import os
from datetime import datetime

# Define the font file path (Use a bundled or well-known local path for robustness)
# NOTE: Replace 'path/to/your/font.ttf' with a real path to a font like Roboto or OpenSans
# For deployment, ensure this font file is available in the environment.
FONT_PATH = "arial.ttf" # Keep arial.ttf for system compatibility, but highly recommend bundling a font.

def generate_project_og(title, tagline):
    width, height = 1200, 630
    bg_color = (15, 23, 42)  # Dark navy

    # 1️⃣ Canvas
    # Use 'RGBA' for blending and then convert to 'RGB' at the end for efficiency
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 2️⃣ Soft Gradient Overlay (Optimized)
    # This gradient is subtle and correct.
    for i in range(height):
        shade = int(15 + (i / height) * 25)
        draw.line([(0, i), (width, i)], fill=(shade, shade, shade))
    
    # 3️⃣ Random Glow Blobs (Cleaned up blending)
    for _ in range(3): # Reduced count slightly for speed
        x = random.randint(-200, width)
        y = random.randint(-200, height)
        r = random.randint(200, 400)

        # Create blob in RGB mode
        blob = Image.new("RGB", (width, height), bg_color) 
        b_draw = ImageDraw.Draw(blob)
        # Draw soft cyan blob
        b_draw.ellipse((x, y, x + r, y + r), fill=(56, 189, 248)) 
        
        # Apply intense blur and blend back
        blob = blob.filter(ImageFilter.GaussianBlur(radius=160)) 
        img = Image.blend(img, blob, alpha=0.15) # Slightly lower alpha

    draw = ImageDraw.Draw(img)

    # 4️⃣ Fonts (Robust Loading)
    def load_font(size):
        try:
            # Check if bundled font exists, otherwise fall back to system font, then default.
            return ImageFont.truetype(FONT_PATH, size)
        except IOError:
            print(f"Warning: Could not load font at {FONT_PATH}. Using default.")
            return ImageFont.load_default(size=size)
            
    font_title = load_font(70)
    font_tagline = load_font(40)
    font_footer = load_font(32)

    # 5️⃣ Auto-wrap title
    wrapped_title = textwrap.fill(title.upper(), width=20)
    
    # --- Title Positioning and Neon Glow ---
    # NOTE: Keep multiline_textsize temporarily, as accurate replacement is complex without knowing requirements.
    # It is deprecated, but functional in current stable versions.
    title_w, title_h = draw.multiline_textsize(wrapped_title, font=font_title, spacing=10)
    title_x = (width - title_w) // 2
    title_y = height // 2 - 100 # Adjusted vertical center slightly

    # 6️⃣ Neon Glow Effect (Using ImageDraw again is the correct, cleaner way)
    glow_color = (56, 189, 248) 
    
    # 6.1 Create the glow layer
    glow_layer = Image.new("RGB", (width, height), bg_color)
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.multiline_text((title_x, title_y), wrapped_title, font=font_title, fill=glow_color, spacing=10)

    # 6.2 Blur and Blend
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(14)) # Slightly higher blur
    img = Image.blend(img, glow_layer, 0.60) # Slightly higher blend alpha

    # 6.3 Draw Title (clean text)
    draw.multiline_text((title_x, title_y), wrapped_title, font=font_title, fill=(255, 255, 255), spacing=10)

    # 7️⃣ Tagline (centered)
    # Using textbbox is the modern way to measure single-line text in PIL
    tag_bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = (width - tag_w) // 2
    tag_y = title_y + title_h + 40
    draw.text((tag_x, tag_y), tagline, font=font_tagline, fill=(200, 210, 220))

    # 8️⃣ Footer Branding Bar
    draw.rectangle((0, height - 80, width, height), fill=(10, 10, 10)) # Darker, more solid bar
    footer = "govardhan.dev"
    
    foot_bbox = draw.textbbox((0, 0), footer, font=font_footer)
    foot_w = foot_bbox[2] - foot_bbox[0]
    foot_x = (width - foot_w) // 2
    
    # Calculate vertical center of the footer bar
    foot_y = height - 80 + (80 - (foot_bbox[3] - foot_bbox[1])) // 2 
    draw.text((foot_x, foot_y), footer, font=font_footer, fill=(255, 255, 255))

    # 9️⃣ Output
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer