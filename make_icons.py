from PIL import Image, ImageDraw, ImageFont
import os

BLU = (0, 51, 153, 255)
GIALLO = (255, 204, 0, 255)

FONT_PATHS = [
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

def load_font(size_px):
    for fp in FONT_PATHS:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size_px)
    return ImageFont.load_default()

def make_icon(size, path, maskable=False):
    # Rendering ad alta risoluzione (4x) e downscale, per bordi lisci
    scale = 4
    S = size * scale
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if maskable:
        # maskable: riempi tutto (Android ritaglierà)
        d.rectangle([0, 0, S, S], fill=GIALLO)
    else:
        # Angoli molto arrotondati per un look più moderno/smooth
        radius = int(S * 0.28)
        border_w = max(1, int(S * 0.045))
        # Riempimento giallo
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=radius, fill=GIALLO)
        # Bordo blu Poste
        d.rounded_rectangle(
            [border_w // 2, border_w // 2, S - 1 - border_w // 2, S - 1 - border_w // 2],
            radius=radius - border_w // 2,
            outline=BLU,
            width=border_w,
        )

    # Testo "PP" al centro
    font = load_font(int(S * 0.56))
    text = "PP"
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (S - tw) / 2 - bbox[0]
    y = (S - th) / 2 - bbox[1]
    d.text((x, y), text, fill=BLU, font=font)

    # Downscale con antialiasing di qualità -> bordi lisci
    img = img.resize((size, size), Image.LANCZOS)
    img.save(path, "PNG")

os.chdir("/sessions/stoic-eloquent-allen/mnt/outputs")
make_icon(192, "icon-192.png")
make_icon(512, "icon-512.png")
make_icon(512, "icon-maskable-512.png", maskable=True)
make_icon(64, "favicon.png")
print("done")
