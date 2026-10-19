"""render.py: draw identity elements as PNGs and an animation over growing N (frames -> ffmpeg).
usage: python render.py still N        -> out/identity_N.png (from out/identity_N.npy)
       python render.py frames A B STEP -> out/frames/fNNN.png, identity for N = A..B, each scaled to 1024 px
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from identity import identity

PAL = np.array([[16, 24, 40],      # 0 grains: deep ink
                [44, 110, 125],    # 1: teal
                [214, 168, 92],    # 2: sand
                [244, 238, 224]],  # 3: paper
               np.uint8)

def img(e, size=1024):
    im = Image.fromarray(PAL[e.astype(int)])
    return im.resize((size, size), Image.NEAREST)

def label(im, text):
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 26)
    except OSError:
        f = ImageFont.load_default()
    d.rectangle([0, im.height - 44, im.width, im.height], fill=(16, 24, 40))
    d.text((14, im.height - 38), text, fill=(244, 238, 224), font=f)
    return im

if __name__ == "__main__":
    os.makedirs("out/frames", exist_ok=True)
    if sys.argv[1] == "still":
        n = int(sys.argv[2])
        img(np.load(f"out/identity_{n}.npy"), max(1024, n * 2)).save(f"out/identity_{n}.png")
    else:
        a, b, step = map(int, sys.argv[2:5])
        for k, n in enumerate(range(a, b + 1, step)):
            e, _ = identity(n)
            label(img(e), f"sandpile identity, {n}x{n} grid").save(f"out/frames/f{k:03d}.png")
            print(n, flush=True)
