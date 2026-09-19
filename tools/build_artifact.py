# Builds a single-file preview (tools/artifact.html) with reduced images inlined once each via a data-a resolver.
import os, re, base64, io, json
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "tools", "artifact-src.html"), encoding="utf-8").read()
names = sorted(set(re.findall(r'assets/([\w\-.]+\.(?:jpg|png))', src)))
A = {}
for n in names:
    im = Image.open(os.path.join(ROOT, "assets", n))
    if n.endswith(".png"):
        im.thumbnail((1400, 1400)); buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); mime = "image/png"
    else:
        mx = 1500 if n == "cova-corner.jpg" else 960
        im = im.convert("RGB"); im.thumbnail((mx, mx)); buf = io.BytesIO(); im.save(buf, "JPEG", quality=66 if n == "cova-corner.jpg" else 49, optimize=True, progressive=True); mime = "image/jpeg"
    A[n] = f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()
out = re.sub(r'data-src="assets/([\w\-.]+)"', r'data-src="\1"', src)   # lightbox sources, resolved at open time
out = re.sub(r'(?<![\w-])src="assets/([\w\-.]+)"', r'data-a="\1"', out)  # <img src> only, never data-src
out = re.sub(r' srcset="[^"]*" sizes="[^"]*"', '', out)  # the preview inlines one edition per image
# packed map tiles + inlined Leaflet for the preview (tiles fetched by the session's tiles.py into TILES_DIR)
TILES_DIR = os.environ.get("TILES_DIR", "")
pack = {"osm": {}, "esri": {}}
if TILES_DIR and os.path.isdir(TILES_DIR):
    for kind, ext, mime in (("osm", ".png", "image/png"), ("esri", ".jpg", "image/jpeg")):
        d = os.path.join(TILES_DIR, kind)
        if not os.path.isdir(d): continue
        import math
        for f in sorted(os.listdir(d)):
            if not re.fullmatch(r"\d+_\d+_\d+" + re.escape(ext), f): continue
            z, x, y = f[:-len(ext)].split("_")
            zi, yi = int(z), int(y)
            lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (yi + 0.5) / 2 ** zi))))
            if kind == "esri" and zi >= 15 and lat > 7.5: continue  # aerial stays at city zooms in Abuja; Cova keeps its close-ups
            im = Image.open(os.path.join(d, f)); buf = io.BytesIO()
            if kind == "osm": im = im.convert("L")   # street tiles are shown in monochrome, so store them that way
            else: im = im.convert("RGB")
            im.save(buf, "JPEG", quality=48 if kind == "osm" else 50, optimize=True)
            pack[kind][f"{z}/{x}/{y}"] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    if not pack["esri"]: pack.pop("esri")
leaflet_css = open(os.path.join(ROOT, "assets", "leaflet", "leaflet.css"), encoding="utf-8").read()
leaflet_js = open(os.path.join(ROOT, "assets", "leaflet", "leaflet.js"), encoding="utf-8").read()
mapblock = ("<style>" + leaflet_css + "</style>\n<script>" + leaflet_js + "</script>\n<script>window.__TILES=" + json.dumps(pack) + ";</script>\n") if pack["osm"] else ""
print("tiles packed:", len(pack["osm"]), "osm", len(pack.get("esri", {})), "esri")
resolver = mapblock + "<script>window.__A=" + json.dumps(A) + ";document.querySelectorAll('[data-a]').forEach(function(el){el.src=window.__A[el.dataset.a]||''});</script>\n"
i = out.index("<script>")
out = out[:i] + resolver + out[i:]
open(os.path.join(ROOT, "tools", "artifact.html"), "w", encoding="utf-8").write(out)
print("artifact.html", len(out)//1024, "KB;", len(names), "images")
