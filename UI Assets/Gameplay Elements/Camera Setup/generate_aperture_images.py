"""
Generate aperture-variant images with depth-of-field effect.

For each injury location:
  - Reads a base image and a subject mask
  - Applies varying Gaussian blur to the background based on aperture
  - Subject (masked area) stays sharp

Usage:
  1. Place base images in: game/images/injury_screens/{location}.png
  2. Create mask images in: game/images/injury_screens/{location}_mask.png
     - White (255) = subject (stays sharp)
     - Black (0) = background (gets blurred)
     - Gray = partial blend
  3. Run: python generate_aperture_images.py

Output: game/images/camera/{location}-{aperture}.png
"""

from PIL import Image, ImageFilter
import os

# Configuration
LOCATIONS = {
    "knuckle1": "knuckle1.png",
    "knuckle2": "knuckle2.png",
    "hematoma": "hematoma.png",
    "laceration": "laceration.png",
    "tattoo": "tattoo_close_base.png",
}

# Aperture -> blur radius (higher = more blur = shallower depth of field)
APERTURE_BLUR = {
    "5.6": 50,   # wide open, very blurry background
    "8":   30,   # moderate blur
    "11":  12,   # slight blur
    "16":  0,    # fully stopped down, everything sharp
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INJURY_DIR = os.path.join(BASE_DIR, "game", "images", "injury_screens")
OUTPUT_DIR = os.path.join(BASE_DIR, "game", "images", "camera")


def generate_dof_image(base_img, mask_img, blur_radius):
    """
    Apply depth-of-field effect.
    - base_img: original sharp image (RGBA or RGB)
    - mask_img: grayscale mask (white=subject, black=background)
    - blur_radius: how much to blur the background
    """
    if blur_radius == 0:
        return base_img.copy()

    # Ensure both are same size
    if mask_img.size != base_img.size:
        mask_img = mask_img.resize(base_img.size, Image.LANCZOS)

    # Convert mask to grayscale 'L' mode
    if mask_img.mode != 'L':
        mask_img = mask_img.convert('L')

    # Create blurred version of the base image
    blurred = base_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # Composite: where mask is white -> sharp, where black -> blurred
    result = Image.composite(base_img, blurred, mask_img)

    return result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for location, base_filename in LOCATIONS.items():
        base_path = os.path.join(INJURY_DIR, base_filename)

        # Mask filename: same name but with _mask suffix
        name_no_ext = os.path.splitext(base_filename)[0]
        mask_path = os.path.join(INJURY_DIR, "{}_mask.png".format(name_no_ext))

        if not os.path.exists(base_path):
            print("[SKIP] Base image not found: {}".format(base_path))
            continue

        # Also check for cutout from remove.bg (transparent background PNG)
        cutout_path = os.path.join(INJURY_DIR, "{}_cutout.png".format(name_no_ext))

        base_img = Image.open(base_path).convert("RGBA")

        if os.path.exists(mask_path):
            # Priority 1: Use hand-made mask
            print("[OK] Using mask: {}".format(os.path.basename(mask_path)))
            mask_img = Image.open(mask_path).convert("L")
        elif os.path.exists(cutout_path):
            # Priority 2: Convert remove.bg cutout (transparent bg) to mask
            print("[OK] Converting cutout to mask: {}".format(os.path.basename(cutout_path)))
            mask_img = cutout_to_mask(cutout_path, base_img.size)
        else:
            # Priority 3: Auto-generate radial gradient mask
            print("[WARN] No mask or cutout found for '{}', using radial fallback".format(location))
            print("       Expected mask: {}".format(mask_path))
            print("       Or cutout:     {}".format(cutout_path))
            mask_img = create_radial_mask(base_img.size)

        print("[OK] Processing '{}'...".format(location))

        for aperture, blur_radius in APERTURE_BLUR.items():
            result = generate_dof_image(base_img, mask_img, blur_radius)

            output_path = os.path.join(OUTPUT_DIR, "{}-{}.png".format(location, aperture))
            result.save(output_path)
            print("     -> {}-{}.png (blur={})".format(location, aperture, blur_radius))

    print("\nDone! Generated images in: {}".format(OUTPUT_DIR))


def cutout_to_mask(cutout_path, target_size):
    """
    Convert a remove.bg cutout (PNG with transparent background) to a grayscale mask.
    White = subject (where alpha > 0), Black = background (where transparent).
    Adds slight feathering for smooth edges.
    """
    cutout = Image.open(cutout_path).convert("RGBA")

    # Resize to match base image if needed
    if cutout.size != target_size:
        cutout = cutout.resize(target_size, Image.LANCZOS)

    # Extract alpha channel as mask
    alpha = cutout.split()[3]  # A channel

    # Slight feather: blur the mask edges for smooth transition
    mask = alpha.filter(ImageFilter.GaussianBlur(radius=3))

    return mask


def create_radial_mask(size, center_ratio=0.15, fade_ratio=0.35):
    """
    Fallback: create a radial gradient mask with tighter sharp center.
    - center_ratio: fraction of max_dist that is fully sharp (small = less sharp area)
    - fade_ratio: fraction of max_dist where transition happens
    Beyond fade_ratio -> fully blurred (black)
    """
    import numpy as np
    w, h = size
    cx, cy = w / 2.0, h / 2.0
    max_dist = (cx ** 2 + cy ** 2) ** 0.5

    # Create coordinate grids
    y_coords, x_coords = np.mgrid[0:h, 0:w]
    dist = np.sqrt((x_coords - cx) ** 2 + (y_coords - cy) ** 2)

    sharp_dist = max_dist * center_ratio
    fade_dist = max_dist * fade_ratio

    # Build mask: 255 in center, fade to 0
    mask_array = np.zeros((h, w), dtype=np.uint8)

    # Fully sharp center
    mask_array[dist <= sharp_dist] = 255

    # Transition zone
    transition = (dist > sharp_dist) & (dist <= fade_dist)
    if np.any(transition):
        fade = 1.0 - (dist[transition] - sharp_dist) / (fade_dist - sharp_dist)
        mask_array[transition] = (fade * 255).astype(np.uint8)

    # Beyond fade_dist -> 0 (fully blurred)

    return Image.fromarray(mask_array, mode='L')


if __name__ == "__main__":
    main()
