"""Sprites des pouvoirs de soutien : pont flottant allemand et réticule AWACS.

Usage : python3 powers.py temperat.pal
"""
import os
import sys
from PIL import Image
import render

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "mods", "ratc", "bits")
CELL = 24


def nearest(pal, rgb):
    best, bi = None, 0
    for i in list(range(16, 80)) + list(range(104, 240)):
        r, g, b = pal[3 * i:3 * i + 3]
        d = (r - rgb[0]) ** 2 + (g - rgb[1]) ** 2 + (b - rgb[2]) ** 2
        if best is None or d < best:
            best, bi = d, i
    return bi


def bridge_tile(pal, orientation):
    """Travée de pont flottant (type M3 / Faltschwimmbrücke), vue de dessus.

    orientation : "ns" (circulation nord-sud), "ew" (est-ouest) ou "c" (travée centrale).
    """
    yellow = nearest(pal, (230, 190, 30))
    black = 143
    deck_light, deck, deck_dark = 133, 136, 139
    pontoon, pontoon_dark = 140, 142
    rivet = 131
    img = Image.new("P", (CELL, CELL), 0)
    p = img.load()

    def along(i, j):
        # (i : sens de circulation, j : travers) -> (x, y)
        return (j, i) if orientation == "ns" else (i, j)

    if orientation == "c":
        for y in range(CELL):
            for x in range(CELL):
                p[x, y] = deck
                if x % 4 == 0 or y % 4 == 0:
                    p[x, y] = deck_dark
                if (x % 4, y % 4) == (2, 2):
                    p[x, y] = rivet
        for k in range(CELL):                       # bordure de signalisation aux 4 coins
            for a, b in ((k, 0), (k, CELL - 1), (0, k), (CELL - 1, k)):
                if k < 4 or k >= CELL - 4:
                    p[a, b] = yellow if (a + b) // 2 % 2 == 0 else black
        return img

    for i in range(CELL):
        for j in range(CELL):
            if j < 2 or j >= CELL - 2:                  # flancs des pontons (dépassent sous le tablier)
                c = pontoon_dark if j in (0, CELL - 1) else pontoon
            elif j < 4 or j >= CELL - 4:                # bordures jaunes et noires
                c = yellow if ((i + j) // 2) % 2 == 0 else black
            else:
                c = deck
                if i % 3 == 0:                          # stries antidérapantes transversales
                    c = deck_dark
                elif i % 3 == 1 and j in (8, 15):       # ornières de roulement
                    c = deck_light
                if j in (4, CELL - 5):
                    c = deck_dark
                if i % 12 == 6 and j in (5, CELL - 6):  # rivets des jonctions de travées
                    c = rivet
            if i % 12 == 0 and 2 <= j < CELL - 2:       # joint entre deux panneaux
                c = black
            x, y = along(i, j)
            p[x, y] = c
    return img


def reticle(pal, size=17):
    """Réticule de ciblage AWACS (coins + croix), rouge vif."""
    red = nearest(pal, (240, 30, 30))
    dark = nearest(pal, (90, 0, 0))
    img = Image.new("P", (size, size), 0)
    p = img.load()
    m = size - 1
    for k in range(5):                              # coins
        for x, y in ((k, 0), (0, k), (m - k, 0), (m, k), (k, m), (0, m - k), (m - k, m), (m, m - k)):
            p[x, y] = red
    c = size // 2
    for k in range(3, 7):                           # branches de la croix
        for x, y in ((c, k), (c, m - k), (k, c), (m - k, c)):
            p[x, y] = red
    p[c, c] = red
    for x, y in ((1, 1), (m - 1, 1), (1, m - 1), (m - 1, m - 1)):
        p[x, y] = dark
    return img


def laser_mark(pal, size=13):
    """Losange vert du désignateur laser (drone Luna)."""
    green = nearest(pal, (40, 240, 60))
    dark = nearest(pal, (0, 90, 20))
    img = Image.new("P", (size, size), 0)
    p = img.load()
    c = size // 2
    for y in range(size):
        for x in range(size):
            d = abs(x - c) + abs(y - c)
            if d == c:
                p[x, y] = green
            elif d == c - 1:
                p[x, y] = dark
    p[c, c] = green
    return img


def main(pal_path):
    pal = render.load_palette(pal_path)
    tiles = [bridge_tile(pal, o) for o in ("ns", "ew", "c")]
    render.save_sheet(tiles, os.path.join(OUT, "tacbridge.png"), pal)
    # Icône du pouvoir : trois travées côte à côte sur fond d'eau.
    icon = Image.new("P", (64, 48), nearest(pal, (40, 70, 110)))
    ip = icon.load()
    water_hi = nearest(pal, (70, 110, 150))
    for y in range(48):
        for x in range(64):
            if (x + 2 * y) % 11 == 0:
                ip[x, y] = water_hi
    ew = tiles[1]
    for k in range(3):
        icon.paste(ew, (-4 + k * CELL, 10))
    icon = render.label(icon, "PONT")
    render.save_sheet([icon], os.path.join(OUT, "tacbridgeicon.png"), pal)
    render.save_sheet([reticle(pal)], os.path.join(OUT, "awacsmark.png"), pal)
    render.save_sheet([laser_mark(pal)], os.path.join(OUT, "lasermark.png"), pal)
    print("pont (3 travées + icône), réticule AWACS")


if __name__ == "__main__":
    main(sys.argv[1])
