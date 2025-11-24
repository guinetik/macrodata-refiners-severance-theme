#!/usr/bin/env python3
"""
Advanced color extraction focusing on specific regions and brightness ranges
"""
from PIL import Image
import sys
from collections import Counter

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code"""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def get_brightness(rgb):
    """Calculate perceived brightness"""
    r, g, b = rgb
    return (0.299 * r + 0.587 * g + 0.114 * b)

def extract_palette_advanced(image_path):
    """Extract colors from specific regions and brightness ranges"""
    img = Image.open(image_path)
    img = img.convert('RGB')

    width, height = img.size

    # Sample different regions
    regions = {
        'background': (0, 0, width, height // 3),  # Top third - dark background
        'walls': (0, height // 3, width // 4, 2 * height // 3),  # Left wall tiles
        'center': (width // 3, height // 3, 2 * width // 3, 2 * height // 3),  # Center area
        'desks': (width // 4, 2 * height // 3, 3 * width // 4, height),  # Bottom - desks
    }

    print("\n" + "=" * 70)
    print("COLOR PALETTE EXTRACTION - Macrodata Refiners Theme")
    print("=" * 70)

    for region_name, (x1, y1, x2, y2) in regions.items():
        region_img = img.crop((x1, y1, x2, y2))
        region_img = region_img.resize((100, 100))
        pixels = list(region_img.getdata())

        color_counter = Counter(pixels)
        common_colors = color_counter.most_common(10)

        print(f"\n{region_name.upper()} REGION:")
        print("-" * 70)

        for (r, g, b), count in common_colors[:5]:
            hex_color = rgb_to_hex((r, g, b))
            brightness = get_brightness((r, g, b))
            print(f"  {hex_color}  RGB({r:3d}, {g:3d}, {b:3d})  Brightness: {brightness:6.1f}")

    # Overall palette
    print("\n" + "=" * 70)
    print("OVERALL PALETTE BY BRIGHTNESS")
    print("=" * 70)

    img_small = img.resize((200, 200))
    all_pixels = list(img_small.getdata())
    color_counter = Counter(all_pixels)
    all_colors = color_counter.most_common(50)

    # Categorize by brightness
    very_dark = []  # 0-30
    dark = []       # 30-60
    mid_dark = []   # 60-100
    mid = []        # 100-150
    light = []      # 150+

    for (r, g, b), count in all_colors:
        brightness = get_brightness((r, g, b))
        hex_color = rgb_to_hex((r, g, b))

        if brightness < 30:
            very_dark.append((hex_color, (r, g, b), brightness, count))
        elif brightness < 60:
            dark.append((hex_color, (r, g, b), brightness, count))
        elif brightness < 100:
            mid_dark.append((hex_color, (r, g, b), brightness, count))
        elif brightness < 150:
            mid.append((hex_color, (r, g, b), brightness, count))
        else:
            light.append((hex_color, (r, g, b), brightness, count))

    print("\nVERY DARK (0-30) - Backgrounds:")
    for hex_color, rgb, brightness, count in very_dark[:8]:
        print(f"  {hex_color}  RGB{rgb}  B:{brightness:.1f}")

    print("\nDARK (30-60) - UI Elements:")
    for hex_color, rgb, brightness, count in dark[:8]:
        print(f"  {hex_color}  RGB{rgb}  B:{brightness:.1f}")

    print("\nMID-DARK (60-100) - Walls/Tiles:")
    for hex_color, rgb, brightness, count in mid_dark[:8]:
        print(f"  {hex_color}  RGB{rgb}  B:{brightness:.1f}")

    print("\nMID (100-150) - Accents:")
    for hex_color, rgb, brightness, count in mid[:8]:
        print(f"  {hex_color}  RGB{rgb}  B:{brightness:.1f}")

    print("\nLIGHT (150+) - Highlights:")
    for hex_color, rgb, brightness, count in light[:8]:
        print(f"  {hex_color}  RGB{rgb}  B:{brightness:.1f}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "reference-mdr.jpg"
    extract_palette_advanced(image_path)
