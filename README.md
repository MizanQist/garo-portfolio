# The Garo Portfolio

A private, single-page portfolio of ten residential addresses (nine in Abuja, one in Victoria Island, Lagos), prepared by Mizan Qist Limited for H.E. Murtala Sule Garo. Static site: `index.html` + `assets/`, no build step needed to host it.

- `index.html` — the site (generated; see below)
- `assets/` — photographs, visualisations and plans (JPEG/PNG)
- `favicon.svg`, `robots.txt` (noindex), `.nojekyll` — for GitHub Pages
- `tools/data.py` — every fact, price and caption on the page
- `tools/build_site.py` — regenerates `index.html` from `data.py` (`python3 tools/build_site.py`)
- `tools/build_assets.py` — rebuilt `assets/` from the MQ portfolio photos, drone originals and the sibling brochures
- `tools/build_artifact.py` — makes `tools/artifact.html`, a single-file preview with reduced images inlined

This site is independent of the other clients' sites: change its prices, wording or properties in `tools/data.py` (and the client's name in `tools/client.py`), then rerun `build_site.py`. Previews need map tiles: `python3 tools/fetch_tiles.py` once, then `TILES_DIR=tools/tiles python3 tools/build_artifact.py`. To change the design, edit the CSS/JS blocks in `build_site.py` (or edit `index.html` directly and stop using the generator).

Sources: Mizan Qist residential portfolio (August 2026), Maitama View and Cova Manor brochures (July 2026 drawings), Heights 777 brochure, drone photography of 22 August 2026, Agulu Lake render. Confidential; not for onward circulation.
