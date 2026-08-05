import os
from PIL import Image

def resize_images(directory, size=(32, 32)):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            filepath = os.path.join(directory, filename)
            try:
                with Image.open(filepath) as img:
                    img = img.resize(size, Image.Resampling.LANCZOS)
                    img.save(filepath)
                print(f"Resized {filename} to {size[0]}x{size[1]}")
            except Exception as e:
                print(f"Failed to resize {filename}: {e}")

if __name__ == "__main__":
    cursors_dir = r"c:\Users\mary2\Forensics-Pursuit\Game\ROP 2026\Xiaohan\The Fifth Guest\game\images\cursors"
    resize_images(cursors_dir)
