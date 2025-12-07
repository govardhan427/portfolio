from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random
import io
import os
from datetime import datetime

# --- CRITICAL FONT FIX ---
# 1. Define the relative path to the bundled font file (Recommended)
# ASSUMPTION: Font is placed at backend/core/fonts/default.ttf
FONT_NAME = "arial.ttf" # Fallback system name
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
BUNDLED_FONT_PATH = os.path.join(FONT_DIR, 'default.ttf')

def generate_project_og(title, tagline):
    width, height = 1200, 630
    bg_color = (15, 23, 42)  # Dark navy

    # 1️⃣ Canvas
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 2️⃣ Soft Gradient Overlay (Optimized)
    for i in range(height):
        shade = int(15 + (i / height) * 25)
        draw.line([(0, i), (width, i)], fill=(shade, shade, shade))
    
    # 3️⃣ Random Glow Blobs (Cleaned up blending)
    for _ in range(3): 
        x = random.randint(-200, width)
        y = random.randint(-200, height)
        r = random.randint(200, 400)

        blob = Image.new("RGB", (width, height), bg_color) 
        b_draw = ImageDraw.Draw(blob)
        b_draw.ellipse((x, y, x + r, y + r), fill=(56, 189, 248)) 
        
        blob = blob.filter(ImageFilter.GaussianBlur(radius=160)) 
        img = Image.blend(img, blob, alpha=0.15) 

    draw = ImageDraw.Draw(img)

    # 4️⃣ Fonts (Robust Loading Function)
    def load_font(size):
        try:
            # Attempt 1: Load bundled font path (most reliable on cloud)
            if os.path.exists(BUNDLED_FONT_PATH):
                 return ImageFont.truetype(BUNDLED_FONT_PATH, size)
            
            # Attempt 2: Fallback to system font (arial.ttf)
            return ImageFont.truetype(FONT_NAME, size)
            
        except IOError as e:
            # Final Fallback: Load PIL's default, generic font
            return ImageFont.load_default(size=size)
            
    font_title = load_font(70)
    font_tagline = load_font(40)
    font_footer = load_font(32)

    # 5️⃣ Auto-wrap title
    wrapped_title = textwrap.fill(title.upper(), width=20)
    
    # --- Title Positioning and Neon Glow ---
    # Using the deprecated multiline_textsize, which is functional but requires care
    title_w, title_h = draw.multiline_textsize(wrapped_title, font=font_title, spacing=10)
    title_x = (width - title_w) // 2
    title_y = height // 2 - 100 

    # 6️⃣ Neon Glow Effect
    glow_color = (56, 189, 248) 
    
    glow_layer = Image.new("RGB", (width, height), bg_color)
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.multiline_text((title_x, title_y), wrapped_title, font=font_title, fill=glow_color, spacing=10)

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(14)) 
    img = Image.blend(img, glow_layer, 0.60) 

    # 6.3 Draw Title (clean text)
    draw.multiline_text((title_x, title_y), wrapped_title, font=font_title, fill=(255, 255, 255), spacing=10)

    # 7️⃣ Tagline (centered)
    tag_bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
    tag_w = tag_bbox[2] - tag_bbox[0]
    tag_x = (width - tag_w) // 2
    tag_y = title_y + title_h + 40
    draw.text((tag_x, tag_y), tagline, font=font_tagline, fill=(200, 210, 220))

    # 8️⃣ Footer Branding Bar
    draw.rectangle((0, height - 80, width, height), fill=(10, 10, 10)) 
    footer = "govardhan.dev"
    
    foot_bbox = draw.textbbox((0, 0), footer, font=font_footer)
    foot_w = foot_bbox[2] - foot_bbox[0]
    foot_x = (width - foot_w) // 2
    
    foot_y = height - 80 + (80 - (foot_bbox[3] - foot_bbox[1])) // 2 
    draw.text((foot_x, foot_y), footer, font=font_footer, fill=(255, 255, 255))

    # 9️⃣ Output
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer