"""Variantes d'infanterie RATC à partir des sprites RA d'origine.

On garde toutes les animations RA (debout, course, tir, couché, morts...)
et on ajoute l'équipement distinctif de chaque unité, pixel par pixel.

Usage : python3 infantry.py temperat.pal DOSSIER_FRAMES
DOSSIER_FRAMES contient e1/, e2/, e3/, e1icon/... produits par
  ./utility.sh --png e1.shp temperat.pal   (etc.)
"""
import os
import sys
from PIL import Image
import render

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "mods", "ratc", "bits")
TRANSPARENT, SHADOW = 0, 4


def nearest(palette, rgb, exclude=range(80, 96)):
    best, bi = None, 0
    for i in list(range(16, 80)) + list(range(104, 240)):
        if i in exclude:
            continue
        r, g, b = palette[3 * i:3 * i + 3]
        d = (r - rgb[0]) ** 2 + (g - rgb[1]) ** 2 + (b - rgb[2]) ** 2
        if best is None or d < best:
            best, bi = d, i
    return bi


def figure_rows(img):
    """Lignes occupées par le soldat (hors ombre), de haut en bas."""
    w, h = img.size
    p = img.load()
    rows = {}
    for y in range(h):
        xs = [x for x in range(w) if p[x, y] not in (TRANSPARENT, SHADOW)]
        if xs:
            rows[y] = xs
    return rows


def recolor(img, head=None, head_rows=2, darken=0, band=None, antenna=None, goggles=None):
    img = img.copy()
    p = img.load()
    rows = figure_rows(img)
    if not rows:
        return img
    ys = sorted(rows)
    standing = ys[-1] - ys[0] >= 9      # couché / mort : on ne touche qu'à la tenue
    if darken:
        for y in ys:
            for x in rows[y]:
                if 80 <= p[x, y] <= 95:
                    p[x, y] = min(95, p[x, y] + darken)
    if not standing:
        return img
    top = ys[0]
    if head is not None:
        for y in ys[:head_rows]:
            for x in rows[y]:
                p[x, y] = head
    if goggles is not None and len(ys) > 2:
        for x in rows[ys[2]]:
            p[x, ys[2]] = goggles
    if band is not None and len(ys) > 6:
        y = ys[5]
        x = rows[y][0]
        p[x, y] = band
    if antenna is not None and top >= 2:
        x = rows[top][-1]
        p[x, top - 1] = antenna
        p[x, top - 2] = antenna
    return img


def load_frames(folder, prefix):
    names = sorted(f for f in os.listdir(folder) if f.startswith(prefix + "-") and f.endswith(".png"))
    return [Image.open(os.path.join(folder, n)) for n in names]


def flag(icon, stripes, vertical=True, x0=48, y0=3, w=13, h=9):
    """Petit drapeau national dans le coin de l'icône."""
    icon = icon.copy()
    p = icon.load()
    for y in range(h):
        for x in range(w):
            if vertical:
                c = stripes[min(len(stripes) - 1, x * len(stripes) // w)]
            else:
                c = stripes[min(len(stripes) - 1, y * len(stripes) // h)]
            p[x0 + x, y0 + y] = c
    for x in range(-1, w + 1):
        p[x0 + x, y0 - 1] = p[x0 + x, y0 + h] = 143
    for y in range(-1, h + 1):
        p[x0 - 1, y0 + y] = p[x0 + w, y0 + y] = 143
    return icon


def union_jack(icon, pal, x0=48, y0=3, w=13, h=9):
    blue, red, white = nearest(pal, (20, 40, 140)), nearest(pal, (200, 20, 30)), nearest(pal, (240, 240, 240))
    icon = flag(icon, [blue], True, x0, y0, w, h)
    p = icon.load()
    for x in range(w):
        for y in range(h):
            diag = abs(x * h - y * w) <= w or abs(x * h - (h - 1 - y) * w) <= w
            if diag:
                p[x0 + x, y0 + y] = white
            if abs(x - w // 2) <= 1 or abs(y - h // 2) <= 1:
                p[x0 + x, y0 + y] = white
            if x == w // 2 or y == h // 2:
                p[x0 + x, y0 + y] = red
    return icon


def main(pal_path, frames_dir):
    pal = render.load_palette(pal_path)
    red = nearest(pal, (170, 20, 30))          # béret amarante
    olive = nearest(pal, (70, 100, 45))
    dkgreen = nearest(pal, (50, 70, 40))
    yellow = nearest(pal, (240, 210, 40))
    black = 143
    grey = 136
    blue = nearest(pal, (20, 60, 170))
    white = nearest(pal, (240, 240, 240))

    units = {
        # nom : (sprite RA, retouche, drapeau)
        "gcp": ("e1", dict(head=red, darken=2), "GCP", lambda i: flag(i, [blue, white, red])),
        "nlaw": ("e3", dict(head=olive), "NLAW", lambda i: union_jack(i, pal)),
        "fpvop": ("e2", dict(goggles=black, antenna=grey), "DRONE FPV", lambda i: flag(i, [blue, yellow], vertical=False)),
        "trench": ("e1", dict(head=dkgreen, band=yellow), "TRANCHEE", lambda i: flag(i, [blue, yellow], vertical=False)),
    }
    for name, (base, opts, title, add_flag) in units.items():
        frames = [recolor(f, **opts) for f in load_frames(os.path.join(frames_dir, base), base)]
        render.save_sheet(frames, os.path.join(OUT, f"{name}.png"), pal)
        icon = load_frames(os.path.join(frames_dir, base + "icon"), base + "icon")[0]
        render.save_sheet([render.label(add_flag(icon), title)], os.path.join(OUT, f"{name}icon.png"), pal)
        print(f"{name}: {len(frames)} images (base {base}) + icône")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
