from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import random
import io
import os
from datetime import datetime

# ... (Font setup remains the same) ...
# ASSUMPTION: Font is placed at backend/core/fonts/default.ttf
FONT_NAME = "arial.ttf" 
FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
BUNDLED_FONT_PATH = os.path.join(FONT_DIR, 'default.ttf')

def generate_project_og(title, tagline):
    width, height = 1200, 630
    bg_color = (15, 23, 42) 

    # 1️⃣ Canvas
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # 2️⃣ Soft Gradient Overlay
    for i in range(height):
        shade = int(15 + (i / height) * 25)
        draw.line([(0, i), (width, i)], fill=(shade, shade, shade))
    
    # 3️⃣ Random Glow Blobs
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

    # 4️⃣ Fonts
    def load_font(size):
        try:
            if os.path.exists(BUNDLED_FONT_PATH):
                 return ImageFont.truetype(BUNDLED_FONT_PATH, size)
            return ImageFont.truetype(FONT_NAME, size)
        except IOError:
            return ImageFont.load_default(size=size)
            
    font_title = load_font(70)
    font_tagline = load_font(40)
    font_footer = load_font(32)

    # 5️⃣ Auto-wrap title
    wrapped_title = textwrap.fill(title.upper(), width=20)
    
    # --- Title Positioning and Neon Glow ---
    
    # CRITICAL FIX FOR PILLOW 12.0.0: Replaced multiline_textsize with multiline_textbbox
    bbox = draw.multiline_textbbox((0, 0), wrapped_title, font=font_title, spacing=10)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    
    title_x = (width - title_w) // 2
    title_y = height // 2 - 100 

    # 6️⃣ Neon Glow Effect
    glow_color = (56, 189, 248) 
    
    glow_layer = Image.new("RGB", (width, height), bg_color)
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.multiline_text((title_x, title_y), wrapped_title, font=font_title, fill=glow_color, spacing=10)

    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(14)) 
    img = Image.blend(img, glow_layer, 0.60) 

    # 6.3 Draw Title
    draw.multiline_text((title_x, title_y), wrapped_title, font=font_title, fill=(255, 255, 255), spacing=10)

    # 7️⃣ Tagline
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