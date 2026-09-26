"""Modèles 3D simplifiés des véhicules RATC (1 m ~ 3 px, 24 px = 1 case).

Chaque véhicule à tourelle fournit : une caisse (hull), une tourelle (turret)
centrée sur son pivot, et le décalage du pivot par rapport au centre de la caisse.
"""
import math
from render import Model


def ellipse(rx, ry, n=10, cx=0.0, cy=0.0):
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def scaled(poly, fx, fy, dx=0.0):
    return [(x * fx + dx, y * fy) for x, y in poly]


def tracked_running_gear(m, x0, x1, half_w, track_w, skirt=True, skirt_z=3.6, skirt_blocks=0):
    """Chenilles + jupes latérales."""
    for s in (1, -1):
        y_in, y_out = s * (half_w - track_w), s * half_w
        ya, yb = sorted((y_in, y_out))
        m.tapered_box(x0, x1, ya, yb, 0, 2.6, inset_front=1.2, inset_back=1.0, mat="rubber")
        if skirt:
            ys = sorted((y_out - s * 0.2, y_out + s * 0.25))
            m.box(x0 + 1.0, x1 - 1.6, ys[0], ys[1], 1.3, skirt_z, "paint", 0.05)
            if skirt_blocks:
                step = (x1 - x0 - 3) / skirt_blocks
                for i in range(0, skirt_blocks, 2):
                    bx = x0 + 1.2 + i * step
                    m.box(bx, bx + step * 0.9, ys[0] - s * 0.1, ys[1] + s * 0.1, 1.6, skirt_z - 0.1, "paint", 0.15)


def barrel(m, x0, x1, z, r, sleeve=None, evacuator=None, muzzle_brake=False):
    m.cylinder_x(x0, x1, 0, z, r, "metal")
    if sleeve:
        m.cylinder_x(x0, sleeve, 0, z, r * 1.25, "paint", tint=0.1)
    if evacuator:
        m.cylinder_x(evacuator[0], evacuator[1], 0, z, r * 1.5, "paint", tint=0.05)
    if muzzle_brake:
        m.cylinder_x(x1 - 1.2, x1, 0, z, r * 1.5, "metal")


# ---------------------------------------------------------------------------
# Leopard 2A7+ : caisse longue et basse, tourelle à blindage en coin (flèche),
# long canon L55, nuque arrière, périscope PERI R17 sur le toit.
# ---------------------------------------------------------------------------
def leopard():
    hull = Model()
    tracked_running_gear(hull, -12, 12, 5.8, 2.2, skirt_blocks=6)
    hull.box(-12, 9.5, -3.7, 3.7, 1.0, 4.2)                                     # caisse
    hull.tapered_box(9.5, 12.5, -3.7, 3.7, 1.0, 4.2, inset_front=2.6)         # glacis
    hull.box(-12, -5.5, -5.4, 5.4, 3.6, 4.5, "paint", 0.12)                     # plage moteur
    hull.box(-11.5, -8.5, -3.5, 3.5, 4.5, 4.8, "dark")                          # grilles
    hull.box(-12.3, -11.6, -5.0, -3.2, 2.5, 4.2, "paint", 0.2)                  # coffres arrière
    hull.box(-12.3, -11.6, 3.2, 5.0, 2.5, 4.2, "paint", 0.2)
    hull.box(8.5, 10, 1.2, 2.8, 4.2, 4.8, "glass")                              # périscope pilote

    tur = Model()
    wedge = [(-7.5, -4.2), (2.5, -4.7), (7.8, -1.4), (7.8, 1.4), (2.5, 4.7), (-7.5, 4.2)]
    tur.prism([(x, y, 4.2) for x, y in wedge], [(x, y, 7.4) for x, y in scaled(wedge, 0.93, 0.88, -0.2)])
    tur.box(-10, -7.3, -3.6, 3.6, 4.7, 7.0, "paint", 0.06)                      # nuque
    tur.box(6.8, 8.6, -1.1, 1.1, 5.0, 6.7, "paint", 0.1)                        # masque
    barrel(tur, 8.4, 24, 5.8, 0.65, sleeve=15)
    tur.box(-1.5, 0.3, 2.0, 3.2, 7.4, 9.3, "metal")                             # PERI R17
    tur.box(-1.7, 0.5, 1.8, 3.4, 9.3, 9.8, "glass")
    tur.box(3.0, 4.6, -3.4, -2.2, 7.3, 8.3, "glass")                            # viseur tireur
    tur.box(-5, -2.8, -3.0, -1.2, 7.4, 8.4, "dark")                             # tourelleau téléopéré
    tur.cylinder_x(-3, 0.5, -2.1, 8.6, 0.25, "metal")
    return hull, tur, -1.5


# ---------------------------------------------------------------------------
# Challenger 3 : tourelle à flancs plats verticaux (Chobham), toit plat,
# nuque profonde, caméra thermique en caisson au-dessus du canon.
# ---------------------------------------------------------------------------
def challenger():
    hull = Model()
    tracked_running_gear(hull, -12.5, 12.5, 6.0, 2.3, skirt_blocks=0)
    hull.box(-12.5, 9.5, -3.8, 3.8, 1.0, 4.3)
    hull.tapered_box(9.5, 12.8, -3.8, 3.8, 1.0, 4.3, inset_front=1.6)
    hull.box(-12.5, -5, -5.6, 5.6, 3.9, 4.6, "paint", 0.1)
    for gx in (-11.5, -9.5, -7.5):                                             # grilles transversales
        hull.box(gx, gx + 1.2, -4.5, 4.5, 4.6, 4.8, "dark")
    for s in (1, -1):                                                          # jupes à panneaux
        for i, bx in enumerate(range(-11, 10, 4)):
            y0, y1 = sorted((s * 5.9, s * 6.4))
            hull.box(bx, bx + 3.6, y0, y1, 1.2, 3.9, "paint", 0.04 + 0.08 * (i % 2))

    tur = Model()
    slab = [(-8.5, -4.6), (5.2, -4.9), (7.8, -3.4), (7.8, 3.4), (5.2, 4.9), (-8.5, 4.6)]
    tur.extrude(slab, 4.3, 7.3)                                                # flancs verticaux
    tur.box(-12, -8.3, -4.0, 4.0, 4.6, 7.1, "paint", 0.08)                     # nuque profonde
    tur.box(-11.8, -8.6, -4.2, 4.2, 7.1, 7.4, "dark")                          # panier de rangement
    tur.box(7.2, 8.8, -1.3, 1.3, 5.0, 6.9, "paint", 0.12)
    barrel(tur, 8.6, 23.5, 5.9, 0.65, sleeve=12, evacuator=(13.5, 15.5))
    tur.box(4.8, 7.6, -2.9, -1.3, 7.3, 8.9, "dark")                            # caisson thermique
    tur.box(7.4, 7.7, -2.7, -1.5, 7.6, 8.6, "glass")
    tur.box(-3.5, -1.0, 1.6, 3.8, 7.3, 8.8, "metal")                           # vision chef
    tur.box(-3.6, -0.9, 1.5, 3.9, 8.8, 9.2, "glass")
    return hull, tur, -2.5


# ---------------------------------------------------------------------------
# Caisse soviétique T-72/T-90 : compacte et basse, glacis couvert de briques
# ERA, fûts de carburant à l'arrière.
# ---------------------------------------------------------------------------
def soviet_hull(era=True):
    hull = Model()
    tracked_running_gear(hull, -11, 11, 5.6, 2.2, skirt_blocks=0, skirt_z=3.2)
    hull.box(-11, 8.5, -3.6, 3.6, 1.0, 3.8)
    hull.tapered_box(8.5, 11.8, -3.6, 3.6, 1.0, 3.8, inset_front=2.8)
    hull.box(-11, -4.5, -5.3, 5.3, 3.3, 4.1, "paint", 0.1)
    hull.box(-10.5, -7, -3, 3, 4.1, 4.4, "dark")
    for y in (-2.2, 2.2):                                                      # fûts arrière
        hull.cylinder_y(-11.6, y - 1.6, y + 1.6, 4.9, 1.1, "paint", tint=0.18)
    if era:
        for s in (1, -1):                                                      # jupes ERA
            for i, bx in enumerate(range(-2, 10, 3)):
                y0, y1 = sorted((s * 5.4, s * 6.0))
                hull.box(bx, bx + 2.6, y0, y1, 1.4, 3.3, "paint", 0.18 if i % 2 else 0.08)
        for i, y in enumerate((-2.7, -0.9, 0.9, 2.7)):                        # briques du glacis
            hull.tapered_box(9.0, 11.0, y - 0.8, y + 0.8, 3.1, 4.0, inset_front=1.2,
                             mat="paint", tint=0.2 if i % 2 else 0.1)
    return hull


# ---------------------------------------------------------------------------
# T-90M Proryv : tourelle basse et arrondie, blocs Relikt en V à l'avant,
# nuque soudée, canon 2A46M-5 avec manchon thermique.
# ---------------------------------------------------------------------------
def t90m():
    hull = soviet_hull()
    tur = Model()
    dome = ellipse(6.4, 5.0, 12)
    tur.prism([(x, y, 3.8) for x, y in dome], [(x, y, 6.3) for x, y in scaled(dome, 0.72, 0.72, -0.4)])
    tur.box(-9.0, -5.2, -4.0, 4.0, 4.0, 6.0, "paint", 0.08)                    # nuque
    for s in (1, -1):                                                          # blocs Relikt en V
        tur.prism([(1.0, s * 1.4, 3.9), (6.8, s * 1.4, 3.9), (4.2, s * 5.4, 3.9), (0.2, s * 5.2, 3.9)],
                  [(0.8, s * 1.4, 6.2), (6.0, s * 1.4, 6.0), (3.6, s * 4.8, 6.0), (0.2, s * 4.6, 6.2)],
                  "paint", 0.16)
    tur.box(5.6, 7.4, -1.1, 1.1, 4.5, 6.0, "paint", 0.1)
    barrel(tur, 7.2, 22, 5.2, 0.62, sleeve=13, evacuator=(12, 14))
    tur.box(-2.5, 0.2, 1.6, 3.8, 6.3, 7.8, "metal")                            # tourelleau chef
    tur.cylinder_x(-2.0, 2.5, 2.7, 8.0, 0.28, "metal")                         # mitrailleuse
    tur.box(1.5, 3.2, -3.6, -2.2, 6.1, 7.2, "glass")                           # viseur Sosna
    return hull, tur, -0.5


# ---------------------------------------------------------------------------
# BMPT Terminator : caisse de T-72, module d'armes bas avec deux canons 2A42
# de 30 mm côte à côte et deux conteneurs de missiles Ataka sur les flancs.
# ---------------------------------------------------------------------------
def bmpt():
    hull = soviet_hull()
    tur = Model()
    base = [(-6.5, -3.8), (4.5, -3.8), (6.0, -2.0), (6.0, 2.0), (4.5, 3.8), (-6.5, 3.8)]
    tur.prism([(x, y, 3.8) for x, y in base], [(x, y, 5.6) for x, y in scaled(base, 0.9, 0.85)])
    tur.box(-3.0, 4.5, -2.2, 2.2, 5.6, 7.2, "paint", 0.06)                     # berceau des canons
    for y in (-1.0, 1.0):                                                      # 2 x 30 mm
        tur.cylinder_x(4.0, 16, y, 6.4, 0.42, "metal")
        tur.cylinder_x(15, 16, y, 6.4, 0.6, "metal")
    for s in (1, -1):                                                          # conteneurs Ataka
        y0, y1 = sorted((s * 4.2, s * 6.6))
        tur.box(-5.0, 6.5, y0, y1, 5.2, 7.2, "paint", 0.14)
        for ty in (s * 4.8, s * 6.0):
            tur.cylinder_x(6.5, 7.0, ty, 6.2, 0.5, "dark")
    tur.box(-2.5, -0.5, -3.4, -2.2, 7.2, 8.4, "glass")                         # viseur
    tur.box(-5.5, -3.2, 1.0, 3.0, 5.6, 7.0, "metal")                           # lance-grenades AG-17
    return hull, tur, -1.0


# ---------------------------------------------------------------------------
# EBRC Jaguar : 6x6 à caisse facettée, tourelle T40 compacte avec canon
# de 40 mm CTA et lanceur de missiles MMP sur le flanc gauche.
# Pas de tourelle mobile dans le jeu : tout est dans la caisse.
# ---------------------------------------------------------------------------
def jaguar():
    m = Model()
    for x in (7.0, 1.2, -6.8):
        for s in (1, -1):
            y0, y1 = sorted((s * 3.6, s * 5.3))
            m.cylinder_y(x, y0, y1, 2.2, 2.2, "rubber")
            m.cylinder_y(x, (y0 + y1) / 2 - 0.1, (y0 + y1) / 2 + 0.1 + s * 0.8, 2.2, 0.9, "metal")
    m.tapered_box(-11.5, 9.5, -4.4, 4.4, 2.2, 5.6, inset_side=1.0, inset_back=0.4)   # caisse facettée
    m.prism([(9.5, -4.4, 2.2), (12.5, -3.0, 2.8), (12.5, 3.0, 2.8), (9.5, 4.4, 2.2)],
            [(9.5, -3.4, 5.6), (10.8, -2.4, 5.0), (10.8, 2.4, 5.0), (9.5, 3.4, 5.6)])  # nez
    for s in (1, -1):                                                          # garde-boue
        y0, y1 = sorted((s * 3.5, s * 5.4))
        m.box(-9.5, 9.5, y0, y1, 4.1, 4.5, "paint", 0.12)
    m.box(8.2, 9.6, -2.6, 2.6, 5.0, 5.6, "glass")                              # épiscopes pilote
    # Tourelle T40
    t = [(-5.5, -3.2), (2.0, -3.4), (4.0, -1.8), (4.0, 1.8), (2.0, 3.4), (-5.5, 3.2)]
    m.prism([(x - 1.5, y, 5.6) for x, y in t], [(x - 1.7, y, 7.6) for x, y in scaled(t, 0.9, 0.85)], "paint", 0.03)
    m.cylinder_x(2.4, 13.5, 0, 6.4, 0.5, "metal")                              # 40 mm CTA
    m.cylinder_x(12.3, 13.5, 0, 6.4, 0.7, "metal")
    m.box(-5.5, 0.5, 3.4, 5.4, 6.0, 7.8, "paint", 0.15)                        # lanceur MMP
    for tz in (6.5, 7.3):
        m.cylinder_x(0.5, 0.9, 4.4, tz, 0.35, "dark")
    m.box(-3.0, -1.0, -2.6, -1.0, 7.6, 8.8, "glass")                           # viseur chef
    return m


# ---------------------------------------------------------------------------
# Panzerhaubitze 2000 : caisse longue type Leopard 1, énorme tourelle
# rectangulaire en arrière, très long tube de 155 mm L52 avec frein de bouche.
# (Pas de tourelle mobile en jeu : tourelle intégrée à la caisse.)
# ---------------------------------------------------------------------------
def pzh():
    m = Model()
    tracked_running_gear(m, -12.5, 12, 5.8, 2.2, skirt_blocks=0)
    m.box(-12.5, 9, -3.7, 3.7, 1.0, 4.4)
    m.tapered_box(9, 12.3, -3.7, 3.7, 1.0, 4.4, inset_front=2.2)
    m.box(4, 9, -5.4, 5.4, 3.8, 4.8, "paint", 0.1)                              # plage avant (moteur)
    m.box(5, 8, -3.0, 3.0, 4.8, 5.1, "dark")
    m.box(-12.8, -4, -5.4, 5.4, 4.4, 9.2, "paint")                              # tourelle
    m.box(-12.9, -4.2, -5.6, 5.6, 9.2, 9.5, "paint", 0.12)
    m.box(-9, -6.5, 2.0, 4.0, 9.5, 10.6, "glass")                               # vision chef
    m.box(-4.3, -2.6, -1.6, 1.6, 5.2, 8.0, "paint", 0.1)                        # masque
    m.cylinder_x(-2.8, 18.5, 0, 6.6, 0.6, "metal")                              # tube L52
    m.cylinder_x(16.8, 18.8, 0, 6.6, 0.95, "metal")                             # frein de bouche
    m.box(9.8, 11.2, -0.8, 0.8, 4.4, 6.2, "dark")                               # verrou de route
    return m


# ---------------------------------------------------------------------------
# AS-90 : tourelle anguleuse centrale, plus courte et haute, tube L39 plus
# court, coffres de rangement sur les flancs de la tourelle.
# ---------------------------------------------------------------------------
def as90():
    m = Model()
    tracked_running_gear(m, -12, 11.5, 5.6, 2.1, skirt_blocks=0)
    m.box(-12, 8.5, -3.6, 3.6, 1.0, 4.3)
    m.tapered_box(8.5, 11.8, -3.6, 3.6, 1.0, 4.3, inset_front=2.5)
    tur = [(-11, -5.0), (-1.5, -5.0), (1.0, -3.4), (1.0, 3.4), (-1.5, 5.0), (-11, 5.0)]
    m.prism([(x, y, 4.3) for x, y in tur], [(x, y, 9.0) for x, y in scaled(tur, 0.97, 0.9, -0.3)])
    for s in (1, -1):                                                           # coffres latéraux
        y0, y1 = sorted((s * 5.0, s * 6.1))
        m.box(-10, -3, y0, y1, 5.0, 7.8, "paint", 0.15)
    m.box(-7.5, -5.0, -3.8, -1.8, 9.0, 10.1, "glass")
    m.box(0.3, 2.0, -1.5, 1.5, 5.4, 7.8, "paint", 0.1)
    m.cylinder_x(1.5, 15.5, 0, 6.6, 0.6, "metal")                               # tube L39
    m.cylinder_x(8.0, 9.5, 0, 6.6, 0.85, "paint", tint=0.1)                     # évacuateur
    m.cylinder_x(14.2, 15.8, 0, 6.6, 0.9, "metal")
    return m


# ---------------------------------------------------------------------------
# CAESAR : camion 6x6, cabine blindée à l'avant, plateau, obusier de 155 mm
# monté à l'arrière et tube pointé vers l'avant par-dessus la cabine.
# ---------------------------------------------------------------------------
def cesar():
    m = Model()
    for x in (8.5, -3.0, -7.5):
        for s in (1, -1):
            y0, y1 = sorted((s * 2.8, s * 4.4))
            m.cylinder_y(x, y0, y1, 1.9, 1.9, "rubber")
    m.box(-12, 7, -3.4, 3.4, 2.4, 3.6, "dark")                                  # châssis
    m.tapered_box(5.5, 12, -4.0, 4.0, 2.6, 7.4, inset_front=1.6, inset_side=0.4) # cabine blindée
    m.box(10.4, 11.8, -3.2, 3.2, 5.4, 6.9, "glass")                             # pare-brise
    m.box(-12, 5.5, -4.2, 4.2, 3.6, 4.4, "paint", 0.1)                          # plateau
    m.box(-9.5, -4, -2.4, 2.4, 4.4, 6.4, "paint", 0.05)                         # berceau
    m.box(-7.5, -5.5, -2.8, 2.8, 6.0, 7.2, "paint", 0.12)                       # tourillons
    m.cylinder_x(-10.5, 17, 0, 7.6, 0.55, "metal")                              # tube 52 calibres
    m.cylinder_x(15.3, 17.2, 0, 7.6, 0.85, "metal")
    m.box(-13.5, -12, -3.2, 3.2, 1.0, 3.6, "metal")                             # bêche arrière
    return m


# ---------------------------------------------------------------------------
# M777 : obusier tracté ultraléger, deux roues, flèches ouvertes en V
# vers l'arrière, tube de 155 mm long et fin.
# ---------------------------------------------------------------------------
def m777():
    m = Model()
    for s in (1, -1):
        y0, y1 = sorted((s * 3.4, s * 4.8))
        m.cylinder_y(1.0, y0, y1, 2.0, 2.0, "rubber")
        m.prism([(0, s * 1.2, 1.4), (0, s * 2.2, 1.4), (-12, s * 5.2, 0.6), (-12, s * 4.2, 0.6)],
                [(0, s * 1.2, 2.6), (0, s * 2.2, 2.6), (-12, s * 5.2, 1.4), (-12, s * 4.2, 1.4)],
                "paint", 0.08)                                                  # flèches
        yb = sorted((s * 4.0, s * 5.8))
        m.box(-13, -11.5, yb[0], yb[1], 0.2, 1.8, "metal")                      # bêches
    m.box(-3.0, 4.5, -3.0, 3.0, 1.6, 3.6, "paint")                              # affût
    m.box(-1.5, 3.5, -2.2, 2.2, 3.6, 5.6, "paint", 0.06)                        # berceau
    m.cylinder_x(-5.5, 18, 0, 5.4, 0.5, "metal")                                # tube
    m.cylinder_x(16.5, 18.2, 0, 5.4, 0.8, "metal")
    for s in (1, -1):                                                           # récupérateurs
        m.cylinder_x(-2.5, 6, s * 0.9, 4.4, 0.35, "metal")
    return m


# ---------------------------------------------------------------------------
# Leleka-100 : drone aile volante à hélice propulsive, en vol (ombre au sol).
# Agrandi ~2,5x pour rester lisible.
# ---------------------------------------------------------------------------
def leleka():
    m = Model()
    z = 11.0
    wing = [(2.5, 0), (-1.0, 9.5), (-3.2, 9.0), (-2.2, 0), (-3.2, -9.0), (-1.0, -9.5)]
    m.extrude(wing, z, z + 0.7)
    m.tapered_box(-3.5, 5.5, -1.2, 1.2, z - 0.4, z + 1.8, inset_front=2.0, inset_side=0.3, tint=0.05)  # fuselage
    m.box(3.0, 4.2, -0.5, 0.5, z - 0.7, z - 0.2, "glass")                       # caméra
    for s in (1, -1):                                                           # dérives de bout d'aile
        m.box(-3.0, -1.2, s * 9.0 - 0.2, s * 9.0 + 0.2, z + 0.7, z + 2.2, "paint", 0.1)
    m.cylinder_y(-4.0, -3.0, 3.0, z + 0.6, 0.2, "dark")                         # hélice
    return m
