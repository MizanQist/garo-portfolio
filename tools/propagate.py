# Pushes the shared files of this (master) copy to the sibling client copies and rebuilds them.
# Run from the Garo folder: python3 tools/propagate.py   (client.py and README.md stay per copy)
import os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(ROOT)
SIBLINGS = ["Babalele Private Portfolio", "Dakingari Private Portfolio"]
SHARED_FILES = ["tools/data.py", "tools/build_site.py", "tools/build_artifact.py", "tools/build_mobile.py", "tools/build_assets.py", "tools/fetch_tiles.py", "tools/routes.json", "favicon.svg", "robots.txt", ".nojekyll", ".gitignore"]
for sib in SIBLINGS:
    dst = os.path.join(PARENT, sib)
    if not os.path.isdir(dst): print("missing", dst); continue
    for f in SHARED_FILES:
        os.makedirs(os.path.dirname(os.path.join(dst, f)) or dst, exist_ok=True); shutil.copy2(os.path.join(ROOT, f), os.path.join(dst, f))
    # assets: copy new/changed files only (by size + mtime)
    n = 0
    for dp, dn, fn in os.walk(os.path.join(ROOT, "assets")):
        rel = os.path.relpath(dp, ROOT); os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in fn:
            a, b = os.path.join(dp, f), os.path.join(dst, rel, f)
            if not os.path.exists(b) or os.path.getsize(a) != os.path.getsize(b) or int(os.path.getmtime(a)) > int(os.path.getmtime(b)): shutil.copy2(a, b); n += 1
    r = subprocess.run([sys.executable, os.path.join(dst, "tools", "build_site.py")], capture_output=True, text=True)
    print(sib, "| assets copied:", n, "|", r.stdout.strip() or r.stderr.strip()[-200:])
