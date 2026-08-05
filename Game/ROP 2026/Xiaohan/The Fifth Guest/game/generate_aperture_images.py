"""
Generate aperture-variant images for The Fifth Guest crime-scene locations.

Usage (from The Fifth Guest/):
  python game/_gen_aperture_variants.py
  # or this file after editing LOCATIONS:
  python game/generate_aperture_images.py

Output: game/images/camera/{location}-{aperture}.png
"""

from PIL import Image, ImageFilter, ImageDraw
import os

LOCATIONS = {
    "shoeprint": "door-view-bg.png",
    "shoeprint_scale": "door-view-bg.png",
    "blood_splatter": "study-bg.png",
    "lamp_far": "study-bg.png",
    "lamp_close": "lamp-bg.png",
    "blood_pool": "blood-pool-bg.png",
    "fingerprint": "fingerprint-zoom-bg.png",
}

APERTURE_BLUR = {
    "5.6": 18,
    "8": 10,
    "11": 4,
    "16": 0,
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCENE_DIR = os.path.join(BASE_DIR, "images", "Scenes")
OUTPUT_DIR = os.path.join(BASE_DIR, "images", "camera")


def make_radial_mask(size):
    w, h = size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    cx, cy = w // 2, h // 2
    steps = 40
    for i in range(steps, 0, -1):
        t = i / float(steps)
        val = int(255 * max(0.0, 1.0 - (1.0 - t) * 1.6))
        rx = int(cx * t)
        ry = int(cy * t)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=val)
    return mask


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for location, base_filename in LOCATIONS.items():
        base_path = os.path.join(SCENE_DIR, base_filename)
        if not os.path.exists(base_path):
            print("[SKIP] missing", base_path)
            continue
        base = Image.open(base_path).convert("RGBA")
        mask = make_radial_mask(base.size)
        print("[OK] Processing {!r}...".format(location))
        for ap, blur in APERTURE_BLUR.items():
            if blur == 0:
                result = base.copy()
            else:
                blurred = base.filter(ImageFilter.GaussianBlur(radius=blur))
                result = Image.composite(base, blurred, mask)
            dest = os.path.join(OUTPUT_DIR, "{}-{}.png".format(location, ap))
            result.save(dest, "PNG")
            print("     -> {} (blur={})".format(os.path.basename(dest), blur))
    print("Done. Images in", OUTPUT_DIR)


if __name__ == "__main__":
    main()
