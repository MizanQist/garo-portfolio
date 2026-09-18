# Makes assets/m/<name>.jpg, a 1400 px edition of every JPEG asset, for phones (srcset and the lightbox on small screens).
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets"); M = os.path.join(A, "m"); os.makedirs(M, exist_ok=True)
n = 0
for f in sorted(os.listdir(A)):
    if not f.endswith(".jpg"): continue
    im = Image.open(os.path.join(A, f)).convert("RGB"); im.thumbnail((1400, 1400), Image.LANCZOS)
    im.save(os.path.join(M, f), "JPEG", quality=78, optimize=True, progressive=True); n += 1
print(n, "mobile images;", sum(os.path.getsize(os.path.join(M, f)) for f in os.listdir(M)) // 1024, "KB")
