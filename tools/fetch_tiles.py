# Fetches the map tiles that build_artifact.py packs into the preview (TILES_DIR=tools/tiles). OSM z11-14 over the
# Abuja box plus z15 around each pin and the CBD; z12-16 around Cova Manor; Esri aerial z13-14 Abuja and z15-16 at Cova.
import math, os, re, time, urllib.request, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import SITES
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiles")
def t(lat, lon, z):
    n = 2 ** z; return int((lon + 180) / 360 * n), int((1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n)
def box(lat0, lat1, lon0, lon1, z):
    x0, y0 = t(lat1, lon0, z); x1, y1 = t(lat0, lon1, z); return {(z, x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}
def around(lat, lon, z, r=1):
    x, y = t(lat, lon, z); return {(z, x + dx, y + dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1)}
AB = (8.995, 9.115, 7.415, 7.545); CBD = (9.0508926, 7.4929880)
abuja = [s["ll"] for s in SITES if s["ll"] and s["city"] == "Abuja"]; cova = [s["ll"] for s in SITES if s["city"] == "Lagos"][0]
osm, esri = set(), set()
def view(lat, lon, z, w=6, h=4):
    """tiles around a point covering w x h tiles (a desktop viewport is about 5.6 x 3.5 tiles)"""
    x, y = t(lat, lon, z); return {(z, x + dx, y + dy) for dx in range(-w // 2, w - w // 2) for dy in range(-h // 2, h - h // 2)}
ABJ, LAG = (9.06, 7.49), (6.43, 3.42)
for z in range(6, 14): osm |= view(*ABJ, z, 8, 5)           # country to district zooms around Abuja, with panning margin
for z in range(9, 14): osm |= view(*LAG, z)                 # Lagos from region to district
osm |= box(*AB, 14)                                         # the Abuja box at street zoom
for ll in abuja + [CBD]: osm |= around(ll[0], ll[1], 15)    # close-ups at every pin
for z in (14, 15): osm |= view(6.428, 3.424, z, 8, 5)              # the Lagos view: Cova Manor and the Eko Hotel together
osm |= around(cova[0], cova[1], 16)
esri |= box(*AB, 13) | box(*AB, 14)                         # aerial at district and street zooms
for z in (15, 16): esri |= around(cova[0], cova[1], z)
print("planned osm", len(osm), "esri", len(esri), flush=True)
os.makedirs(os.path.join(OUT, "osm"), exist_ok=True); os.makedirs(os.path.join(OUT, "esri"), exist_ok=True)
UA = {"User-Agent": "MizanQist-brochure/1.0 (nabildeealee@icloud.com)"}
def get(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0: return
    for _ in range(3):
        try:
            open(path, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()); return
        except Exception: time.sleep(1.5)
    print("FAILED", url, flush=True)
for z, x, y in sorted(osm): get(f"https://tile.openstreetmap.org/{z}/{x}/{y}.png", os.path.join(OUT, "osm", f"{z}_{x}_{y}.png")); time.sleep(0.12)
for z, x, y in sorted(esri): get(f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", os.path.join(OUT, "esri", f"{z}_{x}_{y}.jpg")); time.sleep(0.08)
# prune tiles that are no longer in the plan, so the preview pack stays within budget
for kind, keep, ext in (("osm", osm, ".png"), ("esri", esri, ".jpg")):
    d = os.path.join(OUT, kind)
    for f in os.listdir(d):
        if not re.fullmatch(r"\d+_\d+_\d+" + re.escape(ext), f): os.remove(os.path.join(d, f)); continue
        if tuple(int(v) for v in f[:-len(ext)].split("_")) not in keep: os.remove(os.path.join(d, f))
print("DONE osm", len(os.listdir(os.path.join(OUT, "osm"))), "esri", len(os.listdir(os.path.join(OUT, "esri"))), flush=True)
