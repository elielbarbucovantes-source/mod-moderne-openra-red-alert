"""Planche d'aperçu : quelques orientations agrandies, caisse + tourelle superposées."""
import sys
from PIL import Image
import render
import models

PAL = render.load_palette(sys.argv[1])
OUT = sys.argv[2]
names = sys.argv[3:] or ["leopard", "challenger", "t90m", "bmpt", "jaguar"]
FACINGS = [0, 4, 8, 12, 16, 20, 24, 28]
S = 48
Z = 4

rows = []
for name in names:
    built = getattr(models, name)()
    row = Image.new("RGB", (S * len(FACINGS), S), (70, 80, 60))
    for i, f in enumerate(FACINGS):
        if isinstance(built, tuple):
            hull, tur, off = built
            body = render.outline(render.render_frame(hull, f / 32, (S, S)))
            turret = render.outline(render.render_frame(tur, f / 32, (S, S), shadow=False))
            import math
            th = 2 * math.pi * f / 32
            dx, dy = round(-math.sin(th) * off), round(-math.cos(th) * off * math.cos(render.TILT))
            layers = [(body, 0, 0), (turret, dx, dy)]
        else:
            layers = [(render.outline(render.render_frame(built, f / 32, (S, S))), 0, 0)]
        for img, dx, dy in layers:
            img.putpalette(PAL)
            rgba = img.convert("RGBA")
            px = rgba.load()
            src = img.load()
            for y in range(S):
                for x in range(S):
                    if src[x, y] == 0:
                        px[x, y] = (0, 0, 0, 0)
                    elif src[x, y] == 4:
                        px[x, y] = (0, 0, 0, 90)
            row.paste(rgba, (i * S + dx, dy), rgba)
    rows.append(row)

sheet = Image.new("RGB", (S * len(FACINGS), S * len(rows)))
for i, r in enumerate(rows):
    sheet.paste(r, (0, i * S))
sheet.resize((sheet.width * Z, sheet.height * Z), Image.NEAREST).save(OUT)
