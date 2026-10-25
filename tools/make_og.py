# Image de partage (Discord, X, WhatsApp…) : public/assets/og.png, 1200 x 630, avec l'icône de chaque appli du catalogue.
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "public" / "assets"
W, H = 1200, 630
CATALOG = ROOT.parent / "Seventh OS" / "apps.json"
APPS = [a["id"] for a in json.loads(CATALOG.read_text("utf-8"))["apps"]] if CATALOG.exists() else     sorted(p.stem for p in (A / "icons").glob("se7en-*.png"))


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

# rangée d'icônes : 72 px, plus petites si le catalogue grandit (tout tient entre les marges)
shown = [a for a in APPS if (A / "icons" / f"{a}.png").exists()]
gap = 16
size = int(min(72, (W - 2 * 84 - gap * (len(shown) - 1)) / max(1, len(shown))))
x = 84
for app in shown:
    img.alpha_composite(rounded(Image.open(A / "icons" / f"{app}.png"), size, int(size / 4)), (x, 510 + (72 - size) // 2))
    x += size + gap

img.convert("RGB").save(A / "og.png", optimize=True)
print("ok", A / "og.png")
