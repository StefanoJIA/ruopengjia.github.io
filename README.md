# ruopengjia.github.io

Ruopeng Jia's personal website. The static site lives in `docs/`.

Preview the site from this checkout with:

```powershell
python -m http.server 8772 --bind 127.0.0.1 --directory docs
```

Open http://127.0.0.1:8772/ to review the research portfolio, academic
background, and contact section. The footer links to the news and gallery archives.

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
