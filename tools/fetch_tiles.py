# Fetches the map tiles that build_artifact.py packs into the preview (TILES_DIR=tools/tiles). OSM z11-14 over the
# Abuja box plus z15 around each pin and the CBD; z12-16 around Cova Manor; Esri aerial z13-14 Abuja and z15-16 at Cova.
import math, os, time, urllib.request, sys
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
# wide context so the preview can zoom out: the country, then the two city regions, then the Abuja box
osm |= box(4.0, 14.0, 2.5, 14.5, 6)                      # Nigeria
osm |= box(5.5, 10.5, 2.5, 9.0, 7) | box(5.5, 10.5, 2.5, 9.0, 8)   # Abuja and Lagos regions
for z in (9, 10): osm |= box(8.6, 9.6, 7.0, 8.0, z) | box(6.2, 6.8, 3.0, 3.8, z)
osm |= box(8.8, 9.35, 7.25, 7.75, 11) | box(6.3, 6.6, 3.2, 3.6, 11)
osm |= box(8.9, 9.25, 7.3, 7.65, 12)
osm |= box(8.95, 9.15, 7.38, 7.58, 13)
for z in (11, 12, 13, 14): osm |= box(*AB, z)
esri |= box(8.9, 9.25, 7.3, 7.65, 11) | box(*AB, 12)
for ll in abuja + [CBD]: osm |= around(ll[0], ll[1], 15)
for z in (12, 13, 14, 15, 16): osm |= around(cova[0], cova[1], z)
for z in (13, 14): esri |= box(*AB, z)
for z in (15, 16): esri |= around(cova[0], cova[1], z)
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
print("DONE osm", len(os.listdir(os.path.join(OUT, "osm"))), "esri", len(os.listdir(os.path.join(OUT, "esri"))), flush=True)
