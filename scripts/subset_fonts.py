"""Refresh local WOFF2 fonts. Requires fonttools[woff] and brotli."""

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlopen

from bs4 import BeautifulSoup
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "docs/assets/fonts"
SOURCE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONTS = [
    ("inter", "Inter%5Bopsz%2Cwght%5D.ttf", "inter-latin", 14),
    ("sourceserif4", "SourceSerif4%5Bopsz%2Cwght%5D.ttf", "source-serif-latin", 36),
    ("sourceserif4", "SourceSerif4-Italic%5Bopsz%2Cwght%5D.ttf", "source-serif-italic-latin", 36),
    ("notosanssc", "NotoSansSC%5Bwght%5D.ttf", "noto-sans-sc-site", None),
    ("notoserifsc", "NotoSerifSC%5Bwght%5D.ttf", "noto-serif-sc-headings", None),
]


def build():
    DEST.mkdir(parents=True, exist_ok=True)
    translations = json.loads((ROOT / "content/zh.json").read_text(encoding="utf-8"))
    chinese = "".join(translations.values())
    headings = ""
    for page in (ROOT / "docs/zh").rglob("*.html"):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        headings += "".join(e.get_text() for e in soup.select("h1,h2,h3,.invitation-title"))
    latin = "".join(chr(i) for i in range(32, 592)) + "–—‘’“”•…→↗↓×µ′"

    def make_font(item):
        family, filename, name, optical_size = item
        with TemporaryDirectory() as directory:
            source = Path(directory) / "font.ttf"
            source.write_bytes(urlopen(SOURCE + family + "/" + filename, timeout=60).read())
            font = TTFont(source)
            if optical_size is not None:
                instantiateVariableFont(font, {"opsz": optical_size}, inplace=True)
            options = subset.Options()
            options.flavor = "woff2"
            subsetter = subset.Subsetter(options=options)
            text = headings if "headings" in name else chinese if "-sc-" in name else latin
            subsetter.populate(text=text + latin)
            subsetter.subset(font)
            font.flavor = "woff2"
            font.save(DEST / (name + ".woff2"))
        print(name, (DEST / (name + ".woff2")).stat().st_size, flush=True)

    with ThreadPoolExecutor(max_workers=5) as pool:
        list(pool.map(make_font, FONTS))
    for family in sorted({item[0] for item in FONTS}):
        license_text = urlopen(SOURCE + family + "/OFL.txt", timeout=30).read().decode("utf-8")
        (DEST / (family + "-OFL.txt")).write_text(
            "\n".join(line.rstrip() for line in license_text.splitlines()) + "\n", encoding="utf-8"
        )


if __name__ == "__main__":
    build()
