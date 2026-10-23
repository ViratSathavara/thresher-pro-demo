# Shree Krushi Thresher Works - multi-page demo (GU / HI / EN)
Open (server must run from this folder):  `python -m http.server 8765`  ->  http://localhost:8765/
Each language has the same 12 pages: Home, Products, 4 product pages, Crop Guide, Manufacturing, Spares & Service, Subsidy help, About, FAQ, Contact (+404).
Edit copy in `tools/c_gu.py`, `c_hi.py`, `c_en.py`; layout in `tools/build.py`; styles in `tools/base.css` + `tools/extra.css`; then run `python tools/build.py`.
`SITE_URL=https://thresher-pro-demo.vercel.app python tools/build.py` sets canonical/hreflang/sitemap domain (use the real domain at go-live; remove the noindex header in vercel.json).
Placeholders to replace: brand, phone/WhatsApp (`WA`, `PHONE` in build.py), address, photos (CC-licensed; credits in footer).
`v1-single-page.html` is the earlier one-page version.
