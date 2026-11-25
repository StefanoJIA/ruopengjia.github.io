"""Build the Chinese HTML pages from English pages and an explicit translation map."""

import html
import json
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TRANSLATIONS = json.loads((ROOT / "content/zh.json").read_text(encoding="utf-8"))
PAGES = sorted(DOCS.glob("*.html")) + sorted((DOCS / "gallery").rglob("*.html"))
ROUTES = {page.relative_to(DOCS).as_posix() for page in PAGES}
UNCHANGED = {
    "Ruopeng Jia", "GitHub", "LinkedIn", "EN", "HTML5 UP", "CC BY 4.0",
    "jia.ruop@northeastern.edu", "AMPLFI", "CUORE / FPGA", "cm",
    "2.78 µs", "1.54 µs", "1.50 µs",
}


class ChinesePage(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.target = "zh/" + source
        self.output = []
        self.missing = set()

    def translate(self, value):
        key = " ".join(value.split())
        if not key:
            return value
        if key in TRANSLATIONS:
            return value[:len(value) - len(value.lstrip())] + TRANSLATIONS[key] + value[len(value.rstrip()):]
        if re.search("[A-Za-z]", key) and key not in UNCHANGED:
            self.missing.add(key)
        return value

    def local_url(self, value):
        url = urlsplit(value)
        if url.scheme or url.netloc or not url.path:
            return value
        resolved = posixpath.normpath(
            posixpath.join(posixpath.dirname(self.source), url.path)
        ) if not url.path.startswith("/") else url.path.lstrip("/")
        target = "zh/" + resolved if resolved in ROUTES else resolved
        path = posixpath.relpath(target, posixpath.dirname(self.target) or ".")
        return urlunsplit(("", "", path, url.query, url.fragment))

    def handle_decl(self, decl):
        self.output.append("<!" + decl + ">")

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        rendered = []
        for key, value in attrs:
            if tag == "html" and key == "lang":
                value = "zh-CN"
            elif key in ("href", "src"):
                if values.get("data-language"):
                    target = self.source if values["data-language"] == "en" else self.target
                    value = posixpath.relpath(target, posixpath.dirname(self.target) or ".")
                elif tag == "link" and values.get("rel") == "canonical":
                    value = "https://ruopengjia.com/" + self.target
                elif not (tag == "link" and values.get("rel") == "alternate"):
                    value = self.local_url(value)
            elif key in ("alt", "title", "aria-label") and value:
                value = self.translate(value)
            elif tag == "meta" and values.get("name") == "description" and key == "content":
                value = self.translate(value)
            if values.get("data-language") and key == "aria-current":
                continue
            rendered.append(key if value is None else key + '="' + html.escape(value, quote=True) + '"')
        if values.get("data-language") == "zh":
            rendered.append('aria-current="page"')
        self.output.append("<" + tag + (" " if rendered else "") + " ".join(rendered) + ">")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.output[-1] = self.output[-1][:-1] + " />"

    def handle_endtag(self, tag):
        self.output.append("</" + tag + ">")

    def handle_data(self, data):
        self.output.append(html.escape(self.translate(data), quote=False))

    def handle_comment(self, data):
        self.output.append("<!--" + data + "-->")


def build():
    pending = []
    missing = set()
    for page in PAGES:
        parser = ChinesePage(page.relative_to(DOCS).as_posix())
        parser.feed(page.read_text(encoding="utf-8-sig"))
        pending.append((DOCS / parser.target, "".join(parser.output)))
        missing.update(parser.missing)
    if missing:
        raise ValueError("Missing Chinese translations:\n" + "\n".join(sorted(missing)))
    for target, content in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    print(f"Built {len(pending)} Chinese pages with no missing text translations.")


if __name__ == "__main__":
    build()
