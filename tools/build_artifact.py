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
        mx = 1600 if n == "lc-dusk.jpg" else 1200
        im = im.convert("RGB"); im.thumbnail((mx, mx)); buf = io.BytesIO(); im.save(buf, "JPEG", quality=68 if n == "lc-dusk.jpg" else 60, optimize=True, progressive=True); mime = "image/jpeg"
    A[n] = f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode()
out = re.sub(r'src="assets/([\w\-.]+)"', r'data-a="\1"', src)
out = re.sub(r'data-src="assets/([\w\-.]+)"', r'data-src="\1"', out)
resolver = "<script>window.__A=" + json.dumps(A) + ";document.querySelectorAll('[data-a]').forEach(function(el){el.src=window.__A[el.dataset.a]||''});</script>\n"
i = out.index("<script>")
out = out[:i] + resolver + out[i:]
open(os.path.join(ROOT, "tools", "artifact.html"), "w", encoding="utf-8").write(out)
print("artifact.html", len(out)//1024, "KB;", len(names), "images")
