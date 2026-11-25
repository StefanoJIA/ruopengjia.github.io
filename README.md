# ruopengjia.github.io

Ruopeng Jia's personal website. The static site lives in `docs/`.

Preview the site from this checkout with:

```powershell
python -m http.server 8772 --bind 127.0.0.1 --directory docs
```

Open http://127.0.0.1:8772/ to review the homepage, detailed research projects,
and academic background. The shared navigation links to Research, Writing,
Background, and Contact. News and the gallery remain in the footer.

Content is maintained directly in the HTML files. Keep the home summaries,
research details, and background timeline consistent when adding results.
Styles are shared by all ten current pages; bump the stylesheet query version
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
