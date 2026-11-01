"""
Prepare a portrait photo for clean ASCII conversion:
  1. crop to the subject bounding box so the portrait fills the frame
  2. remove the background (rembg with u2net_human_seg) so the subject is isolated
  3. boost LOCAL contrast (CLAHE) so a flatly-lit face gains highlights and
     shadows -- this is what turns a dark blob into a recognizable face
  4. composite the subject onto pure white so the background reads as blank
     (white -> spaces in the ascii ramp)

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
"""
import os
import sys

import cv2
import numpy as np
from PIL import Image
import rembg

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "photo.jpg")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

# 1. open and crop to portrait area
raw = Image.open(INP)
w, h = raw.size

# Focus on upper body / face: Y ~ 240 to 770 for a ~466x1024 photo
if h > 800 and w < 600:
    crop_box = (0, 240, w, 770)
    raw = raw.crop(crop_box)

# 2. cut out the subject using human segmentation session
session = rembg.new_session("u2net_human_seg")
cut = rembg.remove(raw.convert("RGBA"), session=session)
rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])                 # 0 = background

# 3. local-contrast the luminance (CLAHE)
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
gray = clahe.apply(gray)

# a touch of global lift so the face sits in the sparse end of the ramp
gray = cv2.convertScaleAbs(gray, alpha=1.05, beta=18)

# 4. paste onto white using the alpha mask (feathered a hair to avoid a halo)
mask = (alpha.astype(np.float32) / 255.0)
mask = cv2.GaussianBlur(mask, (0, 0), 1.0)
out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out, mode="L").save(OUT)
print("wrote", OUT, out.shape)
