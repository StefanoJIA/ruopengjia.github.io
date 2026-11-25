# ruopengjia.github.io

Ruopeng Jia's personal website. The static site lives in `docs/`.

Preview the site from this checkout with:

```powershell
python -m http.server 8772 --bind 127.0.0.1 --directory docs
```

Open http://127.0.0.1:8772/ to review the homepage, detailed research projects,
and academic background. Research, Writing, About, Teaching, News, Gallery, and
Contact are all in the main navigation.

English pages live at the domain root; their complete Chinese counterparts
live under `docs/zh/`. The language control links to the same page and preserves
its current section. Shared images, scripts, and PDFs are served from one copy.

After editing English HTML, update the corresponding entries in
`content/zh.json`, then run:

```powershell
python scripts/build_zh.py
python -m unittest discover -s tests -v
```

The builder uses Python's standard library and rejects missing translations.
Commit the generated Chinese HTML alongside English changes so the existing
GitHub Pages deployment can publish both without a new build service.

The profile and homepage link to the author's selected two-page academic
English CV, a byte-preserved copy under `docs/files/`. News dates describe
the underlying milestones rather than when their website entries were added.
Reading questions and listening prompts are editorial notes, not quotations.

The three calligraphy photographs under `docs/images/gallery/` were retrieved
from the author's [public Imgur album](https://imgur.com/gallery/SfmdMg0), linked
from his own public LinkedIn post. The album is dated March 29, 2023. This date
belongs to that album; the separate November 2024 update remains a later sharing
milestone. Images retain the complete photographed frame. Gallery captions and
the March 2023 News entry are available in both languages.

Typography uses local WOFF2 subsets of Inter, Source Serif 4, Noto Sans SC, and
Noto Serif SC from [Google Fonts](https://github.com/google/fonts). Their SIL
Open Font License notices live alongside them in `docs/assets/fonts/`.
The browser loads them from the site, with `font-display: swap` and system
fallbacks. Chinese body and heading subsets cover the site's current text.
After adding Chinese characters, regenerate Chinese pages first, then refresh
the subsets with `python scripts/subset_fonts.py` (requires `fonttools[woff]`,
`brotli`, and `beautifulsoup4`). English HTML remains the source for both editions.

The personal mark in `docs/images/brand/ruopeng-jia-mark.svg` is an original
single-color abstract RJ mark drawn as two open paths with rounded turns and a consistent stroke.
The upper return loop and diagonal lower return retain the R/J gestures; a small
negative-space gap separates the paths, suggesting coupled optical waveguides.
It has no enclosing badge, decorative ring, or accent dot. Social icons were extracted from
the site's bundled Font Awesome Free font; icons are licensed
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) by
[Font Awesome](https://fontawesome.com/).

Content is maintained directly in the HTML files. Keep the home summaries,
research details, and background timeline consistent when adding results.
Styles are shared by all eleven English pages and their Chinese counterparts; bump the stylesheet query version
across the main pages and gallery archives when changing it.

The thesis PDF in `docs/files/` is the author's original 2024 copy.
Its title page and Figure 1.2 are reproduced under `docs/images/research/`.
The retained SVGs are explanatory illustrations. The photon path and the
detector pulse in them are schematic. The waveform PNG is the author's
visualization of the [public CUORE dataset](https://doi.org/10.5281/zenodo.20721645)
by Vivek Sharma and Krystal Alfonso, licensed CC BY 4.0. Its preprocessing
comparison shows 100 Hz; the deployed classifier uses 25 Hz. Preserve this
distinction and the visible attribution.

FPGA core timings describe specific reuse-factor designs. The 1,350-event
numerical check compares physical score codes with the HLS C reference.
Core timing, full-system latency, observation time, and generalization are
separate claims; the current work does not establish full-system acceleration.

GitHub Pages publishes `main:/docs` at `https://ruopengjia.com`. Keep
`docs/CNAME` and the Pages custom domain in sync. In Alibaba Cloud DNS,
the apex uses the [GitHub Pages A records](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#dns-records-for-your-custom-domain);
`www` uses a CNAME to `stefanojia.github.io` so Pages can redirect to the apex.

The homepage contact section (`#contact`) is the entry point for arranging
research meetings. When Northstar is ready, add a booking link or a read-only
feed of explicitly published meeting slots there. Keep the workbench and its
calendar APIs behind authentication. The public feed should expose only slot
start and end times with time zones, without event details or credentials.
Keep email available when there are no slots or the service is unavailable.

The teaching page (`teaching.html`, with its Chinese counterpart) summarizes
individual undergraduate EE/ECE support through HD/Haidao Education (海道教育) and NewEDU.
Its scope and case descriptions were checked against the author's private
2024–2026 teaching archive: tutor-labelled lecture slides, instructor MATLAB
demonstrations, lesson notes, FPGA interface examples, and power-system models.
The page distinguishes teaching focus and learning goals from measured outcomes.
No student names, grades, course submissions, private records, or third-party
lecture/exam files are published. NewEDU follows the spelling in the archive
and its existing website project. Source documents remain outside this repo.
