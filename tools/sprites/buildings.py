"""Bâtiments des pouvoirs de soutien nationaux (2x2 cases + dalle, comme le Radar Dome).

Usage : python3 buildings.py CHEMIN/temperat.pal [nom ...]

Chaque feuille contient : image intacte, image endommagée, puis l'animation
de construction (le bâtiment sort de terre). Les modèles sont décrits comme
les véhicules (24 px = 1 case) : x vers le fond (nord), y vers la gauche
(ouest), z vers le haut. L'empreinte 2x2 occupe x, y dans [-24, 24].
"""
import math
import os
import random
import sys
import render
from render import Model

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "mods", "ratc", "bits")
SIZE = (48, 112)
MAKE_FRAMES = 10
HEIGHT = 1.35
# Caméra plus rasante que pour les véhicules : on voit les façades, comme sur les bâtiments RA.
TILT = math.radians(58)
# Lumière venant de l'avant-gauche (les véhicules sont éclairés de l'arrière-gauche) :
# les façades tournées vers la caméra restent claires.
_l = (-0.45, -0.5, 0.75)
LIGHT = tuple(c / math.sqrt(sum(v * v for v in _l)) for c in _l)


# ---------------------------------------------------------------------------
# Éléments communs
# ---------------------------------------------------------------------------
def slab(m, x0=-23, x1=23, y0=-23, y1=23, mat="metal", tint=0.3):
    m.box(x0, x1, y0, y1, 0, 1.5, mat, tint)


def extrude_x(m, profile, x0, x1, mat="paint", tint=0.0):
    """Profil (y, z) donné dans le sens antihoraire, extrudé de x0 (avant) à x1 (fond)."""
    part = Model().extrude(profile, x0, x1, mat, tint)
    for s in part.transformed(lambda p, q, r: (r, p, q)).solids:
        m.solids.append(s)


def dish(m, cx, cy, cz, r, toward=(-1.0, 0.3), elev=40, mat="white"):
    """Parabole : disque orienté vers (toward), relevé de elev degrés, sur un pied."""
    dx, dy = toward
    ln = math.hypot(dx, dy)
    dx, dy = dx / ln, dy / ln
    e = math.radians(elev)
    n = (math.cos(e) * dx, math.cos(e) * dy, math.sin(e))
    u = (-dy, dx, 0.0)
    v = (n[1] * u[2] - n[2] * u[1], n[2] * u[0] - n[0] * u[2], n[0] * u[1] - n[1] * u[0])
    ring = []
    for i in range(12):
        a = 2 * math.pi * i / 12
        ring.append(tuple(c + r * (math.cos(a) * u[k] + math.sin(a) * v[k]) for k, c in enumerate((cx, cy, cz))))
    m.plate(ring, 0.8, mat)
    horn = tuple(c + n[k] * r * 0.7 for k, c in enumerate((cx, cy, cz)))
    m.box(horn[0] - 0.5, horn[0] + 0.5, horn[1] - 0.5, horn[1] + 0.5, horn[2] - 0.5, horn[2] + 0.5, "dark")
    m.box(cx - 1.2, cx + 1.2, cy - 1.2, cy + 1.2, 0, cz - r * 0.3, "metal", 0.1)       # pied


def mast(m, x, y, h, base=1.6, arms=3, light=True):
    """Mât en treillis avec traverses et feu d'obstacle rouge."""
    m.tapered_box(x - base, x + base, y - base, y + base, 0, h, inset_front=base * 0.7,
                  inset_back=base * 0.7, inset_side=base * 0.7, mat="metal", tint=0.15)
    for i in range(arms):
        z = h * (0.45 + 0.5 * i / max(1, arms - 1))
        m.box(x - 0.3, x + 0.3, y - 3.2, y + 3.2, z - 0.3, z + 0.3, "metal")
    if light:
        m.box(x - 0.6, x + 0.6, y - 0.6, y + 0.6, h, h + 1.2, "red")


def sandbags(m, x0, x1, y0, y1, h=2.6):
    """Rangée de sacs de sable (le long du plus grand côté)."""
    along_x = (x1 - x0) >= (y1 - y0)
    length = (x1 - x0) if along_x else (y1 - y0)
    n = max(1, int(length / 2.4))
    for i in range(n):
        a = (x0 if along_x else y0) + i * length / n
        b = a + length / n * 0.92
        tint = 0.04 if i % 2 else 0.14
        if along_x:
            m.box(a, b, y0, y1, 1.5, 1.5 + h, "olive", tint)
        else:
            m.box(x0, x1, a, b, 1.5, 1.5 + h, "olive", tint)


def hazard_band(m, x, y0, y1, z0, z1, n=6):
    """Bande jaune et noire verticale (façade orientée vers l'avant, à x)."""
    step = (y1 - y0) / n
    for i in range(n):
        m.box(x - 0.3, x + 0.2, y0 + i * step, y0 + (i + 1) * step, z0, z1, "yellow" if i % 2 == 0 else "dark")


# ---------------------------------------------------------------------------
# France — Centre de commandement SCALP : bunker bétonné à flancs inclinés,
# paraboles satellite, mâts de liaison et tourelle de visée laser sur le toit.
# ---------------------------------------------------------------------------
def pcscalp():
    m = Model()
    slab(m)
    m.tapered_box(-19, 12, -21, 11, 1.5, 13, inset_front=4, inset_back=3, inset_side=3.5, mat="concrete")
    m.box(-15, 9, -17.5, 7.5, 13, 14, "concrete", 0.08)                              # dalle de toit
    m.box(-20.5, -17, -6, 2, 1.5, 8, "dark")                                         # entrée
    m.box(-21, -20.5, -7, 3, 1.5, 9.5, "concrete", 0.2)                              # linteau
    m.box(-17.5, -16, -17.5, 7.5, 9.5, 11, "paint")                                  # bandeau national
    for y in (-13, -3, 5):                                                           # meurtrières
        m.box(-16.2, -15.6, y - 1.5, y + 1.5, 6.5, 7.5, "dark")
    m.box(-4, 3, -4, 3, 14, 17, "metal", 0.05)                                       # tourelle de visée laser
    m.box(-4.3, -3.8, -2.5, 1.5, 15, 16.5, "glass")
    m.box(-6, -4, -1.2, 0.2, 15.2, 16.4, "red")                                      # émetteur laser
    for x in (-12, -9, 6):                                                           # aérations
        m.box(x, x + 1.5, 4, 6, 14, 15.5, "dark")
    dish(m, 14, -16, 11, 6.5, toward=(-0.6, -0.4), elev=45)
    dish(m, 18, 3, 7, 3.5, toward=(-1, 0.4), elev=30)
    mast(m, 16, 17, 30)
    mast(m, -18, 17, 18, base=1.0, arms=2)
    return m


# ---------------------------------------------------------------------------
# Allemagne — Pionierzentrum : hangar d'assemblage à toit cintré, grande porte
# balisée, rampe d'essai pour les véhicules de franchissement, grue et
# travées de pont flottant en stock.
# ---------------------------------------------------------------------------
def pionier():
    m = Model()
    slab(m)
    arch = [(-7, 1.5), (7, 1.5), (7, 9), (5, 12.5), (0, 14), (-5, 12.5), (-7, 9)]    # profil (y, z)
    extrude_x(m, [(y + 9, z) for y, z in arch], -18, 18, "metal", 0.02)               # hangar (côté ouest)
    for x in (-10, -2, 6, 14):                                                        # arceaux
        extrude_x(m, [(y + 9, z + 0.4) for y, z in arch], x, x + 1, "metal", 0.2)
    extrude_x(m, [(y * 1.02 + 9, z + 0.5) for y, z in arch], -18.4, -17.6, "paint")   # arche de façade
    m.box(-18.8, -18, 3.5, 14.5, 1.5, 10, "dark")                                     # grande porte
    hazard_band(m, -19, 2.5, 15.5, 10, 11.2, n=8)
    m.box(-18, 18, -21, -6, 1.5, 7, "concrete")                                       # atelier (côté est)
    m.box(-18.5, -18, -19, -15, 1.5, 5.5, "glass")
    m.box(-18.5, -18, -12, -8, 1.5, 5.5, "glass")
    m.box(-16, 16, -20, -7, 7, 7.6, "concrete", 0.12)
    # rampe d'essai inclinée devant l'atelier
    m.prism([(-23, -21, 1.5), (-13, -21, 1.5), (-13, -7, 1.5), (-23, -7, 1.5)],
            [(-23, -21, 1.6), (-13, -21, 5.5), (-13, -7, 5.5), (-23, -7, 1.6)], "metal", 0.12)
    # travées de pont flottant empilées
    for i in range(3):
        m.box(6, 19, -5, 2, 1.5 + i * 2.2, 3.4 + i * 2.2, "yellow" if i == 2 else "paint", 0.1 * i)
    # grue
    m.box(12, 14, -18, -16, 7.6, 24, "yellow", 0.1)
    m.box(-2, 20, -17.8, -16.2, 22.5, 24, "yellow", 0.05)
    m.box(16, 20, -18.5, -15.5, 20, 22.5, "concrete", 0.2)                            # contrepoids
    m.box(-1, -0.4, -17.2, -16.8, 13, 22.5, "dark")                                   # câble
    m.box(-2, 0.6, -18.2, -15.8, 11.5, 13, "yellow", 0.2)                             # crochet
    mast(m, 20, 20, 16, base=1.0, arms=1)
    return m


# ---------------------------------------------------------------------------
# Royaume-Uni — Station SIGINT (GCHQ Forward) : bâtiment bas et fermé, dôme
# furtif à facettes sur le toit, mâts de brouillage à panneaux à l'arrière.
# ---------------------------------------------------------------------------
def gchq():
    m = Model()
    slab(m)
    m.box(-20, 6, -21, 21, 1.5, 10, "concrete", 0.05)                                  # bâtiment principal
    m.box(-20.5, -20, -21, 21, 6.5, 7.5, "glass")                                      # bandeau vitré
    m.box(-20.5, -20, -3, 3, 1.5, 5.5, "dark")                                         # entrée
    m.box(-18, 4, -19, 19, 10, 11, "concrete", 0.15)
    m.box(-20.4, -19.8, 8, 17, 8, 9.5, "paint")                                         # bandeau national
    # dôme furtif : facettes en tronc de pyramide octogonale
    def octagon(r, z, cx=-6, cy=-4):
        return [(cx + r * math.cos(2 * math.pi * (i + 0.5) / 8), cy + r * math.sin(2 * math.pi * (i + 0.5) / 8), z)
                for i in range(8)]
    m.prism(octagon(10, 11), octagon(8, 16), "white")
    m.prism(octagon(8, 16), octagon(4.5, 20.5), "white", 0.05)
    m.prism(octagon(4.5, 20.5), octagon(1.5, 22), "white", 0.1)
    # mâts de brouillage à panneaux (arrière)
    for y in (-15, 0, 15):
        m.box(10, 12, y - 1, y + 1, 1.5, 27, "metal", 0.1)
        for z in (16, 22):
            m.box(9, 13, y - 4, y + 4, z, z + 3.5, "paint", 0.05)
        m.box(10.6, 11.4, y - 0.4, y + 0.4, 27, 28.2, "red")
    m.box(8, 14, -20, 20, 1.5, 3, "concrete", 0.2)                                     # socle des mâts
    # clôture de sécurité
    for x0, x1, y0, y1 in ((-23, 22, 22.2, 22.8), (-23, 22, -22.8, -22.2), (21.8, 22.4, -22.8, 22.8)):
        m.box(x0, x1, y0, y1, 1.5, 5, "metal", 0.25)
    return m


# ---------------------------------------------------------------------------
# Ukraine — PC de liaison ISR & AWACS : poste semi-enterré sous filet de
# camouflage, sacs de sable, antenne radar à rotodome (clin d'œil à l'AWACS),
# terminaux satellite plats et shelters de communication.
# ---------------------------------------------------------------------------
def pcawacs():
    m = Model()
    slab(m, mat="earth", tint=0.05)
    m.box(-14, 10, -18, 6, 1.5, 7, "concrete", 0.1)                                     # poste semi-enterré
    m.tapered_box(-17, 13, -21, 9, 1.5, 8.5, inset_front=3, inset_back=3, inset_side=3, mat="earth", tint=0.1)
    m.box(-17.5, -14, -8, -2, 1.5, 6, "dark")                                           # accès
    # filet de camouflage tendu au-dessus
    m.prism([(-15, -19, 9.5), (11, -19, 9.5), (11, 7, 9.5), (-15, 7, 9.5)],
            [(-13, -17, 11), (9, -17, 11), (9, 5, 11), (-13, 5, 11)], "olive", 0.08)
    for x, y in ((-9, -12), (0, -5), (5, -14), (-6, 2)):                                # taches du filet
        m.box(x, x + 4, y, y + 3, 11, 11.3, "olive", 0.25)
    sandbags(m, -22, -18, -21, 9)
    sandbags(m, -22, 14, 10, 12.5)
    # rotodome sur mât (arrière gauche)
    m.box(14, 16, 12, 14, 1.5, 20, "metal", 0.1)
    rot = [(15 + 7 * math.cos(2 * math.pi * i / 14), 13 + 7 * math.sin(2 * math.pi * i / 14)) for i in range(14)]
    m.extrude(rot, 20, 22.5, "white")
    m.box(9, 21, 12.5, 13.5, 20.6, 21.9, "paint")                                       # bande du rotodome
    # terminaux satellite plats
    for x, y in ((16, -8), (16, -16)):
        m.box(x - 0.6, x + 0.6, y - 0.6, y + 0.6, 1.5, 4, "metal")
        m.prism([(x - 3, y - 2.5, 4), (x + 3, y - 2.5, 5.5), (x + 3, y + 2.5, 5.5), (x - 3, y + 2.5, 4)],
                [(x - 3, y - 2.5, 4.6), (x + 3, y - 2.5, 6.1), (x + 3, y + 2.5, 6.1), (x - 3, y + 2.5, 4.6)], "white", 0.1)
    # shelter de communication (conteneur)
    m.box(-4, 8, 14, 21, 1.5, 7, "olive", 0.02)
    m.box(-4.4, -4, 16, 19, 1.5, 5.5, "dark")
    mast(m, 20, -21, 24, base=1.0, arms=2)
    return m


# ---------------------------------------------------------------------------
# Russie — PC d'appui thermobarique : casemate très blindée enterrée sous un
# merlon de terre, deux dépôts de munitions, et un lanceur TOS-1A en
# stationnement devant l'entrée.
# ---------------------------------------------------------------------------
def pctos():
    m = Model()
    slab(m, mat="earth", tint=0.05)
    m.tapered_box(-16, 16, -22, 4, 1.5, 12, inset_front=6, inset_back=5, inset_side=5, mat="earth")   # merlon
    m.box(-12, 12, -18, 0, 1.5, 12.5, "concrete", 0.05)                                  # casemate
    m.box(-11, 11, -17, -1, 12.5, 14, "concrete", 0.15)
    m.box(-16.5, -12, -12, -5, 1.5, 8, "dark")                                            # porte blindée
    m.box(-16.8, -16.4, -13, -4, 8, 9.5, "paint")                                         # bandeau national
    m.box(-4, 2, -12, -6, 14, 17, "metal", 0.1)                                           # calculateur / optique
    m.box(-4.3, -3.9, -11, -7, 15, 16.2, "glass")
    # dépôts de munitions (demi-enterrés, portes jaunes)
    for x in (-18, 4):
        m.tapered_box(x, x + 10, 8, 22, 1.5, 7, inset_front=1.5, inset_back=1.5, inset_side=2, mat="earth", tint=0.1)
        m.box(x - 0.4, x + 0.1, 12, 18, 1.5, 5.5, "yellow")
    # lanceur TOS-1A garé (caisse de char + bloc de 24 tubes relevé)
    tx, ty = 17, -12
    m.box(tx - 5.5, tx + 5.5, ty - 4.5, ty + 4.5, 1.5, 3.8, "rubber")
    m.box(tx - 5, tx + 5.5, ty - 3.4, ty + 3.4, 2, 5, "paint", 0.05)
    m.prism([(tx - 5, ty - 3.2, 5), (tx + 3, ty - 3.2, 5), (tx + 3, ty + 3.2, 5), (tx - 5, ty + 3.2, 5)],
            [(tx - 7, ty - 3.2, 11), (tx + 1, ty - 3.2, 11), (tx + 1, ty + 3.2, 11), (tx - 7, ty + 3.2, 11)],
            "paint", 0.12)
    for i in range(3):                                                                    # bouches des tubes
        for j in range(4):
            y = ty - 2.4 + j * 1.6
            z = 6.2 + i * 1.6
            m.box(tx - 5.6 - i * 0.55, tx - 5.1 - i * 0.55, y - 0.5, y + 0.5, z - 0.5, z + 0.5, "dark")
    mast(m, 20, 20, 26, base=1.0, arms=2)
    return m


# ---------------------------------------------------------------------------
# Japon — Centre de guerre électronique : bâtiment technique blanc et moderne,
# grands panneaux d'antennes réseau inclinés (radar AESA), mât de brouillage
# et shelter de brouilleur mobile.
# ---------------------------------------------------------------------------
def jpew():
    m = Model()
    slab(m)
    m.box(-19, 4, -21, 8, 1.5, 12, "white", 0.1)                                      # bâtiment technique
    m.box(-19.5, -19, -21, 8, 7, 8.2, "glass")                                        # bandeau vitré
    m.box(-19.5, -19, -4, 2, 1.5, 5.5, "dark")                                        # entrée
    m.box(-17, 2, -19, 6, 12, 13, "white", 0.2)
    m.box(-19.4, -18.9, -20, -12, 9.5, 11, "paint")                                   # bandeau national
    # panneaux d'antennes réseau inclinés (face avant et côté)
    for y0 in (-16, -5):
        m.prism([(-4, y0, 13), (2, y0, 13), (2, y0 + 9, 13), (-4, y0 + 9, 13)],
                [(-1.5, y0, 21), (-0.5, y0, 21), (-0.5, y0 + 9, 21), (-1.5, y0 + 9, 21)], "white", 0.02)
        m.prism([(-4.4, y0 + 0.5, 13.5), (-4.0, y0 + 0.5, 13.5), (-4.0, y0 + 8.5, 13.5), (-4.4, y0 + 8.5, 13.5)],
                [(-1.9, y0 + 0.5, 20.5), (-1.5, y0 + 0.5, 20.5), (-1.5, y0 + 8.5, 20.5), (-1.9, y0 + 8.5, 20.5)],
                "dark")                                                               # grille rayonnante
    # mât de brouillage à dipôles
    m.box(10, 12, 13, 15, 1.5, 28, "metal", 0.1)
    for z in (14, 18, 22, 26):
        m.box(9.6, 12.4, 10, 18, z, z + 0.6, "white", 0.1)
    m.box(10.6, 11.4, 13.6, 14.4, 28, 29.2, "red")
    # shelter du brouilleur mobile (camion)
    for x in (12, 18):
        for y in (-20, -13):
            m.box(x - 1.2, x + 1.2, y - 0.6, y + 0.6, 1.5, 3.2, "rubber")
    m.box(8, 21, -20, -13, 3, 4, "dark")
    m.box(8, 16, -20.5, -12.5, 4, 9, "white", 0.14)
    m.box(16, 21, -20, -13, 4, 8, "paint", 0.06)                                      # cabine
    dish(m, 12, -16.5, 12, 3.2, toward=(-1, -0.3), elev=35)
    mast(m, 20, 3, 18, base=1.0, arms=2)
    return m


# ---------------------------------------------------------------------------
# Inde — PC du régiment Pinaka : hangar de maintenance au fond, lanceur Pinaka
# garé de profil devant (camion 8x8, deux blocs de 6 tubes relevés),
# caisses de roquettes.
# ---------------------------------------------------------------------------
def pinaka_launcher(m, tx, ty):
    """Camion lanceur Pinaka orienté le long de y, cabine vers la gauche (y+)."""
    for y in (ty - 7.5, ty - 4, ty + 1, ty + 4.5):
        for s in (1, -1):
            m.box(tx + s * 3.0 - 0.7, tx + s * 3.0 + 0.7, y - 1.4, y + 1.4, 1.5, 4.2, "rubber")
    m.box(tx - 3.2, tx + 3.2, ty - 9.5, ty + 7.5, 2.6, 4.4, "dark")                   # châssis
    m.box(tx - 3.6, tx + 3.6, ty + 3.5, ty + 9.0, 4.4, 9.5, "paint", 0.04)            # cabine blindée
    m.box(tx - 3.1, tx + 3.1, ty + 8.9, ty + 9.3, 6.8, 9.0, "glass")
    m.box(tx - 3.7, tx - 3.5, ty + 5.0, ty + 8.0, 6.8, 8.8, "glass")                  # vitre latérale
    for dx in (-1.6, 1.6):                                                            # 2 blocs de 6 tubes
        m.prism([(tx + dx - 1.5, ty - 9.5, 5.0), (tx + dx + 1.5, ty - 9.5, 5.0),
                 (tx + dx + 1.5, ty + 2.5, 5.0), (tx + dx - 1.5, ty + 2.5, 5.0)],
                [(tx + dx - 1.5, ty - 9.5, 12.0), (tx + dx + 1.5, ty - 9.5, 12.0),
                 (tx + dx + 1.5, ty + 2.5, 8.0), (tx + dx - 1.5, ty + 2.5, 8.0)], "paint", 0.12)
    for k in range(3):                                                                # séparations des tubes
        z0, z1 = 5.6 + k * 2.0, 7.0 + k * 1.6
        m.prism([(tx - 3.3, ty - 9.5, z0), (tx - 3.1, ty - 9.5, z0), (tx - 3.1, ty + 2.5, z1 - 1.4), (tx - 3.3, ty + 2.5, z1 - 1.4)],
                [(tx - 3.3, ty - 9.5, z0 + 0.5), (tx - 3.1, ty - 9.5, z0 + 0.5), (tx - 3.1, ty + 2.5, z1 - 0.9), (tx - 3.3, ty + 2.5, z1 - 0.9)],
                "dark")
    m.box(tx - 1.2, tx + 1.2, ty - 10.5, ty - 9.5, 1.5, 4.0, "metal")                  # vérin de stabilisation


def pinaka():
    m = Model()
    slab(m, mat="earth", tint=0.05)
    m.box(4, 21, -22, 10, 1.5, 11, "concrete")                                         # hangar (fond)
    arch = [(-16, 11), (16, 11), (12, 14.5), (-12, 14.5)]
    extrude_x(m, [(y - 6, z) for y, z in arch], 4, 21, "metal", 0.1)                   # toit
    m.box(3.5, 4, -18, -4, 1.5, 9, "dark")                                             # porte
    hazard_band(m, 3.4, -19, -3, 9, 10, n=6)
    m.box(3.4, 3.9, 0, 8, 7, 8.5, "paint")                                             # bandeau national
    pinaka_launcher(m, -10, 2)
    for i, (x, y) in enumerate(((-20, -20), (-20, -15.5), (-15.5, -20), (-8, -21))):   # caisses de roquettes
        m.box(x, x + 3.5, y, y + 3.2, 1.5, 3.5 + (i % 2), "olive", 0.1 * (i % 3))
    mast(m, 19, 19, 22, base=1.0, arms=2)
    return m


def pinaka_power_icon():
    m = Model()
    pinaka_launcher(m, 0, 1)
    return m.transformed(lambda x, y, z: (x, y, z - 3))                             # recentré dans l'icône


def jpew_power_icon():
    m = Model()
    for y0 in (-10, 1):
        m.prism([(-3, y0, 0), (3, y0, 0), (3, y0 + 9, 0), (-3, y0 + 9, 0)],
                [(-0.5, y0, 8), (0.5, y0, 8), (0.5, y0 + 9, 8), (-0.5, y0 + 9, 8)], "white", 0.02)
        m.prism([(-3.4, y0 + 0.5, 0.5), (-3.0, y0 + 0.5, 0.5), (-3.0, y0 + 8.5, 0.5), (-3.4, y0 + 8.5, 0.5)],
                [(-0.9, y0 + 0.5, 7.5), (-0.5, y0 + 0.5, 7.5), (-0.5, y0 + 8.5, 7.5), (-0.9, y0 + 8.5, 7.5)], "dark")
    m.box(4, 6, 12, 14, 0, 14, "metal", 0.1)
    for z in (4, 8, 12):
        m.box(3.6, 6.4, 9, 17, z, z + 0.6, "white", 0.1)
    m.box(4.6, 5.4, 12.6, 13.4, 14, 15.2, "red")
    return m.transformed(lambda x, y, z: (x, y - 3.5, z - 3))                       # recentré dans l'icône

# ---------------------------------------------------------------------------
BUILDINGS = {
    # nom : (modèle, couleur d'icône, échelle d'icône, nom affiché)
    "pcscalp": (pcscalp, (60, 80, 150), 0.72, "PC SCALP"),
    "pionier": (pionier, (84, 96, 58), 0.72, "PIONIER"),
    "gchq": (gchq, (150, 132, 92), 0.72, "GCHQ"),
    "pcawacs": (pcawacs, (90, 110, 70), 0.72, "PC AWACS"),
    "pctos": (pctos, (70, 88, 52), 0.72, "PC TOS-1A"),
    "jpew": (jpew, (180, 180, 184), 0.72, "GUERRE EL."),
    "pinaka": (pinaka, (150, 128, 84), 0.72, "PC PINAKA"),
}

POWER_PAINT = {"jpew": (200, 200, 204), "pinaka": (170, 150, 96)}

# Icône dédiée au pouvoir de soutien (sinon le jeu réutilise une icône RA).
POWER_ICONS = {
    # bâtiment : (modèle de l'icône, texte, échelle, orientation)
    "jpew": (jpew_power_icon, "BROUILLAGE", 1.8, 0.86),
    "pinaka": (pinaka_power_icon, "PINAKA", 2.3, 0.62),
}


def stretched(model):
    """Allonge la profondeur pour que l'empreinte couvre exactement 2x2 cases à l'écran,
    et exagère les hauteurs comme sur les sprites RA."""
    k = 1 / math.cos(TILT)
    return model.transformed(lambda x, y, z: (x * k, y, z * HEIGHT))


def damaged(model, seed):
    """Même bâtiment noirci, avec des traces de brûlure."""
    rnd = random.Random(seed)
    m = Model()
    for s in model.solids:
        if s[0] in ("quad", "poly"):
            m.solids.append((s[0], s[1], s[2], s[3] + 0.18))
        else:
            b, t, mat, tint = s
            m.solids.append((b, t, mat, tint + 0.18))
    for _ in range(7):
        x, y = rnd.uniform(-22, 18), rnd.uniform(-22, 18)
        w, d = rnd.uniform(2, 5), rnd.uniform(2, 5)
        m.box(x, x + w, y, y + d, 1.5, 1.8, "burnt")
    return m


def frame(model):
    saved = render.TILT, render.LIGHT
    render.TILT, render.LIGHT = TILT, LIGHT
    try:
        return render.outline(render.render_frame(stretched(model), 0.0, SIZE))
    finally:
        render.TILT, render.LIGHT = saved


def build(name, palette):
    fn, color, icon_scale, title = BUILDINGS[name]
    model = fn()
    frames = [frame(model), frame(damaged(model, name))]
    for i in range(1, MAKE_FRAMES + 1):                 # sort de terre
        k = i / MAKE_FRAMES
        frames.append(frame(model.transformed(lambda x, y, z, k=k: (x, y, z * k))))
    render.save_sheet(frames, os.path.join(OUT, f"{name}.png"), palette)
    icon = render.render_icon(model, palette, scale=icon_scale, facing=0.9, paint=color,
                              bg=((96, 120, 150), (60, 72, 60)))
    render.save_sheet([render.label(icon, title)], os.path.join(OUT, f"{name}icon.png"), palette)
    if name in POWER_ICONS:
        icon_fn, text, scale, facing = POWER_ICONS[name]
        picon = render.render_icon(icon_fn(), palette, scale=scale, facing=facing, paint=POWER_PAINT[name],
                                   bg=((140, 40, 30), (40, 20, 20)))
        render.save_sheet([render.label(picon, text)], os.path.join(OUT, f"{name}power.png"), palette)
    print(f"{name}: {len(frames)} images + icône")


if __name__ == "__main__":
    pal = render.load_palette(sys.argv[1])
    for n in sys.argv[2:] or list(BUILDINGS):
        build(n, pal)
