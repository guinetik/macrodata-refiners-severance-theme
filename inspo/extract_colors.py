#!/usr/bin/env python3
"""
Extract dominant colors from reference images for theme generation
"""
from PIL import Image
import sys
from collections import Counter

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code"""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def extract_palette(image_path, num_colors=16):
    """Extract dominant colors from an image"""
    # Open and resize image for faster processing
    img = Image.open(image_path)
    img = img.convert('RGB')
    img = img.resize((150, 150))

    # Get all pixels
    pixels = list(img.getdata())

    # Count color frequency
    color_counter = Counter(pixels)

    # Get most common colors
    common_colors = color_counter.most_common(num_colors)

    return common_colors

def analyze_image(image_path):
    """Analyze image and categorize colors"""
    print(f"\nAnalyzing: {image_path}")
    print("=" * 60)

    colors = extract_palette(image_path, 20)

    darks = []
    mids = []
    lights = []
    teals = []
    greens = []

    for (r, g, b), count in colors:
        hex_color = rgb_to_hex((r, g, b))
        brightness = (r + g + b) / 3

        # Categorize by brightness
        if brightness < 50:
            darks.append((hex_color, (r, g, b), count))
        elif brightness < 150:
            mids.append((hex_color, (r, g, b), count))
        else:
            lights.append((hex_color, (r, g, b), count))

        # Identify teals and greens (cyan/teal: high G and B, low R)
        if g > r and b > r and abs(g - b) < 50:
            teals.append((hex_color, (r, g, b), count))
        elif g > r and g > b:
            greens.append((hex_color, (r, g, b), count))

    print("\nDARK BACKGROUNDS (brightness < 50):")
    for hex_color, rgb, count in darks[:5]:
        print(f"  {hex_color}  RGB{rgb}  (count: {count})")

    print("\nMID TONES (50-150 brightness):")
    for hex_color, rgb, count in mids[:5]:
        print(f"  {hex_color}  RGB{rgb}  (count: {count})")

    print("\nTEAL/CYAN TONES:")
    for hex_color, rgb, count in teals[:5]:
        print(f"  {hex_color}  RGB{rgb}  (count: {count})")

    print("\nGREEN TONES:")
    for hex_color, rgb, count in greens[:5]:
        print(f"  {hex_color}  RGB{rgb}  (count: {count})")

    print("\nLIGHT TONES (brightness > 150):")
    for hex_color, rgb, count in lights[:5]:
        print(f"  {hex_color}  RGB{rgb}  (count: {count})")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "reference-mdr.jpg"
    analyze_image(image_path)
