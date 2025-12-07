from PIL import Image
import io

def encode_text_into_image(image_file, secret_text):
    """
    Hides secret text inside the red channel of an image.
    This is a simplified steganography logic for the portfolio flex.
    """
    # Open image
    img = Image.open(image_file)
    img = img.convert('RGB')
    encoded = img.copy()
    
    # Convert text to binary
    binary_secret = ''.join(format(ord(i), '08b') for i in secret_text)
    data_len = len(binary_secret)
    
    pixels = encoded.load()
    width, height = img.size
    
    idx = 0
    for y in range(height):
        for x in range(width):
            if idx < data_len:
                r, g, b = pixels[x, y]
                
                # Modify the Least Significant Bit of the Red channel
                # If bit is 1, make Red odd. If 0, make Red even.
                new_r = r
                if binary_secret[idx] == '1':
                    new_r = r | 1 # Force to odd
                else:
                    new_r = r & ~1 # Force to even
                
                pixels[x, y] = (new_r, g, b)
                idx += 1
            else:
                break
    
    # Save to memory
    output = io.BytesIO()
    encoded.save(output, format='PNG') # PNG is lossless (required for stego)
    output.seek(0)
    return output