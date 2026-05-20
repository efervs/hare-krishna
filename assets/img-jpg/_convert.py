"""Convert .webp images to JPG (min 500x500, square) for Meta WhatsApp Catalog."""
from pathlib import Path
from PIL import Image, ImageOps

SRC = Path(r"C:\Users\Eferi\Hare Krishna\Web\assets\img")
DST = Path(r"C:\Users\Eferi\Hare Krishna\Web\assets\img-jpg")
DST.mkdir(parents=True, exist_ok=True)

MIN_SIZE = 800  # >=500, generous for Meta
BG = (255, 255, 255)

count = 0
for src in sorted(SRC.iterdir()):
    if src.suffix.lower() not in (".webp", ".png", ".jpg", ".jpeg"):
        continue
    if src.name.startswith("."):
        continue

    out = DST / (src.stem + ".jpg")
    try:
        im = Image.open(src)
        im = ImageOps.exif_transpose(im)

        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, BG)
            bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
            im = bg
        else:
            im = im.convert("RGB")

        w, h = im.size
        side = max(w, h, MIN_SIZE)
        canvas = Image.new("RGB", (side, side), BG)

        if w < side or h < side:
            scale = min(side / w, side / h)
            new_w, new_h = int(w * scale), int(h * scale)
            im = im.resize((new_w, new_h), Image.LANCZOS)
            w, h = new_w, new_h

        canvas.paste(im, ((side - w) // 2, (side - h) // 2))
        canvas.save(out, "JPEG", quality=88, optimize=True, progressive=True)
        count += 1
        print(f"OK  {src.name} -> {out.name}  ({side}x{side})")
    except Exception as e:
        print(f"ERR {src.name}: {e}")

print(f"\nDone. {count} archivos convertidos en: {DST}")
