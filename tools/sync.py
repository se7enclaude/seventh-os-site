# Met le site à jour depuis le catalogue de Seventh OS (../Seventh OS/apps.json et ui/icons) :
#   - icônes copiées dans public/assets/icons ;
#   - copie de secours des fiches (FALLBACK dans public/app.js), dans l'ordre du catalogue ;
#   - nombre d'applis écrit dans la page (avant que le JavaScript ne le relise) ;
#   - image de partage refaite avec toutes les icônes (tools/make_og.py).
# La page relit déjà apps.json en direct : ce script sert à ce qui ne bouge pas tout seul.
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = ROOT.parent / "Seventh OS"
PUB = ROOT / "public"


def js(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def main() -> int:
    apps = json.loads((HUB / "apps.json").read_text("utf-8"))["apps"]
    icons = PUB / "assets" / "icons"
    copied = 0
    for f in (HUB / "ui" / "icons").glob("*.png"):
        dst = icons / f.name
        if not dst.exists() or dst.read_bytes() != f.read_bytes():
            shutil.copy2(f, dst)
            copied += 1
    lines = ",\n".join(
        "  { id: %s, name: %s, subtitle: %s, accent: %s, tagline: %s }"
        % (js(a["id"]), js(a["name"]), js(a.get("subtitle", "")), js(a.get("accent", "#fff")), js(a.get("tagline", "")))
        for a in apps)
    app_js = PUB / "app.js"
    s = app_js.read_text("utf-8")
    s = re.sub(r"const FALLBACK = \[\n.*?\n\];", "const FALLBACK = [\n" + lines + ",\n];", s, count=1, flags=re.S)
    app_js.write_text(s, "utf-8", newline="\n")
    page = PUB / "index.html"
    h = page.read_text("utf-8")
    h = re.sub(r"(data-count>)\d+(<)", rf"\g<1>{len(apps)}\2", h)
    # adresse complète et changeante : Discord, X… gardent l'aperçu en cache tant que l'adresse de l'image ne change pas
    ver = "-".join(a["id"].removeprefix("se7en-")[:3] for a in apps)
    h = re.sub(r'(<meta property="og:image" content=")[^"]*(")', rf"\g<1>https://seventh-os.pages.dev/assets/og.png?v={ver}\2", h)
    page.write_text(h, "utf-8", newline="\n")
    subprocess.run([sys.executable, str(ROOT / "tools" / "make_og.py")], check=True)
    print(f"{len(apps)} applis · {copied} icône(s) mise(s) à jour · image de partage refaite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
