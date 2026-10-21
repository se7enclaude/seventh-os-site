# Image de partage (Discord, X, WhatsApp…) : public/assets/og.png, 1200 x 630.
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "public" / "assets"
W, H = 1200, 630
APPS = ["se7en-voice", "se7en-clip", "se7en-download", "se7en-dualsense", "se7en-autoclick", "se7en-vision", "se7en-ia"]


def glow(img, xy, r, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse((x - r, y - r, x + r, y + r), fill=color + (alpha,))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(r * 0.55)))


def rounded(im, size, radius):
    im = im.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius, fill=255)
    im.putalpha(mask)
    return im


img = Image.new("RGBA", (W, H), (11, 13, 14, 255))
glow(img, (120, 160), 380, (74, 120, 128), 150)
glow(img, (1050, 40), 330, (233, 161, 154), 90)
glow(img, (1100, 640), 420, (39, 80, 90), 170)

d = ImageDraw.Draw(img)
anton = lambda s: ImageFont.truetype(str(A / "fonts" / "Anton-Regular.ttf"), s)
manrope = ImageFont.truetype(str(A / "fonts" / "Manrope-Variable.ttf"), 40)
try:
    manrope.set_variation_by_axes([800])
except Exception:
    pass

img.alpha_composite(rounded(Image.open(A / "icons" / "seventh-os.png"), 132, 30), (80, 84))
big = anton(150)
d.text((80, 236), "SEVENTH", font=big, fill="white")
w = d.textlength("SEVENTH ", font=big)
d.text((80 + w, 236), "OS", font=big, fill=(241, 185, 178))
d.text((84, 430), "Tous tes logiciels se7en. Une seule appli.", font=manrope, fill=(255, 255, 255, 220))

x = 84
for app in APPS:
    p = A / "icons" / f"{app}.png"
    if p.exists():
        img.alpha_composite(rounded(Image.open(p), 72, 18), (x, 510))
        x += 88

img.convert("RGB").save(A / "og.png", optimize=True)
print("ok", A / "og.png")
