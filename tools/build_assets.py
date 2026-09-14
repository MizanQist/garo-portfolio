# Builds assets/ for the Garo Private Portfolio from the MQ portfolio photos, the drone originals and the sibling brochures.
import os, shutil
from PIL import Image, ImageOps
Image.MAX_IMAGE_PIXELS = None
D = "/Users/mammanali/Desktop/Desktop - Mamman’s MacBook Pro"
P = "/private/tmp/claude-501/-Users-mammanali/790ae5f1-578e-43e0-8d8e-ca298bd448d0/scratchpad/mq/photos"
OUT = os.path.join(D, "Garo Private Portfolio", "assets")
os.makedirs(OUT, exist_ok=True)

def save(im, name, maxw=None, q=84):
    im = ImageOps.exif_transpose(im).convert("RGB")
    if maxw and im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = os.path.join(OUT, name + ".jpg")
    im.save(p, "JEPG".replace("JEPG","JPEG"), quality=q, optimize=True, progressive=True)
    print(f"{name:22s} {im.size} {os.path.getsize(p)//1024} KB")

def port(pid, name, maxw=None):
    save(Image.open(os.path.join(P, pid + ".jpg")), name, maxw)

# 01 Lake Chad = Maitama View
MV = os.path.join(D, "Maitama View Brochure", "assets")
for src, name in [("hero-terrace","lc-hero"),("hero-dusk","lc-dusk"),("row","lc-row"),("corner","lc-corner"),("avenue","lc-avenue"),("avenue-corner","lc-avenue-corner"),("front-day","lc-front"),("aerial","lc-aerial")]:
    save(Image.open(os.path.join(MV, src + ".jpg")), name, 2400)
# 02 Gana Street
port("61","gana-c1"); port("60","gana-c2"); port("30","gana-s1"); port("31","gana-s2"); port("32","gana-s3")
# 03 Agulu Lake
save(Image.open(os.path.join(D, "Agulu Lake ", "Agulu Lake Render.png")), "agulu-render")
A2 = os.path.join(D, "Agulu Lake 2")
for src, name in [("dji_fly_20260822_153324_266_1787416185879_photo_optimized 2.JPG","agulu-s1"),("dji_fly_20260822_153326_267_1787416175979_photo_optimized 2.JPG","agulu-s2"),("dji_fly_20260822_153404_270_1787416156219_photo_optimized 2.JPG","agulu-s3"),("dji_fly_20260822_153340_268_1787416170490_photo_optimized 2.JPG","agulu-s4")]:
    save(Image.open(os.path.join(A2, src)), name, 2400, 80)
# 04 Heights 777
H7 = os.path.join(D, "Heights 777 Brochure", "assets")
for src, name in [("corner-dusk","h777-corner-dusk"),("entrance-dusk","h777-entrance-dusk"),("front-clear","h777-front-clear"),("street-day","h777-street-day"),("balconies-aerial","h777-balconies"),("entrance-day","h777-entrance-day"),("front-overcast","h777-front-overcast")]:
    save(Image.open(os.path.join(H7, src + ".jpg")), name, 1800)
# 05 Katampe
for i, pid in enumerate(["52","56","57","58","53","54","55"], 1): port(pid, f"kat-c{i}")
port("51","kat-plan1"); port("59","kat-plan2")
for i, pid in enumerate(["04","07","09","11","13"], 1): port(pid, f"kat-s{i}")
save(Image.open(os.path.join(D, "Katampe", "dji_fly_20260822_155504_289_1787415741201_photo_optimized.JPG")), "kat-s6", 2400, 80)
# 06 Utako
port("48","utako-plan"); port("49","utako-c1"); port("50","utako-c2")
for i, pid in enumerate(["23","19","18","25","21","22","26"], 1): port(pid, f"utako-s{i}")
U = os.path.join(D, "Utako ")
save(Image.open(os.path.join(U, "dji_fly_20260822_180314_317_1787426663477_photo_optimized.JPG")), "utako-s8", 2400, 80)
save(Image.open(os.path.join(U, "dji_fly_20260822_181212_329_1787427968939_photo_optimized.JPG")), "utako-s9", 2400, 80)
# 07 Olakunle Gidado
for i, pid in enumerate(["62","64","65","63"], 1): port(pid, f"og-s{i}")
# 09 Linda Chalker
for i, pid in enumerate(["69","68","67","66"], 1): port(pid, f"linda-c{i}")
for i, pid in enumerate(["37","36","35","34","33"], 1): port(pid, f"linda-s{i}")
# 10 Cova Manor
CM = os.path.join(D, "Cova Manor Brochure", "assets")
for src in ["approach","corner","front"]:
    save(Image.open(os.path.join(CM, src + ".jpg")), "cova-" + src)
for src in ["plan-duplex-lower","plan-duplex-upper","plan-first"]:
    shutil.copy(os.path.join(CM, src + ".png"), os.path.join(OUT, "cova-" + src + ".png")); print("copied", src)
print("DONE")
