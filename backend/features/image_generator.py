from PIL import Image, ImageDraw, ImageFont
import random
import io

def generate_project_og(title, tagline):
    """
    Generates a social media preview image dynamically.
    Creates a dark background with neon text.
    """
    # 1. Create Canvas (1200x630 is standard OG size)
    width, height = 1200, 630
    # Dark background color
    img = Image.new('RGB', (width, height), color=(15, 23, 42)) 
    draw = ImageDraw.Draw(img)

    # 2. Draw "Neon" Accents (Random circles)
    for _ in range(5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(50, 200)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(30, 41, 59), outline=None)

    # 3. Add Text
    # Try to load a font, otherwise use default
    try:
        # If you have a .ttf file, point to it here. 
        # For now, we use default to ensure it runs without errors.
        font_title = ImageFont.load_default()
        font_tag = ImageFont.load_default()
        # Scale logic would go here if we had a custom font file
    except:
        font_title = ImageFont.load_default()
    
    # Draw Title (Centered-ish)
    draw.text((100, 250), title.upper(), fill=(56, 189, 248), font=font_title) # Cyan color
    draw.text((100, 320), tagline, fill=(148, 163, 184), font=font_title) # Slate color
    draw.text((100, 500), "govardhan.dev", fill=(255, 255, 255), font=font_title)

    # 4. Save to Bytes
    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output