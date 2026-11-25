import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "docs"


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.references = []
        self.language_links = {}
        self.language = None
        self.h1_count = 0
        self.feed(path.read_text(encoding="utf-8-sig"))

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "html":
            self.language = values.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if "id" in values:
            self.ids.append(values["id"])
        for key in ("href", "src"):
            if values.get(key):
                self.references.append(values[key])
        if values.get("data-language"):
            self.language_links[values["data-language"]] = values


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = (
            sorted(ROOT.glob("*.html"))
            + sorted((ROOT / "gallery").rglob("*.html"))
            + sorted((ROOT / "zh").rglob("*.html"))
        )
        cls.documents = {page.resolve(): Document(page) for page in cls.pages}

    def resolve(self, page, href):
        url = urlsplit(href)
        path = unquote(url.path)
        target = ROOT / path.lstrip("/") if path.startswith("/") else page.parent / path
        return target.resolve() if path else page.resolve()

    def test_local_routes_assets_and_fragments(self):
        for page, doc in self.documents.items():
            self.assertEqual(doc.h1_count, 1, page)
            self.assertFalse([key for key, count in Counter(doc.ids).items() if count > 1], page)
            for href in doc.references:
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                with self.subTest(page=page.name, href=href):
                    target = self.resolve(page, href)
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.is_file(), target)
                    if url.fragment and target in self.documents:
                        self.assertIn(unquote(url.fragment), self.documents[target].ids)

    def test_language_pairs(self):
        self.assertEqual(len(self.pages), 22)
        for page, doc in self.documents.items():
            relative = page.relative_to(ROOT.resolve())
            chinese = relative.parts[0] == "zh"
            original = Path(*relative.parts[1:]) if chinese else relative
            self.assertEqual(doc.language, "zh-CN" if chinese else "en")
            self.assertEqual(set(doc.language_links), {"en", "zh"})
            for lang, attributes in doc.language_links.items():
                target = ROOT / ("zh" if lang == "zh" else "") / original
                self.assertEqual(self.resolve(page, attributes["href"]), target.resolve())
                self.assertEqual(attributes.get("aria-current") == "page", lang == ("zh" if chinese else "en"))

    def test_cv_is_linked_in_both_profile_editions(self):
        cv = ROOT / "files/ruopeng-jia-academic-cv.pdf"
        self.assertTrue(cv.read_bytes().startswith(b"%PDF"))
        for relative in ("index.html", "about.html", "zh/index.html", "zh/about.html"):
            page = (ROOT / relative).resolve()
            targets = {
                self.resolve(page, href)
                for href in self.documents[page].references
                if not urlsplit(href).scheme
            }
            self.assertIn(cv.resolve(), targets, relative)

    def test_teaching_is_reachable_from_every_page(self):
        for page, doc in self.documents.items():
            chinese = page.relative_to(ROOT.resolve()).parts[0] == "zh"
            target = (ROOT / ("zh" if chinese else "") / "teaching.html").resolve()
            links = {self.resolve(page, href) for href in doc.references if not urlsplit(href).scheme}
            self.assertIn(target, links, page)


if __name__ == "__main__":
    unittest.main()
