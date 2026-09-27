"""Modèles 3D simplifiés des véhicules RATC (1 m ~ 3 px, 24 px = 1 case).

Chaque véhicule à tourelle fournit : une caisse (hull), une tourelle (turret)
centrée sur son pivot, et le décalage du pivot par rapport au centre de la caisse.
"""
import math
from render import Model, hd_style


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


# ===========================================================================
# ÉLÉMENTS DÉTAILLÉS COMMUNS (véhicules rendus avec hd.py)
# ===========================================================================
# Camouflages : taches en nuances de la couleur du joueur (seuil de bruit, assombrissement).
NATO3 = {"scale": 7.0, "seed": 3, "tones": [(0.32, 0.16), (0.62, 0.0), (1.1, 0.07)]}       # vert/brun/noir OTAN
FR3 = {"scale": 7.0, "seed": 7, "tones": [(0.3, 0.16), (0.58, 0.0), (1.1, 0.07)]}         # Centre-Europe français
UK2 = {"scale": 8.0, "seed": 5, "tones": [(0.4, 0.16), (1.1, 0.0)]}                      # vert et noir britannique
RU3 = {"scale": 8.0, "seed": 11, "tones": [(0.3, 0.15), (0.6, 0.0), (1.1, -0.08)]}      # vert/sable/noir russe
SAND2 = {"scale": 7.0, "seed": 13, "tones": [(0.35, 0.12), (1.1, 0.0)]}                  # uni délavé


def ys(a, b):
    return sorted((a, b))


def hd_tracks(m, x0, x1, y_out, width, wheels, wheel_r=1.05, top=2.6, sprocket="rear"):
    """Chenille en boucle : brins, barbotin denté, poulie de tension, galets avec moyeux."""
    re = top / 2
    for s in (1, -1):
        ya, yb = ys(s * y_out, s * (y_out - width))
        m.box(x0 + re, x1 - re, ya, yb, top - 0.5, top, "rubber")                  # brin supérieur
        m.box(x0 + re, x1 - re, ya, yb, 0.0, 0.5, "rubber")                        # brin au sol
        for x in (x0 + re, x1 - re):                                              # enroulements
            m.cylinder_y(x, ya, yb, re, re, "rubber", sides=12)
        yi = ys(s * (y_out - width), s * (y_out - width + 0.5))
        m.box(x0 + re, x1 - re, yi[0], yi[1], 0.4, top - 0.4, "dark")              # fond entre les galets
        xs_, xi = (x0 + re, x1 - re) if sprocket == "rear" else (x1 - re, x0 + re)
        yo = ys(s * y_out, s * (y_out + 0.2))
        m.cylinder_y(xs_, yo[0], yo[1], re, re * 0.8, "metal", sides=10)          # barbotin
        m.cylinder_y(xs_, *ys(s * (y_out + 0.2), s * (y_out + 0.4)), re, re * 0.35, "dark", sides=6)
        m.cylinder_y(xi, yo[0], yo[1], re, re * 0.7, "metal", sides=10, tint=0.1)  # poulie
        a, b = x0 + re + wheel_r + 0.2, x1 - re - wheel_r - 0.2
        for i in range(wheels):
            x = a + i * (b - a) / max(1, wheels - 1)
            wy = ys(s * (y_out - 0.05), s * (y_out - width + 0.3))
            m.cylinder_y(x, wy[0], wy[1], 0.5 + wheel_r, wheel_r, "rubber", sides=10, tint=0.1)
            hy = ys(s * (y_out - 0.05), s * (y_out + 0.1))
            m.cylinder_y(x, hy[0], hy[1], 0.5 + wheel_r, wheel_r * 0.6, "metal", sides=8)   # moyeu


def hd_skirts(m, x0, x1, y_out, z0, z1, panels, heavy=0, heavy_z0=None, tint=0.0):
    """Jupes latérales en panneaux ; les `heavy` premiers (à l'avant) sont des modules épais."""
    step = (x1 - x0) / panels
    for s in (1, -1):
        for i in range(panels):
            xa, xb = x1 - (i + 1) * step + 0.08, x1 - i * step - 0.08
            if i < heavy:
                m.box(xa, xb, *ys(s * y_out, s * (y_out + 0.9)), heavy_z0 if heavy_z0 is not None else z0 - 0.3,
                      z1, "paint", tint + 0.04 * (i % 2))
                m.box(xa + 0.3, xb - 0.3, *ys(s * (y_out + 0.9), s * (y_out + 1.0)), z1 - 0.6, z1 - 0.3, "dark")
            else:
                m.box(xa, xb, *ys(s * y_out, s * (y_out + 0.35)), z0, z1, "paint", tint + 0.06 + 0.05 * (i % 2))


def wheel(m, x, y_in, y_out, r, z=None, hub=True):
    """Roue de camion / blindé : pneu sculpté, jante et moyeu."""
    z = r if z is None else z
    m.cylinder_y(x, *ys(y_in, y_out), z, r, "rubber", sides=12)
    if hub:
        s = 1 if y_out > y_in else -1
        m.cylinder_y(x, *ys(y_out, y_out + s * 0.12), z, r * 0.62, "metal", sides=10)
        m.cylinder_y(x, *ys(y_out + s * 0.12, y_out + s * 0.3), z, r * 0.28, "dark", sides=6)


def smoke_launchers(m, x, y, z, s, n, spacing=0.6, along="x"):
    """Rangée de lance-pots fumigènes orientés vers l'avant et l'extérieur."""
    for i in range(n):
        px, py = (x + i * spacing, y) if along == "x" else (x, y + s * i * spacing)
        m.tube((px, py, z), (px + 0.7, py + s * 0.7, z + 0.5), 0.3, "dark", sides=6)


def antenna(m, x, y, z, h):
    m.box(x - 0.4, x + 0.4, y - 0.4, y + 0.4, z, z + 0.5, "dark")
    m.tube((x, y, z + 0.5), (x - 0.4, y, z + h), 0.3, "metal", sides=4)


def mg(m, x, y, z, length=3.0, yaw_left=0.0):
    """Mitrailleuse sur affût (canon vers l'avant) avec caisse à munitions."""
    m.box(x - 1.0, x + 0.6, y - 0.4, y + 0.4, z, z + 0.6, "dark")
    m.tube((x, y, z + 0.5), (x + length, y + yaw_left, z + 0.6), 0.25, "metal", sides=4)
    m.box(x - 0.6, x + 0.2, y + 0.4, y + 1.0, z + 0.1, z + 0.6, "olive", 0.1)


def hatch(m, x, y, z, r=1.0, mat="paint", tint=0.14):
    m.cylinder_z(x, y, z, z + 0.3, r, mat, sides=10, tint=tint)
    m.box(x - r * 0.9, x - r * 0.5, y - 0.2, y + 0.2, z + 0.3, z + 0.5, "dark")


def periscope(m, x0, x1, y0, y1, z, h=0.5):
    m.box(x0, x1, y0, y1, z, z + h, "dark")
    m.box(x1 - 0.2, x1 + 0.05, y0 + 0.1, y1 - 0.1, z + 0.1, z + h - 0.05, "glass")


def hd_barrel(m, x0, x1, z, r, sleeves=(), evacuator=None, brake=None, mrs=True, y=0.0):
    """Canon : tube, manchon thermique segmenté, évacuateur de fumées, frein de bouche, référence de bouche."""
    m.cylinder_x(x0, x1, y, z, r, "metal", sides=10)
    for a, b in sleeves:
        m.cylinder_x(a, b, y, z, r * 1.22, "paint", sides=10, tint=0.08)
    if evacuator:
        m.cylinder_x(evacuator[0], evacuator[1], y, z, r * 1.55, "paint", sides=10, tint=0.04)
    if brake:
        m.cylinder_x(x1 - brake, x1, y, z, r * 1.55, "metal", sides=8)
        m.box(x1 - brake * 0.8, x1 - brake * 0.25, y - r * 1.6, y + r * 1.6, z - r * 0.4, z + r * 0.4, "dark")
    if mrs:
        m.box(x1 - 0.9, x1 - 0.3, y - 0.25, y + 0.25, z + r, z + r + 0.45, "metal")


def jerrycans(m, x, y, z, n, s):
    for i in range(n):
        m.box(x + i * 1.0, x + i * 1.0 + 0.85, *ys(y, y + s * 0.7), z, z + 1.3, "olive", 0.05 * (i % 2))


def tow_cable(m, x0, x1, y, z):
    m.tube((x0, y, z), (x1, y, z), 0.28, "dark", sides=4)
    for x in (x0, x1):
        m.box(x - 0.3, x + 0.3, y - 0.35, y + 0.35, z - 0.2, z + 0.3, "metal")


def lights(m, x, y, z, s):
    """Phare avec son garde en tube."""
    m.box(x - 0.4, x + 0.2, *ys(y, y + s * 0.7), z, z + 0.6, "white", 0.05)
    m.box(x + 0.2, x + 0.35, *ys(y + s * 0.1, y + s * 0.6), z + 0.1, z + 0.5, "glass")


# ---------------------------------------------------------------------------
# Leopard 2A7+ : caisse longue et basse, 7 galets, jupes à modules lourds à
# l'avant, module de blindage frontal, plage moteur à grandes grilles, câbles
# de remorquage. Tourelle à blindage espacé en flèche, périscope PERI R17A2,
# viseur EMES 15, tourelleau FLW 200, coffres latéraux et panier arrière,
# 2 x 4 lance-pots, canon L55 à manchon thermique et référence de bouche.
# ---------------------------------------------------------------------------
def leopard():
    hull = Model()
    hd_tracks(hull, -12, 12, 5.8, 2.2, wheels=7)
    hull.box(-11.8, 9.5, -3.6, 3.6, 0.7, 2.8, "dark")                            # ventre
    hull.box(-12, 9.5, -5.6, 5.6, 2.8, 4.2)                                      # caisse
    hull.prism([(9.5, -5.6, 2.8), (12.6, -4.6, 3.6), (12.6, 4.6, 3.6), (9.5, 5.6, 2.8)],
               [(9.5, -5.6, 4.2), (10.8, -4.8, 4.2), (10.8, 4.8, 4.2), (9.5, 5.6, 4.2)])     # glacis
    hull.prism([(9.2, -3.6, 0.8), (11.6, -3.6, 0.8), (11.6, 3.6, 0.8), (9.2, 3.6, 0.8)],
               [(9.2, -3.9, 2.8), (12.9, -3.9, 3.0), (12.9, 3.9, 3.0), (9.2, 3.9, 2.8)], "paint", 0.1)  # nez + module 2A7
    hd_skirts(hull, -11.8, 11.5, 5.6, 1.3, 4.1, panels=7, heavy=3)
    # plage moteur : grandes grilles, prises d'air, coffre de la climatisation
    hull.box(-11.8, -4.5, -4.6, 4.6, 4.2, 4.5, "paint", 0.1)
    hull.box(-11.2, -7.6, -3.8, 3.8, 4.5, 4.7, "dark")
    hull.box(-7.2, -5.0, -3.8, -0.4, 4.5, 4.7, "dark")
    hull.box(-7.2, -5.0, 0.4, 3.8, 4.5, 4.7, "dark")
    hull.box(-12.4, -11.8, -4.8, 4.8, 1.6, 4.2, "dark", 0.1)                      # grille arrière
    for s in (1, -1):
        hull.box(-12.5, -11.6, *ys(s * 3.0, s * 4.8), 2.6, 4.4, "paint", 0.2)    # coffres arrière
        tow_cable(hull, -10.5, 6.0, s * 4.9, 4.35)
        lights(hull, 10.6, s * 4.0, 4.2, s)
        hull.box(12.3, 12.9, *ys(s * 1.6, s * 2.6), 1.6, 2.2, "dark")            # crochets
    # poste de pilotage (à droite) : trappe, épiscopes
    hatch(hull, 8.0, -2.4, 4.2, 0.9)
    periscope(hull, 8.6, 9.3, -3.4, -1.4, 4.2, 0.4)
    hull.box(3.0, 4.4, -5.2, -3.4, 4.2, 4.9, "olive", 0.08)                        # sac d'équipage
    hd_style(hull, camo=NATO3, dust=0.8)

    tur = Model()
    body = [(-7.4, -4.4), (3.0, -4.7), (6.0, -4.2), (6.0, 4.2), (3.0, 4.7), (-7.4, 4.4)]
    tur.prism([(x, y, 4.2) for x, y in body], [(x - 0.2, y * 0.95, 7.2) for x, y in body])
    for s in (1, -1):                                                          # blindage espacé en flèche
        mirrored_prism(tur, [(5.6, 1.2, 4.4), (9.2, 1.2, 4.4), (6.0, 4.9, 4.4), (4.2, 4.9, 4.4)],
                       [(5.6, 1.2, 7.3), (8.6, 1.2, 7.3), (5.8, 4.7, 7.3), (4.2, 4.7, 7.3)], s, "paint", 0.05)
        tur.box(-6.5, -1.5, *ys(s * 4.5, s * 5.3), 4.6, 6.8, "paint", 0.14)       # coffres latéraux
        tur.box(-6.3, -1.7, *ys(s * 5.3, s * 5.4), 6.2, 6.6, "dark")
        for k in range(4):                                                     # lance-pots
            tur.tube((-1.2 + k * 0.7, s * 4.6, 6.9), (-0.6 + k * 0.7, s * 5.4, 7.5), 0.3, "dark")
    tur.box(-10.2, -7.2, -3.8, 3.8, 4.5, 6.9, "paint", 0.06)                    # nuque
    for k in range(6):                                                         # panier arrière
        tur.box(-11.0, -10.7, -3.6 + k * 1.44, -3.3 + k * 1.44, 5.0, 7.3, "dark")
    tur.box(-11.0, -10.2, -3.8, 3.8, 7.0, 7.3, "dark")
    tur.box(-10.9, -10.3, -3.4, 3.4, 5.2, 6.8, "olive", 0.1)                     # paquetage
    tur.box(6.6, 8.6, -1.2, 1.2, 4.9, 6.8, "paint", 0.12)                       # masque
    hd_barrel(tur, 8.4, 24, 5.8, 0.62, sleeves=((9.0, 12.6), (13.0, 15.0), (18.5, 22.4)), evacuator=(15.2, 18.2))
    tur.cylinder_x(7.6, 9.2, 1.7, 5.3, 0.25, "dark")                           # coaxiale
    # PERI R17A2 (chef, à gauche) : colonne et tête
    tur.cylinder_z(-1.2, 2.6, 7.1, 8.8, 0.8, "metal", sides=8)
    tur.box(-2.2, -0.1, 1.7, 3.5, 8.8, 9.9, "paint", 0.06)
    tur.box(-0.1, 0.15, 2.0, 3.2, 9.1, 9.7, "glass")
    # EMES 15 (tireur, à droite) : caisson avec volets
    tur.box(1.6, 4.4, -3.8, -1.8, 7.1, 8.1, "paint", 0.1)
    tur.box(4.4, 4.65, -3.5, -2.1, 7.3, 7.9, "glass")
    hatch(tur, -3.4, 1.8, 7.1, 1.0)                                            # trappe du chef
    hatch(tur, -3.6, -2.4, 7.1, 1.0)                                           # trappe du chargeur
    mg(tur, -3.0, -3.4, 7.4, 3.0)
    # tourelleau téléopéré FLW 200
    tur.box(-6.2, -4.4, -0.2, 1.6, 7.1, 7.7, "dark")
    tur.box(-5.9, -4.6, 0.1, 1.3, 7.7, 8.6, "paint", 0.08)
    tur.tube((-4.8, 0.7, 8.2), (-2.4, 0.7, 8.25), 0.22, "metal", sides=4)
    for y in (-3.0, 3.0):
        antenna(tur, -8.6, y, 6.9, 7.0)
    hd_style(tur, camo=NATO3)
    return hull, tur, -1.5


# ---------------------------------------------------------------------------
# Challenger 3 : jupes à grands modules « Dorchester », grilles anti-roquettes
# à l'arrière, deux fûts de carburant, pilote au centre. Tourelle à flancs
# plats, nuque profonde et coffres, système de protection active Trophy
# (radars aux coins, lanceurs sur les flancs), viseurs Orion, canon L55A1.
# ---------------------------------------------------------------------------
def challenger():
    hull = Model()
    hd_tracks(hull, -12.5, 12.5, 6.0, 2.3, wheels=6)
    hull.box(-12.3, 9.5, -3.7, 3.7, 0.7, 2.9, "dark")
    hull.box(-12.5, 9.5, -5.8, 5.8, 2.9, 4.3)
    hull.prism([(9.5, -5.8, 2.9), (12.8, -4.8, 3.5), (12.8, 4.8, 3.5), (9.5, 5.8, 2.9)],
               [(9.5, -5.8, 4.3), (11.0, -5.0, 4.3), (11.0, 5.0, 4.3), (9.5, 5.8, 4.3)])
    hull.prism([(9.3, -3.7, 0.8), (11.8, -3.7, 0.8), (11.8, 3.7, 0.8), (9.3, 3.7, 0.8)],
               [(9.3, -4.0, 2.9), (13.0, -4.0, 3.1), (13.0, 4.0, 3.1), (9.3, 4.0, 2.9)], "paint", 0.1)
    for s in (1, -1):
        for i, (x0, x1) in enumerate(((5.8, 11.6), (0.4, 5.6), (-5.0, 0.2))):   # modules Dorchester
            hull.box(x0, x1, *ys(s * 5.8, s * 6.9), 1.1, 4.3, "paint", 0.03 + 0.07 * (i % 2))
            for bx in (x0 + 0.8, x1 - 1.2):
                hull.box(bx, bx + 0.4, *ys(s * 6.9, s * 7.0), 3.6, 4.0, "dark")
        for k in range(9):                                                     # grilles anti-roquettes
            x = -12.2 + k * 0.8
            hull.box(x, x + 0.28, *ys(s * 6.0, s * 6.7), 1.2, 4.2, "dark")
        hull.box(-12.3, -5.2, *ys(s * 6.0, s * 6.7), 3.9, 4.25, "dark")
        lights(hull, 11.0, s * 4.1, 4.3, s)
        tow_cable(hull, -10.0, 5.0, s * 5.2, 4.45)
    hull.box(-12.5, -5, -5.0, 5.0, 4.3, 4.6, "paint", 0.1)
    for gx in (-11.6, -9.6, -7.6):
        hull.box(gx, gx + 1.3, -4.2, 4.2, 4.6, 4.8, "dark")
    for y in (-2.1, 2.1):                                                      # fûts arrière
        hull.cylinder_y(-13.3, y - 1.8, y + 1.8, 3.6, 1.15, "paint", sides=10, tint=0.2)
        hull.box(-13.4, -13.2, y - 1.9, y + 1.9, 2.4, 4.8, "dark")
    hatch(hull, 8.6, 0.0, 4.3, 0.9)                                            # pilote au centre
    periscope(hull, 9.2, 9.8, -1.0, 1.0, 4.3, 0.35)
    hd_style(hull, camo=UK2, dust=0.8)

    tur = Model()
    slab = [(-8.6, -4.7), (5.0, -5.0), (7.8, -3.4), (7.8, 3.4), (5.0, 5.0), (-8.6, 4.7)]
    tur.extrude(slab, 4.3, 7.4)
    tur.box(-8.4, 4.8, -4.4, 4.4, 7.4, 7.6, "paint", 0.1)                        # toit
    tur.box(-12.2, -8.4, -4.1, 4.1, 4.6, 7.2, "paint", 0.06)                    # nuque profonde
    for s in (1, -1):
        tur.box(-11.8, -5.5, *ys(s * 4.4, s * 5.4), 4.8, 7.0, "paint", 0.16)    # coffres latéraux
        tur.box(-11.6, -5.7, *ys(s * 5.4, s * 5.5), 6.3, 6.7, "dark")
        # Trophy : radar au coin avant, lanceur sur le flanc
        mirrored_prism(tur, [(5.2, 4.6, 5.0), (7.2, 3.4, 5.0), (7.6, 3.9, 5.0), (5.6, 5.3, 5.0)],
                       [(5.2, 4.6, 7.2), (7.2, 3.4, 7.2), (7.6, 3.9, 7.2), (5.6, 5.3, 7.2)], s, "dark", 0.05)
        tur.box(0.5, 3.6, *ys(s * 5.0, s * 6.0), 6.2, 7.9, "paint", 0.12)
        tur.cylinder_z(2.0, s * 5.5, 7.9, 8.4, 0.6, "metal", sides=8)
        smoke_launchers(tur, 3.2, s * 4.6, 7.0, s, 5, spacing=0.5)
    tur.box(7.2, 8.8, -1.3, 1.3, 5.0, 7.0, "paint", 0.12)
    hd_barrel(tur, 8.6, 23.5, 5.9, 0.64, sleeves=((9.0, 12.0), (16.0, 19.0), (19.3, 22.4)), evacuator=(12.6, 15.6))
    # Orion : viseur du chef (panoramique, gauche) et viseur du tireur (droite)
    tur.cylinder_z(-2.4, 2.8, 7.6, 8.9, 0.9, "metal")
    tur.box(-3.5, -1.2, 1.7, 3.9, 8.9, 10.1, "paint", 0.05)
    tur.box(-1.2, -0.95, 2.1, 3.5, 9.2, 9.9, "glass")
    tur.box(3.2, 5.8, -3.6, -1.4, 7.6, 8.9, "dark", 0.05)
    tur.box(5.8, 6.05, -3.3, -1.7, 7.8, 8.6, "glass")
    hatch(tur, -4.6, -2.4, 7.6, 1.0)
    mg(tur, -4.0, -3.3, 7.9, 2.8)
    for k in range(6):                                                          # panier de nuque
        tur.box(-12.9, -12.5, -3.8 + k * 1.5, -3.5 + k * 1.5, 5.0, 7.6, "dark")
    tur.box(-12.8, -12.3, -3.2, 3.2, 5.3, 7.2, "olive", 0.1)
    for y in (-3.2, 3.2):
        antenna(tur, -10.0, y, 7.2, 7.0)
    hd_style(tur, camo=UK2)
    return hull, tur, -2.5


# ---------------------------------------------------------------------------
# Caisse russe T-72/T-90 : 6 grands galets, jupes caoutchouc avec blindage
# réactif Relikt, glacis couvert de briques ERA, lame de terrassement sous le
# nez, fûts de carburant, grilles anti-roquettes sur l'arrière.
# ---------------------------------------------------------------------------
def russian_hull(camo):
    hull = Model()
    hd_tracks(hull, -11, 11, 5.6, 2.2, wheels=6, wheel_r=1.15)
    hull.box(-10.8, 8.5, -3.4, 3.4, 0.7, 2.8, "dark")
    hull.box(-11, 8.5, -5.4, 5.4, 2.8, 3.9)
    hull.prism([(8.5, -5.4, 2.8), (11.8, -4.2, 3.2), (11.8, 4.2, 3.2), (8.5, 5.4, 2.8)],
               [(8.5, -5.4, 3.9), (9.6, -4.6, 3.9), (9.6, 4.6, 3.9), (8.5, 5.4, 3.9)])
    hull.prism([(8.3, -3.4, 0.8), (10.8, -3.4, 0.8), (10.8, 3.4, 0.8), (8.3, 3.4, 0.8)],
               [(8.3, -3.6, 2.8), (12.0, -3.6, 3.1), (12.0, 3.6, 3.1), (8.3, 3.6, 2.8)], "paint", 0.1)
    hull.box(11.4, 12.6, -4.6, 4.6, 0.9, 1.8, "paint", 0.2)                      # lame de terrassement
    for i, x in enumerate((9.0, 10.3)):                                        # briques ERA du glacis
        for j, y in enumerate((-3.6, -1.8, 0.0, 1.8, 3.6)):
            hull.box(x, x + 1.2, y - 0.85, y + 0.85, 3.9 - i * 0.35, 4.4 - i * 0.35, "paint", 0.12 + 0.08 * ((i + j) % 2))
    for s in (1, -1):
        hull.box(-10.5, 11.5, *ys(s * 5.4, s * 5.75), 1.6, 3.3, "rubber", 0.05)   # jupe caoutchouc
        for i, x0 in enumerate((1.0, 3.6, 6.2, 8.8)):                          # ERA des jupes
            hull.box(x0, x0 + 2.4, *ys(s * 5.7, s * 6.4), 1.5, 3.8, "paint", 0.08 + 0.1 * (i % 2))
        for k in range(8):                                                     # grilles arrière
            x = -10.8 + k * 0.8
            hull.box(x, x + 0.28, *ys(s * 5.8, s * 6.4), 1.4, 3.9, "dark")
        hull.box(-10.9, -4.6, *ys(s * 5.8, s * 6.4), 3.6, 3.95, "dark")
        lights(hull, 9.5, s * 4.3, 3.9, s)
        hull.box(-8.0, -3.0, *ys(s * 4.0, s * 5.3), 3.9, 4.8, "paint", 0.18)    # coffres des garde-boue
    hull.box(-11, -4.5, -4.2, 4.2, 3.9, 4.2, "paint", 0.1)
    hull.box(-10.5, -7, -3, 3, 4.2, 4.4, "dark")
    for y in (-2.2, 2.2):
        hull.cylinder_y(-11.8, y - 1.6, y + 1.6, 4.9, 1.15, "paint", sides=10, tint=0.18)
        hull.box(-11.9, -11.6, y - 1.7, y + 1.7, 3.6, 5.2, "dark")
    hull.cylinder_y(-10.2, -4.2, 4.2, 4.6, 0.5, "dark", sides=6)                # rondin d'auto-désembourbage
    hatch(hull, 7.2, 0.0, 3.9, 0.8)
    periscope(hull, 7.9, 8.4, -0.8, 0.8, 3.9, 0.3)
    return hd_style(hull, camo=camo, dust=0.9)


def relikt_turret(tur, z0, z1):
    """Tourelle coulée arrondie couverte de modules Relikt en V."""
    dome = ellipse(6.4, 5.0, 14)
    tur.prism([(x, y, z0) for x, y in dome], [(x, y, z1) for x, y in scaled(dome, 0.72, 0.72, -0.4)])
    for s in (1, -1):
        mirrored_prism(tur, [(1.0, 1.4, z0 + 0.1), (7.0, 1.4, z0 + 0.1), (4.3, 5.5, z0 + 0.1), (0.2, 5.3, z0 + 0.1)],
                       [(0.8, 1.4, z1 - 0.1), (6.2, 1.4, z1 - 0.3), (3.7, 4.9, z1 - 0.3), (0.2, 4.7, z1 - 0.1)],
                       s, "paint", 0.1)
        for k in range(3):                                                     # joints des modules
            x = 1.6 + k * 1.6
            tur.box(x, x + 0.18, *ys(s * 1.5, s * (5.2 - k * 0.5)), z1 - 0.28, z1 - 0.12, "dark")
        tur.box(-4.6, 0.0, *ys(s * 4.6, s * 5.6), z0 + 0.4, z1 - 0.3, "paint", 0.16)   # ERA latéral


# ---------------------------------------------------------------------------
# T-90M Proryv : tourelle soudée à modules Relikt en V, nuque-coffre à
# munitions entourée d'une cage grillagée, viseur Sosna-U, panoramique PK-5,
# tourelleau Kord, lance-pots 902, tube de schnorchel, cage anti-drones.
# ---------------------------------------------------------------------------
def t90m():
    hull = russian_hull(RU3)
    tur = Model()
    relikt_turret(tur, 3.9, 6.4)
    tur.box(-9.4, -5.0, -4.2, 4.2, 4.0, 6.2, "paint", 0.08)                    # nuque (munitions)
    for k in range(7):                                                         # cage de nuque
        tur.box(-10.3, -10.0, -4.2 + k * 1.4, -3.9 + k * 1.4, 4.2, 6.6, "dark")
    tur.box(-10.3, -9.2, -4.3, 4.3, 6.4, 6.7, "dark")
    tur.box(5.6, 7.4, -1.1, 1.1, 4.6, 6.1, "paint", 0.12)
    hd_barrel(tur, 7.2, 22, 5.2, 0.6, sleeves=((7.8, 10.8), (15.2, 18.2), (18.5, 21.2)), evacuator=(11.2, 14.4), mrs=False)
    tur.box(1.4, 3.6, 2.2, 3.8, 6.2, 7.3, "paint", 0.1)                        # Sosna-U (gauche)
    tur.box(3.6, 3.85, 2.5, 3.5, 6.4, 7.1, "glass")
    tur.cylinder_z(-2.6, -2.6, 6.3, 7.8, 0.75, "metal")                       # PK-5 (droite)
    tur.box(-3.5, -1.6, -3.4, -1.8, 7.8, 8.8, "paint", 0.05)
    tur.box(-1.6, -1.35, -3.2, -2.0, 8.0, 8.6, "glass")
    hatch(tur, -1.6, 1.8, 6.3, 0.9)
    mg(tur, -1.0, -0.8, 7.0, 3.4)                                              # Kord
    for s in (1, -1):                                                          # lance-pots 902 en arc
        for k in range(6):
            a = (k - 2.5) * 0.35
            px, py = 2.6 - k * 0.6, s * (4.9 + 0.3 * math.cos(a))
            tur.tube((px, py, 6.2), (px + 0.6, py + s * 0.6, 6.8), 0.3, "dark")
    tur.tube((-8.8, -3.6, 6.6), (-8.8, 3.6, 6.6), 0.55, "paint", sides=8, tint=0.2)   # schnorchel
    # cage anti-drones au-dessus de la tourelle
    for x, y in ((5.0, 4.4), (5.0, -4.4), (-7.6, 4.4), (-7.6, -4.4)):
        tur.tube((x, y, 6.2), (x, y, 10.6), 0.25, "dark", sides=4)
    for k in range(9):
        x = -7.6 + k * 1.58
        tur.box(x - 0.14, x + 0.14, -4.6, 4.6, 10.5, 10.75, "dark")
    for y in (-4.6, 0.0, 4.6):
        tur.box(-7.8, 5.2, y - 0.14, y + 0.14, 10.5, 10.75, "dark")
    antenna(tur, -7.0, 2.8, 6.4, 6.0)
    hd_style(tur, camo=RU3)
    return hull, tur, -0.5


# ---------------------------------------------------------------------------
# BMPT Terminator : caisse de T-72, module de combat bas, deux canons 2A42 de
# 30 mm dans un carter blindé, deux lanceurs Ataka blindés sur les flancs,
# lance-grenades AG-17 dans les garde-boue avant, viseurs panoramiques.
# ---------------------------------------------------------------------------
def bmpt():
    hull = russian_hull(RU3)
    for s in (1, -1):                                                          # AG-17 avant
        hull.box(8.2, 10.4, *ys(s * 3.6, s * 5.2), 3.9, 5.0, "paint", 0.12)
        hull.cylinder_x(10.4, 12.2, s * 4.4, 4.5, 0.3, "metal")
    tur = Model()
    base = [(-6.8, -4.0), (4.6, -4.0), (6.2, -2.2), (6.2, 2.2), (4.6, 4.0), (-6.8, 4.0)]
    tur.prism([(x, y, 3.9) for x, y in base], [(x, y, 5.8) for x, y in scaled(base, 0.9, 0.86)])
    tur.box(-7.8, -5.6, -3.6, 3.6, 4.0, 5.6, "paint", 0.08)
    # carter des canons : bloc bas au centre, deux 30 mm
    tur.prism([(-3.4, -2.4, 5.8), (4.4, -2.4, 5.8), (5.2, -1.6, 5.8), (5.2, 1.6, 5.8), (4.4, 2.4, 5.8), (-3.4, 2.4, 5.8)],
              [(-3.2, -2.1, 7.4), (4.0, -2.1, 7.4), (4.6, -1.4, 7.1), (4.6, 1.4, 7.1), (4.0, 2.1, 7.4), (-3.2, 2.1, 7.4)],
              "paint", 0.04)
    for y in (-1.0, 1.0):
        tur.cylinder_x(4.6, 15.4, y, 6.5, 0.4, "metal", sides=8)
        tur.cylinder_x(14.4, 16.0, y, 6.5, 0.58, "metal", sides=8)
        tur.cylinder_x(5.0, 7.6, y, 6.5, 0.62, "paint", sides=8, tint=0.1)
    for s in (1, -1):                                                          # lanceurs Ataka
        tur.box(-5.4, 6.8, *ys(s * 4.3, s * 6.8), 5.4, 7.4, "paint", 0.12)
        tur.box(-5.2, 6.6, *ys(s * 4.4, s * 6.7), 7.4, 7.6, "paint", 0.2)
        for ty in (s * 4.95, s * 6.15):
            tur.cylinder_x(6.8, 7.2, ty, 6.4, 0.5, "dark")
        tur.box(-4.0, -1.0, *ys(s * 3.6, s * 4.3), 5.0, 6.8, "dark")           # bras d'élévation
        smoke_launchers(tur, -5.8, s * 3.8, 5.6, s, 4, spacing=0.55)
    tur.box(-2.8, -0.4, -3.6, -2.2, 7.4, 8.6, "paint", 0.06)                    # viseur tireur
    tur.box(-0.4, -0.15, -3.4, -2.4, 7.6, 8.3, "glass")
    tur.cylinder_z(-4.6, 2.8, 5.8, 7.4, 0.7, "metal")                         # panoramique chef
    tur.box(-5.4, -3.8, 2.2, 3.4, 7.4, 8.4, "paint", 0.05)
    tur.box(-3.8, -3.55, 2.4, 3.2, 7.6, 8.2, "glass")
    antenna(tur, -6.4, -2.8, 5.8, 6.0)
    hd_style(tur, camo=RU3)
    return hull, tur, -1.0


# ---------------------------------------------------------------------------
# EBRC Jaguar : 6x6 à caisse facettée, grandes roues, tourelle T40 (40 mm
# CTA), lanceur de 2 missiles MMP relevable, tourelleau téléopéré, coffres,
# rétroviseurs, antennes.
# ---------------------------------------------------------------------------
def jaguar():
    m = Model()
    for x in (7.0, 1.2, -6.8):
        for s in (1, -1):
            wheel(m, x, s * 3.5, s * 5.3, 2.2)
    m.box(-11.0, 10.0, -3.4, 3.4, 1.4, 2.6, "dark")                             # plancher en V
    m.tapered_box(-11.5, 9.5, -4.6, 4.6, 2.4, 5.6, inset_side=1.1, inset_back=0.4)
    m.prism([(9.5, -4.6, 2.4), (12.6, -3.0, 2.9), (12.6, 3.0, 2.9), (9.5, 4.6, 2.4)],
            [(9.5, -3.5, 5.6), (10.9, -2.4, 5.0), (10.9, 2.4, 5.0), (9.5, 3.5, 5.6)])
    for s in (1, -1):
        m.box(-9.8, 9.6, *ys(s * 3.4, s * 5.6), 4.2, 4.6, "paint", 0.12)       # garde-boue
        for x0, x1 in ((-9.6, -4.4), (-3.6, -1.0)):                            # coffres latéraux
            m.box(x0, x1, *ys(s * 4.3, s * 4.9), 2.8, 4.2, "paint", 0.16)
        m.box(9.2, 10.0, *ys(s * 3.4, s * 4.6), 4.8, 5.3, "white", 0.05)        # phares
        m.tube((8.6, s * 3.4, 5.2), (9.4, s * 5.2, 6.0), 0.22, "dark", sides=4)  # rétroviseurs
        m.box(9.2, 9.8, *ys(s * 5.0, s * 5.5), 5.7, 6.5, "glass")
        for k in range(4):                                                     # marchepied
            m.box(-11.9, -11.5, *ys(s * (1.2 + k * 0.1), s * 2.4), 2.4 + k * 0.7, 2.6 + k * 0.7, "dark")
    m.box(8.1, 9.6, -2.8, 2.8, 5.0, 5.6, "glass")                                # épiscopes du pilote
    m.box(-11.7, -11.4, -2.0, 1.2, 2.8, 5.0, "dark", 0.1)                        # porte arrière
    for x in (-8.8, -6.4):
        hatch(m, x, -2.2, 5.6, 0.8)
    # tourelle T40
    t = [(-5.5, -3.3), (2.0, -3.5), (4.1, -1.8), (4.1, 1.8), (2.0, 3.5), (-5.5, 3.3)]
    m.prism([(x - 1.5, y, 5.6) for x, y in t], [(x - 1.7, y, 7.7) for x, y in scaled(t, 0.9, 0.85)], "paint", 0.03)
    m.box(1.8, 3.2, -1.1, 1.1, 5.9, 7.2, "paint", 0.12)
    hd_barrel(m, 2.8, 13.6, 6.4, 0.46, evacuator=(6.0, 8.0), brake=1.2, mrs=False)
    m.box(-5.8, 0.4, 3.3, 5.5, 6.0, 7.9, "paint", 0.15)                         # lanceur MMP
    m.box(-5.6, 0.2, 5.5, 5.6, 6.4, 7.5, "dark")
    for tz in (6.5, 7.4):
        m.cylinder_x(0.4, 0.8, 4.4, tz, 0.4, "dark")
    m.box(-3.4, -1.0, -2.9, -1.1, 7.7, 8.9, "paint", 0.06)                       # viseur PASEO
    m.box(-1.0, -0.75, -2.6, -1.4, 7.9, 8.6, "glass")
    m.box(-6.4, -4.8, -1.2, 0.8, 7.6, 8.2, "dark")                              # tourelleau 7,62
    m.tube((-5.4, -0.2, 8.1), (-3.2, -0.2, 8.15), 0.22, "metal", sides=4)
    for s in (1, -1):
        smoke_launchers(m, -3.2, s * 3.4, 7.2, s, 3, spacing=0.6)
    for y in (-2.6, 2.6):
        antenna(m, -10.4, y, 5.6, 6.0)
    return hd_style(m, camo=FR3, dust=0.8, dust_height=2.8, track_period=1.6)


# ---------------------------------------------------------------------------
# Panzerhaubitze 2000 : caisse longue, moteur à l'avant (grilles), énorme
# tourelle arrière avec trappes, coffres et lance-pots, tube L52 à frein de
# bouche multi-chicanes, verrou de route, tourelleau de mitrailleuse.
# ---------------------------------------------------------------------------
def pzh():
    m = Model()
    hd_tracks(m, -12.5, 12, 5.8, 2.2, wheels=7, sprocket="front")
    m.box(-12.3, 9.0, -3.6, 3.6, 0.7, 2.8, "dark")
    m.box(-12.5, 9, -5.6, 5.6, 2.8, 4.4)
    m.prism([(9, -5.6, 2.8), (12.3, -4.4, 3.4), (12.3, 4.4, 3.4), (9, 5.6, 2.8)],
            [(9, -5.6, 4.4), (10.4, -4.6, 4.4), (10.4, 4.6, 4.4), (9, 5.6, 4.4)])
    hd_skirts(m, -12.2, 11.2, 5.6, 1.4, 4.2, panels=6)
    m.box(1.0, 8.6, -4.8, 2.0, 4.4, 4.9, "paint", 0.1)                            # moteur (avant droit)
    for gx in (1.6, 3.4, 5.2):
        m.box(gx, gx + 1.3, -4.2, 1.4, 4.9, 5.1, "dark")
    hatch(m, 7.6, 3.4, 4.4, 0.9)                                                 # pilote (avant gauche)
    periscope(m, 8.3, 8.9, 2.4, 4.4, 4.4, 0.4)
    for s in (1, -1):
        lights(m, 10.2, s * 4.2, 4.4, s)
        tow_cable(m, -3.0, 8.0, s * 5.0, 4.55)
    # tourelle
    m.box(-12.8, -3.6, -5.4, 5.4, 4.4, 9.0, "paint")
    m.prism([(-3.6, -5.4, 4.4), (-2.4, -4.4, 4.4), (-2.4, 4.4, 4.4), (-3.6, 5.4, 4.4)],
            [(-3.6, -5.4, 9.0), (-3.0, -4.6, 8.6), (-3.0, 4.6, 8.6), (-3.6, 5.4, 9.0)], "paint", 0.06)
    m.box(-12.9, -3.8, -5.6, 5.6, 9.0, 9.3, "paint", 0.12)
    for s in (1, -1):
        m.box(-11.0, -6.0, *ys(s * 5.4, s * 5.5), 5.4, 8.2, "dark", 0.1)        # trappes latérales
        m.box(-11.8, -8.0, *ys(s * 5.5, s * 6.3), 5.0, 6.8, "paint", 0.18)       # coffres
        smoke_launchers(m, -5.0, s * 5.4, 8.2, s, 4, spacing=0.55)
    m.box(-13.3, -12.8, -2.8, 2.8, 5.0, 8.2, "dark", 0.08)                        # trappe de chargement
    m.box(-4.0, -2.2, -1.7, 1.7, 5.2, 8.2, "paint", 0.1)                          # masque
    hd_barrel(m, -2.6, 18.6, 6.6, 0.6, evacuator=(3.0, 6.2), brake=2.2, mrs=False)
    m.box(9.6, 11.2, -1.0, 1.0, 4.4, 6.3, "dark")                                 # verrou de route
    m.box(9.4, 11.4, -1.3, 1.3, 6.0, 6.4, "metal")
    m.cylinder_z(-8.4, 2.6, 9.3, 10.1, 1.2, "paint", tint=0.1)                  # coupole du chef
    periscope(m, -7.6, -6.8, 1.8, 3.4, 10.1, 0.4)
    mg(m, -8.2, -2.6, 9.4, 3.0)
    hatch(m, -10.4, -2.4, 9.3, 1.0)
    for y in (-3.6, 3.6):
        antenna(m, -12.0, y, 9.3, 6.0)
    return hd_style(m, camo=NATO3, dust=0.8)


# ---------------------------------------------------------------------------
# AS-90 : tourelle anguleuse centrale, coffres latéraux, tube L39 à frein de
# bouche et évacuateur, jupes, coupole et mitrailleuse, bêche de transport.
# ---------------------------------------------------------------------------
def as90():
    m = Model()
    hd_tracks(m, -12, 11.5, 5.6, 2.1, wheels=6, sprocket="front")
    m.box(-11.8, 8.5, -3.5, 3.5, 0.7, 2.8, "dark")
    m.box(-12, 8.5, -5.4, 5.4, 2.8, 4.3)
    m.prism([(8.5, -5.4, 2.8), (11.8, -4.2, 3.3), (11.8, 4.2, 3.3), (8.5, 5.4, 2.8)],
            [(8.5, -5.4, 4.3), (10.0, -4.4, 4.3), (10.0, 4.4, 4.3), (8.5, 5.4, 4.3)])
    hd_skirts(m, -11.6, 10.8, 5.4, 1.5, 4.1, panels=5)
    tur = [(-11, -5.0), (-1.5, -5.0), (1.0, -3.4), (1.0, 3.4), (-1.5, 5.0), (-11, 5.0)]
    m.prism([(x, y, 4.3) for x, y in tur], [(x, y, 9.0) for x, y in scaled(tur, 0.97, 0.9, -0.3)])
    m.box(-11.2, -1.6, -4.6, 4.6, 9.0, 9.25, "paint", 0.12)
    for s in (1, -1):
        m.box(-10.2, -3.0, *ys(s * 5.0, s * 6.2), 5.0, 7.8, "paint", 0.15)
        m.box(-10.0, -3.2, *ys(s * 6.2, s * 6.3), 6.6, 7.0, "dark")
        m.box(-9.4, -7.4, *ys(s * 6.3, s * 6.8), 5.4, 6.4, "olive", 0.08)       # bidons
        smoke_launchers(m, -2.4, s * 4.4, 8.0, s, 5, spacing=0.5)
        lights(m, 10.0, s * 4.1, 4.3, s)
        tow_cable(m, -10.0, 6.0, s * 5.1, 4.45)
    hatch(m, 7.4, 2.6, 4.3, 0.9)
    periscope(m, 8.1, 8.7, 1.6, 3.6, 4.3, 0.4)
    m.box(0.2, 2.0, -1.6, 1.6, 5.3, 7.9, "paint", 0.1)
    hd_barrel(m, 1.5, 15.6, 6.6, 0.58, evacuator=(7.8, 9.8), brake=1.8, mrs=False)
    m.box(9.0, 10.4, -0.9, 0.9, 4.3, 6.3, "dark")
    m.box(8.8, 10.6, -1.2, 1.2, 6.0, 6.4, "metal")
    m.cylinder_z(-6.2, -2.6, 9.2, 10.0, 1.1, "paint", tint=0.1)
    periscope(m, -5.6, -4.8, -3.6, -1.8, 10.0, 0.4)
    mg(m, -6.0, -2.0, 10.1, 2.8)
    hatch(m, -7.4, 2.4, 9.2, 1.0)
    for y in (-3.6, 3.6):
        antenna(m, -10.4, y, 9.2, 6.0)
    return hd_style(m, camo=UK2, dust=0.8)


# ---------------------------------------------------------------------------
# CAESAR : camion Renault Sherpa 6x6, cabine blindée vitrée, plateau avec
# coffres à munitions, obusier de 155 mm monté à l'arrière (berceau, freins de
# recul, équilibreurs), tube pointé au-dessus de la cabine, bêche arrière.
# ---------------------------------------------------------------------------
def cesar():
    m = Model()
    for x in (8.5, -3.0, -7.3):
        for s in (1, -1):
            wheel(m, x, s * 2.8, s * 4.5, 1.9)
    m.box(-12, 7.5, -2.4, 2.4, 1.6, 2.6, "dark")                                  # longerons
    m.box(-12, 7, -3.4, 3.4, 2.6, 3.4, "dark", 0.1)                               # châssis
    # cabine blindée (pare-brise incliné, portes, vitres latérales)
    m.prism([(5.4, -4.1, 2.6), (12.2, -4.1, 2.6), (12.2, 4.1, 2.6), (5.4, 4.1, 2.6)],
            [(5.4, -3.8, 7.4), (10.2, -3.8, 7.4), (10.2, 3.8, 7.4), (5.4, 3.8, 7.4)])
    m.prism([(10.2, -3.8, 7.4), (10.2, 3.8, 7.4), (12.2, 3.9, 5.0), (12.2, -3.9, 5.0)],
            [(10.1, -3.4, 7.2), (10.1, 3.4, 7.2), (12.0, 3.5, 5.2), (12.0, -3.5, 5.2)], "glass")
    m.box(11.9, 12.5, -3.8, 3.8, 3.0, 4.8, "dark")                                 # calandre
    for s in (1, -1):
        m.box(6.2, 9.6, *ys(s * 4.0, s * 4.15), 5.2, 6.8, "glass")                # vitres latérales
        m.box(11.6, 12.4, *ys(s * 3.0, s * 3.8), 4.9, 5.4, "white", 0.05)          # phares
        m.tube((10.0, s * 3.8, 6.4), (10.6, s * 5.0, 6.8), 0.2, "dark", sides=4)   # rétroviseurs
        m.box(10.4, 10.8, *ys(s * 4.9, s * 5.3), 6.0, 7.2, "dark")
        m.box(4.4, 6.0, *ys(s * 3.0, s * 4.2), 1.2, 2.6, "dark")                  # marchepied
        m.box(5.6, 8.8, *ys(s * 3.4, s * 4.4), 1.4, 3.4, "paint", 0.2)           # garde-boue avant
        m.box(-9.4, -1.0, *ys(s * 3.6, s * 4.8), 3.0, 3.6, "paint", 0.18)         # garde-boue arrière
        m.box(-0.6, 4.8, *ys(s * 3.2, s * 4.5), 3.4, 5.4, "paint", 0.12)          # coffres à obus
        m.box(-0.4, 4.6, *ys(s * 4.5, s * 4.6), 4.8, 5.1, "dark")
    hatch(m, 7.2, 1.8, 7.4, 0.9)
    m.box(-12, 5.2, -4.2, 4.2, 3.4, 3.9, "paint", 0.1)                             # plateau
    # affût : berceau, tourillons, freins de recul et équilibreurs
    m.box(-10.5, -3.6, -2.4, 2.4, 3.9, 5.8, "paint", 0.04)
    m.box(-8.2, -5.6, -2.9, 2.9, 5.6, 7.4, "paint", 0.12)
    for y in (-1.2, 1.2):
        m.cylinder_x(-7.6, 3.0, y, 7.1, 0.45, "metal", sides=6)
    for s in (1, -1):
        m.tube((-9.6, s * 2.0, 4.2), (-6.6, s * 2.2, 7.4), 0.35, "metal", sides=6)
    hd_barrel(m, -10.5, 17.2, 7.6, 0.55, brake=2.0, mrs=False)
    m.cylinder_x(-2.8, -0.6, 0, 7.6, 0.72, "paint", tint=0.08)
    m.box(12.0, 12.6, -0.8, 0.8, 5.0, 7.3, "dark")                                 # support de tube
    # bêche arrière relevée et vérins
    m.prism([(-13.8, -3.2, 1.0), (-12.4, -3.2, 1.0), (-12.4, 3.2, 1.0), (-13.8, 3.2, 1.0)],
            [(-13.2, -3.2, 3.8), (-12.2, -3.2, 3.8), (-12.2, 3.2, 3.8), (-13.2, 3.2, 3.8)], "metal", 0.1)
    for y in (-2.4, 2.4):
        m.tube((-12.0, y, 3.6), (-13.0, y, 1.8), 0.3, "metal", sides=4)
    antenna(m, 6.2, -3.0, 7.4, 5.0)
    return hd_style(m, camo=FR3, dust=0.8, dust_height=2.6, track_period=1.6)


# ---------------------------------------------------------------------------
# M777 : obusier tracté ultraléger en batterie, flèches ouvertes en V, bêches
# plantées, roues relevées, berceau en titane, freins de recul et
# équilibreurs, tube long et fin à frein de bouche, calculateur de tir.
# ---------------------------------------------------------------------------
def m777():
    m = Model()
    for s in (1, -1):
        wheel(m, 1.2, s * 3.4, s * 4.8, 1.9, z=2.3)
        m.prism([(0, s * 1.2, 1.2), (0, s * 2.2, 1.2), (-12, s * 5.4, 0.4), (-12, s * 4.4, 0.4)],
                [(0, s * 1.2, 2.4), (0, s * 2.2, 2.4), (-12, s * 5.4, 1.2), (-12, s * 4.4, 1.2)],
                "paint", 0.06)                                                  # flèches
        m.box(-8.0, -7.0, *ys(s * 3.2, s * 4.6), 1.0, 1.9, "dark")               # traverse
        m.prism([(-13.2, s * 4.0, 0.0), (-11.6, s * 4.0, 0.0), (-11.6, s * 6.0, 0.0), (-13.2, s * 6.0, 0.0)],
                [(-12.8, s * 4.0, 1.9), (-11.8, s * 4.0, 1.9), (-11.8, s * 6.0, 1.9), (-12.8, s * 6.0, 1.9)],
                "metal", 0.1)                                                   # bêches
        m.tube((-11.2, s * 4.8, 1.2), (-12.4, s * 5.0, 2.4), 0.25, "dark", sides=4)   # poignées
    m.box(-3.4, 4.8, -3.0, 3.0, 0.2, 1.4, "paint", 0.1)                            # plateau de tir
    m.box(-3.0, 4.5, -3.2, 3.2, 1.4, 3.6, "paint")                                 # affût
    m.box(-1.6, 3.6, -2.4, 2.4, 3.6, 5.8, "paint", 0.05)                           # berceau
    hd_barrel(m, -5.5, 18.2, 5.4, 0.48, brake=1.7, mrs=False)
    for s in (1, -1):
        m.cylinder_x(-2.6, 6.2, s * 0.95, 4.5, 0.36, "metal", sides=6)          # freins de recul
        m.tube((-1.8, s * 2.7, 3.2), (2.2, s * 2.3, 6.0), 0.4, "metal", sides=6)   # équilibreurs
    m.box(-1.2, 0.8, 2.6, 3.8, 3.4, 4.8, "dark", 0.05)                             # calculateur DFCS
    m.box(0.8, 0.95, 2.8, 3.6, 3.8, 4.5, "glass")
    return hd_style(m, camo=SAND2, dust=0.9, dust_height=2.0, track_period=1.6)


# ---------------------------------------------------------------------------
# BM-21 Grad sur Oural-375 : capot moteur avancé, cabine vitrée, 6x6, rampe
# de 40 tubes (4 x 10) relevée vers l'avant au-dessus de la cabine.
# ---------------------------------------------------------------------------
def grad():
    m = Model()
    for x in (8.2, -2.6, -6.8):
        for s in (1, -1):
            wheel(m, x, s * 2.7, s * 4.4, 1.8)
    m.box(-11.5, 11.5, -2.2, 2.2, 1.4, 2.4, "dark")
    m.box(-11.5, 4.0, -3.4, 3.4, 2.4, 3.1, "dark", 0.1)
    m.tapered_box(8.0, 12.4, -2.6, 2.6, 2.4, 5.0, inset_front=0.8, inset_side=0.5)   # capot
    m.box(12.2, 12.6, -2.2, 2.2, 2.8, 4.6, "dark")                                  # calandre
    for s in (1, -1):
        m.box(7.0, 11.8, *ys(s * 2.6, s * 4.3), 3.0, 3.7, "paint", 0.14)        # ailes
        m.box(11.4, 12.0, *ys(s * 3.0, s * 3.9), 3.7, 4.3, "white", 0.05)        # phares
        m.box(-9.0, -0.6, *ys(s * 3.3, s * 4.5), 2.9, 3.5, "paint", 0.18)       # garde-boue arrière
        m.box(-0.4, 3.6, *ys(s * 3.2, s * 4.2), 2.6, 4.2, "paint", 0.1)          # coffres
    m.box(4.0, 8.0, -3.8, 3.8, 2.6, 7.2)                                            # cabine
    m.prism([(8.0, -3.6, 5.0), (8.0, 3.6, 5.0), (8.0, 3.6, 7.2), (8.0, -3.6, 7.2)],
            [(8.7, -3.4, 5.0), (8.7, 3.4, 5.0), (8.2, 3.4, 7.0), (8.2, -3.4, 7.0)], "glass")
    for s in (1, -1):
        m.box(5.0, 7.6, *ys(s * 3.8, s * 3.95), 5.2, 6.8, "glass")
    m.box(-11.5, 3.6, -3.6, 3.6, 3.1, 3.6, "paint", 0.1)                            # plateau
    m.box(-7.2, -3.2, -2.2, 2.2, 3.6, 5.2, "paint", 0.05)                           # support tournant
    # rampe de 40 tubes, représentée par 3 rangées de 5 tubes (lisible à cette échelle),
    # relevée de 15° vers l'avant, au-dessus du plateau (la cabine reste dégagée)
    el = math.radians(15)
    x0, x1 = -11.2, 3.2
    rise = (x1 - x0) * math.tan(el)
    m.prism([(x0, -3.6, 5.2), (x1, -3.6, 5.2 + rise), (x1, 3.6, 5.2 + rise), (x0, 3.6, 5.2)],
            [(x0, -3.6, 5.5), (x1, -3.6, 5.5 + rise), (x1, 3.6, 5.5 + rise), (x0, 3.6, 5.5)], "dark")
    for row in range(3):
        for col in range(5):
            y = -2.9 + col * 1.45
            z = 6.0 + row * 1.05
            m.tube((x0, y, z), (x1, y, z + rise), 0.42, "paint", sides=8, tint=0.12 * (col % 2) + 0.05 * row)
            if row == 2 and col < 4:                                               # rainure sombre entre les tubes
                m.tube((x0, y + 0.72, z + 0.2), (x1, y + 0.72, z + rise + 0.2), 0.2, "dark", sides=4)
            m.tube((x1, y, z + rise), (x1 + 0.15, y, z + rise + 0.04), 0.34, "dark", sides=6)   # bouche
    for x in (-10.6, 2.6):                                                         # colliers de la rampe
        zc = 5.2 + (x - x0) * math.tan(el)
        m.box(x - 0.35, x + 0.35, -3.7, 3.7, zc, zc + 3.4, "dark")
    m.box(-4.4, -3.0, -1.2, 1.2, 3.6, 5.6, "metal")                                 # vérin d'élévation
    antenna(m, 4.6, -3.2, 7.2, 4.0)
    return hd_style(m, camo=RU3, dust=0.9, dust_height=2.6, track_period=1.6)


# ---------------------------------------------------------------------------
# Camion de ravitaillement : 6x6 militaire à cabine avancée, benne bâchée
# (arceaux visibles), jerricans, roue de secours, marchepieds.
# ---------------------------------------------------------------------------
def ravit():
    m = Model()
    for x in (8.0, -3.4, -7.4):
        for s in (1, -1):
            wheel(m, x, s * 2.8, s * 4.4, 1.8)
    m.box(-11.5, 11.0, -2.2, 2.2, 1.4, 2.4, "dark")
    m.box(-11.5, 5.0, -3.4, 3.4, 2.4, 3.1, "dark", 0.1)
    m.tapered_box(5.2, 11.6, -3.9, 3.9, 2.4, 7.6, inset_front=0.9, inset_side=0.3)     # cabine
    m.box(11.3, 11.9, -3.3, 3.3, 5.0, 7.0, "glass")
    m.box(11.6, 12.1, -3.4, 3.4, 2.8, 4.6, "dark")                                   # calandre
    for s in (1, -1):
        m.box(6.2, 9.8, *ys(s * 3.75, s * 3.95), 5.2, 6.9, "glass")
        m.box(11.4, 12.0, *ys(s * 2.6, s * 3.5), 4.8, 5.3, "white", 0.05)
        m.tube((9.6, s * 3.8, 6.4), (10.2, s * 4.9, 6.8), 0.2, "dark", sides=4)
        m.box(10.0, 10.4, *ys(s * 4.8, s * 5.2), 5.8, 7.0, "dark")
        m.box(6.0, 9.4, *ys(s * 3.4, s * 4.4), 1.4, 3.3, "paint", 0.2)             # ailes
        m.box(-10.2, -0.6, *ys(s * 3.5, s * 4.6), 2.8, 3.4, "paint", 0.18)
        jerrycans(m, 1.2, s * 3.5, 2.6, 3, s)
    # benne bâchée : ridelles + bâche en arc sur arceaux
    m.box(-11.8, 4.6, -4.1, 4.1, 3.1, 4.8, "paint", 0.1)
    arc = [(-4.1, 4.8), (-4.0, 6.8), (-3.1, 8.3), (-1.4, 8.9), (1.4, 8.9), (3.1, 8.3), (4.0, 6.8), (4.1, 4.8)]
    for (ya, za), (yb, zb) in zip(arc, arc[1:]):
        m.prism([(-11.8, ya, za), (4.6, ya, za), (4.6, yb, zb), (-11.8, yb, zb)],
                [(-11.8, ya * 0.97, za + 0.01), (4.6, ya * 0.97, za + 0.01), (4.6, yb * 0.97, zb + 0.01),
                 (-11.8, yb * 0.97, zb + 0.01)], "olive", 0.2)
    for x in (-9.0, -5.0, -1.0, 3.0):                                                # arceaux sous la bâche
        for (ya, za), (yb, zb) in zip(arc, arc[1:]):
            m.tube((x, ya * 1.02, za + 0.05), (x, yb * 1.02, zb + 0.05), 0.3, "olive", sides=4, tint=0.4)
    m.box(-11.9, -11.8, -3.6, 3.6, 4.8, 8.4, "olive", 0.18)                          # rabat arrière
    return hd_style(m, camo=None, dust=0.9, dust_height=2.6, track_period=1.6)


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


# ===========================================================================
# JAPON
# ===========================================================================
# ---------------------------------------------------------------------------
# Type 10 : char léger et compact (44 t), caisse basse, tourelle à blindage
# modulaire en coin aux flancs plats, nuque de rangement, canon de 120 mm
# sans manchon épais, jupes à plaques.
# ---------------------------------------------------------------------------
def type10():
    hull = Model()
    tracked_running_gear(hull, -11, 11, 5.4, 2.1, skirt_blocks=6)
    hull.box(-11, 8.5, -3.5, 3.5, 1.0, 3.9)
    hull.tapered_box(8.5, 11.4, -3.5, 3.5, 1.0, 3.9, inset_front=2.2)
    hull.box(-11, -4.5, -5.1, 5.1, 3.4, 4.2, "paint", 0.1)
    hull.box(-10.5, -7.5, -3.2, 3.2, 4.2, 4.5, "dark")
    hull.box(7.6, 9.0, 1.0, 2.4, 3.9, 4.4, "glass")

    tur = Model()
    wedge = [(-6.5, -4.3), (3.0, -4.5), (7.4, -1.6), (7.4, 1.6), (3.0, 4.5), (-6.5, 4.3)]
    tur.extrude(wedge, 3.9, 6.6)                                                # flancs plats
    tur.box(-9.5, -6.2, -3.8, 3.8, 4.2, 6.4, "paint", 0.08)                     # nuque
    tur.box(6.6, 8.0, -1.0, 1.0, 4.5, 6.2, "paint", 0.12)                       # masque
    barrel(tur, 7.8, 22, 5.3, 0.6)
    tur.box(1.5, 3.2, 2.2, 3.6, 6.6, 7.9, "glass")                              # viseur chef
    tur.box(2.4, 3.8, -3.5, -2.3, 6.6, 7.4, "glass")                            # viseur tireur
    tur.box(-3.5, -1.5, 1.0, 2.8, 6.6, 7.4, "metal")
    tur.cylinder_x(-2.5, 1.5, 1.9, 7.6, 0.22, "metal")                          # mitrailleuse
    return hull, tur, -1.0


# ---------------------------------------------------------------------------
# Type 16 : blindé à roues 8x8, caisse haute à nez pointu, tourelle
# anguleuse avec canon de 105 mm à frein de bouche.
# ---------------------------------------------------------------------------
def type16():
    hull = Model()
    for x in (8.0, 3.5, -3.0, -7.5):
        for s in (1, -1):
            y0, y1 = sorted((s * 3.4, s * 5.0))
            hull.cylinder_y(x, y0, y1, 2.1, 2.1, "rubber")
            hull.cylinder_y(x, (y0 + y1) / 2 - 0.1, (y0 + y1) / 2 + 0.1 + s * 0.7, 2.1, 0.8, "metal")
    hull.tapered_box(-11, 9, -4.3, 4.3, 2.2, 5.4, inset_side=0.8, inset_back=0.3)
    hull.prism([(9, -4.3, 2.2), (12.5, -2.6, 3.0), (12.5, 2.6, 3.0), (9, 4.3, 2.2)],
               [(9, -3.5, 5.4), (10.5, -2.2, 4.9), (10.5, 2.2, 4.9), (9, 3.5, 5.4)])
    for s in (1, -1):
        y0, y1 = sorted((s * 3.3, s * 5.2))
        hull.box(-9.5, 10, y0, y1, 4.2, 4.6, "paint", 0.12)
    hull.box(8.0, 9.4, 1.0, 3.0, 5.2, 5.8, "glass")

    tur = Model()
    t = [(-6.0, -3.6), (2.5, -3.8), (5.5, -1.6), (5.5, 1.6), (2.5, 3.8), (-6.0, 3.6)]
    tur.prism([(x, y, 5.4) for x, y in t], [(x - 0.3, y, 7.8) for x, y in scaled(t, 0.9, 0.85)])
    tur.box(-8.5, -5.8, -3.0, 3.0, 5.6, 7.6, "paint", 0.1)                      # nuque
    barrel(tur, 5.2, 19.5, 6.6, 0.5, muzzle_brake=True)
    tur.box(0.5, 2.0, 2.0, 3.3, 7.6, 8.7, "glass")
    tur.box(1.5, 2.8, -3.2, -2.2, 7.6, 8.3, "glass")
    return hull, tur, -1.5


# ---------------------------------------------------------------------------
# Type 19 : camion 8x8 à cabine blindée, obusier de 155 mm monté à l'arrière,
# tube pointé vers l'avant au-dessus de la cabine (comme le CAESAR, en plus long).
# ---------------------------------------------------------------------------
def type19():
    m = Model()
    for x in (9.0, 5.0, -4.0, -8.0):
        for s in (1, -1):
            y0, y1 = sorted((s * 2.9, s * 4.5))
            m.cylinder_y(x, y0, y1, 1.9, 1.9, "rubber")
    m.box(-12.5, 7.5, -3.4, 3.4, 2.4, 3.6, "dark")                              # châssis
    m.tapered_box(6.5, 12.8, -4.1, 4.1, 2.6, 7.6, inset_front=1.2, inset_side=0.4)  # cabine
    m.box(11.3, 12.4, -3.3, 3.3, 5.6, 7.0, "glass")
    m.box(-12.5, 6.0, -4.3, 4.3, 3.6, 4.4, "paint", 0.1)                        # plateau
    m.box(-10.5, -4.5, -2.6, 2.6, 4.4, 6.8, "paint", 0.04)                      # berceau
    m.box(-8.5, -6.3, -3.0, 3.0, 6.2, 7.6, "paint", 0.14)
    m.cylinder_x(-11.5, 18.5, 0, 8.0, 0.55, "metal")                            # tube 52 calibres
    m.cylinder_x(16.8, 18.7, 0, 8.0, 0.85, "metal")
    for s in (1, -1):                                                           # coffres latéraux
        y0, y1 = sorted((s * 4.3, s * 5.0))
        m.box(-2.0, 5.5, y0, y1, 3.0, 4.4, "paint", 0.16)
    m.box(-14.0, -12.5, -3.2, 3.2, 1.0, 3.6, "metal")                           # bêche
    return m


# ===========================================================================
# INDE
# ===========================================================================
# ---------------------------------------------------------------------------
# Arjun Mk1A : char lourd massif (68 t), caisse haute et longue, tourelle
# volumineuse à flancs verticaux et blocs de blindage réactif, canon de
# 120 mm avec manchon thermique.
# ---------------------------------------------------------------------------
def arjun():
    hull = Model()
    tracked_running_gear(hull, -12.5, 12.5, 6.0, 2.3, skirt_blocks=0, skirt_z=3.8)
    hull.box(-12.5, 9.5, -3.9, 3.9, 1.0, 4.5)
    hull.tapered_box(9.5, 12.8, -3.9, 3.9, 1.0, 4.5, inset_front=2.0)
    hull.box(-12.5, -5, -5.7, 5.7, 4.0, 4.8, "paint", 0.1)
    hull.box(-12, -8, -3.8, 3.8, 4.8, 5.1, "dark")
    for s in (1, -1):                                                           # blindage réactif des jupes
        for i, bx in enumerate(range(-1, 11, 3)):
            y0, y1 = sorted((s * 5.9, s * 6.5))
            hull.box(bx, bx + 2.6, y0, y1, 1.4, 3.8, "paint", 0.18 if i % 2 else 0.08)

    tur = Model()
    slab_ = [(-8.0, -4.9), (4.8, -5.1), (7.6, -3.2), (7.6, 3.2), (4.8, 5.1), (-8.0, 4.9)]
    tur.extrude(slab_, 4.5, 7.8)
    tur.box(-11.5, -7.8, -4.2, 4.2, 4.8, 7.6, "paint", 0.08)                    # nuque
    for s in (1, -1):                                                           # blocs ERA de tourelle
        y0, y1 = sorted((s * 3.4, s * 5.4))
        tur.box(3.5, 7.4, y0, y1, 5.0, 7.4, "paint", 0.2)
    tur.box(7.0, 8.8, -1.3, 1.3, 5.2, 7.4, "paint", 0.12)
    barrel(tur, 8.6, 23.5, 6.3, 0.66, sleeve=13, evacuator=(13, 15))
    tur.box(-3.0, -0.5, 1.8, 4.0, 7.8, 9.3, "metal")                            # coupole du chef
    tur.box(-3.1, -0.4, 1.7, 4.1, 9.3, 9.7, "glass")
    tur.box(3.0, 4.8, -3.4, -2.0, 7.8, 8.8, "glass")
    return hull, tur, -2.0


# ---------------------------------------------------------------------------
# NAMICA : chasseur de chars sur châssis BMP-2, lanceur de 8 missiles Nag
# relevable monté sur le toit (pas de tourelle mobile en jeu).
# ---------------------------------------------------------------------------
def namica():
    m = Model()
    tracked_running_gear(m, -10.5, 10.5, 5.0, 1.9, skirt=False)
    m.box(-10.5, 7.0, -3.4, 3.4, 1.0, 4.4)
    m.prism([(7.0, -3.4, 1.0), (11.2, -3.4, 1.0), (11.2, 3.4, 1.0), (7.0, 3.4, 1.0)],
            [(7.0, -3.4, 4.4), (8.0, -3.4, 4.4), (8.0, 3.4, 4.4), (7.0, 3.4, 4.4)])         # nez en coin
    m.box(-10.5, -2.0, -4.6, 4.6, 3.6, 4.4, "paint", 0.12)                      # garde-boue
    m.box(-8.0, 3.0, -3.0, 3.0, 4.4, 5.2, "paint", 0.06)                        # socle du lanceur
    # lanceur : 2 rangées de 4 tubes, légèrement relevé vers l'avant
    m.prism([(-7.5, -3.2, 5.2), (4.0, -3.2, 5.2), (4.0, 3.2, 5.2), (-7.5, 3.2, 5.2)],
            [(-7.5, -3.2, 7.4), (4.0, -3.2, 8.6), (4.0, 3.2, 8.6), (-7.5, 3.2, 7.4)], "paint", 0.14)
    for i in range(4):
        for j in range(2):
            y = -2.4 + i * 1.6
            z = 6.1 + j * 1.3
            m.box(4.0, 4.4, y - 0.55, y + 0.55, z + 0.5, z + 1.5, "dark")
    m.box(-9.5, -8.0, -2.0, -0.5, 5.2, 6.8, "glass")                            # viseur
    m.box(6.5, 7.6, -2.6, -1.0, 4.4, 5.0, "glass")
    return m


# ---------------------------------------------------------------------------
# Dhanush : obusier tracté de 155 mm (dérivé du FH-77), flèches ouvertes,
# grand bouclier, groupe auxiliaire de propulsion à l'avant de l'affût.
# ---------------------------------------------------------------------------
def dhanush():
    m = Model()
    for s in (1, -1):
        for x in (1.5, -1.5):
            y0, y1 = sorted((s * 3.6, s * 5.0))
            m.cylinder_y(x, y0, y1, 1.9, 1.9, "rubber")
        m.prism([(0, s * 1.3, 1.4), (0, s * 2.4, 1.4), (-12.5, s * 5.6, 0.6), (-12.5, s * 4.5, 0.6)],
                [(0, s * 1.3, 2.8), (0, s * 2.4, 2.8), (-12.5, s * 5.6, 1.4), (-12.5, s * 4.5, 1.4)],
                "paint", 0.08)                                                  # flèches
        m.box(-13.5, -12, *sorted((s * 4.2, s * 6.2)), 0.2, 1.8, "metal")       # bêches
    m.box(-3.5, 5.0, -3.2, 3.2, 1.6, 3.8, "paint")                              # affût
    m.box(3.5, 7.0, -2.6, 2.6, 1.6, 4.6, "paint", 0.1)                          # groupe auxiliaire
    m.box(6.8, 7.1, -1.8, 1.8, 2.4, 4.0, "dark")
    m.box(-1.5, 3.5, -2.4, 2.4, 3.8, 6.0, "paint", 0.05)                        # berceau
    m.box(2.5, 3.2, -4.0, 4.0, 3.8, 7.2, "paint", 0.14)                         # bouclier
    m.cylinder_x(-6.0, 19, 0, 5.6, 0.55, "metal")                               # tube
    m.cylinder_x(17.2, 19.2, 0, 5.6, 0.85, "metal")
    for s in (1, -1):
        m.cylinder_x(-3.0, 6.5, s * 1.0, 4.5, 0.35, "metal")                    # récupérateurs
    return m


# ===========================================================================
# FRANCE — Leclerc XLR
# ===========================================================================
def ccw(poly):
    """Remet un polygone (x, y) dans le sens antihoraire (normales tournées vers l'extérieur)."""
    area = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
               for i in range(len(poly)))
    return poly if area > 0 else poly[::-1]


def mirrored_prism(m, bottom, top, s, mat="paint", tint=0.0):
    """Prisme défini pour le côté gauche (y > 0), reflété en y selon s, sens corrigé."""
    b = [(x, s * y, z) for x, y, z in bottom]
    t = [(x, s * y, z) for x, y, z in top]
    if s < 0:
        b, t = b[::-1], t[::-1]
    m.prism(b, t, mat, tint)


# ---------------------------------------------------------------------------
# Leclerc XLR. Caisse longue et basse, glacis très incliné, pilote à gauche,
# modules de blindage XLR sur l'avant des jupes et grilles anti-roquettes sur
# l'arrière, grilles moteur, deux fûts de carburant transversaux à l'arrière.
# Tourelle basse à blindage avant en V (série 2), longue nuque du chargeur
# automatique avec cage grillagée, canon CN120-26 L52 à manchon thermique
# segmenté et référence de bouche, viseur panoramique HL-70 du chef (gauche),
# viseur HL-60 du tireur (droite), tourelleau téléopéré, lance-pots GALIX sur
# les flancs, antennes SCORPION et brouilleur anti-IED sur la nuque.
# ---------------------------------------------------------------------------
def leclerc():
    hull = Model()
    # --- Train de roulement : chenilles, barbotin arrière et poulie avant visibles
    for s in (1, -1):
        y_in, y_out = s * 3.6, s * 5.7
        ya, yb = sorted((y_in, y_out))
        hull.tapered_box(-11.2, 11.2, ya, yb, 0, 2.5, inset_front=1.3, inset_back=1.1, mat="rubber")
        hull.cylinder_y(-10.6, ya + 0.2, yb - 0.2, 1.4, 1.2, "metal", tint=0.2)    # barbotin
        hull.cylinder_y(10.7, ya + 0.2, yb - 0.2, 1.5, 1.0, "metal", tint=0.2)     # poulie de tension
    # --- Caisse
    hull.box(-11.5, 7.8, -3.6, 3.6, 1.0, 3.9)
    hull.tapered_box(7.8, 11.9, -3.6, 3.6, 1.0, 3.9, inset_front=3.0)             # glacis très incliné
    hull.box(11.4, 12.1, -3.2, 3.2, 1.0, 1.9, "paint", 0.15)                       # plaque inférieure
    for s in (1, -1):
        # garde-boue avant, relevés vers le nez
        mirrored_prism(hull, [(6.5, 3.6, 3.3), (11.8, 3.6, 2.6), (11.8, 5.9, 2.6), (6.5, 5.9, 3.3)],
                       [(6.5, 3.6, 3.8), (11.8, 3.6, 3.1), (11.8, 5.9, 3.1), (6.5, 5.9, 3.8)], s, "paint", 0.08)
        # modules de blindage XLR sur l'avant des jupes (épais, en 3 blocs)
        for i, (x0, x1) in enumerate(((0.8, 4.0), (4.2, 7.4), (7.6, 10.4))):
            y0, y1 = sorted((s * 5.8, s * 6.7))
            hull.box(x0, x1, y0, y1, 1.2, 3.9, "paint", 0.04 + 0.1 * (i % 2))
            hull.box(x0 + 0.3, x1 - 0.3, *sorted((s * 6.7, s * 6.8)), 3.4, 3.6, "dark")   # fixations
        # jupes arrière plus minces
        y0, y1 = sorted((s * 5.7, s * 6.1))
        hull.box(-6.0, 0.6, y0, y1, 1.4, 3.7, "paint", 0.1)
        # grilles anti-roquettes (slat armour) sur l'arrière des flancs
        for k in range(8):
            x = -11.2 + k * 0.72
            hull.box(x, x + 0.25, *sorted((s * 6.1, s * 6.6)), 1.3, 3.8, "dark")
        hull.box(-11.3, -5.9, *sorted((s * 6.1, s * 6.6)), 3.6, 3.9, "dark")
        # coffres de rangement sur les garde-boue arrière
        hull.box(-9.5, -5.5, *sorted((s * 3.9, s * 5.6)), 3.9, 4.8, "paint", 0.18)
        # phares et feux de gabarit
        hull.box(11.2, 11.7, *sorted((s * 2.5, s * 3.3)), 3.0, 3.5, "glass")
        hull.box(11.8, 12.3, *sorted((s * 1.6, s * 2.4)), 1.3, 1.8, "dark")          # crochets de remorquage
    # --- Plage arrière : grilles moteur (groupe 1500 ch)
    hull.box(-11.5, -4.5, -3.6, 3.6, 3.9, 4.3, "paint", 0.1)
    for gx in (-11.0, -9.6, -8.2):
        hull.box(gx, gx + 1.0, -3.0, 3.0, 4.3, 4.45, "dark")
    hull.box(-7.0, -5.2, -3.3, 3.3, 4.3, 4.5, "dark", 0.1)                         # prises d'air
    # --- Fûts de carburant transversaux (signature du Leclerc)
    for y0, y1 in ((0.4, 3.5), (-3.5, -0.4)):
        hull.cylinder_y(-12.5, y0, y1, 3.8, 1.05, "paint", tint=0.22, sides=10)
    hull.box(-12.3, -11.5, -3.6, 3.6, 2.6, 3.0, "metal", 0.1)                      # berceau des fûts
    # --- Poste de pilotage (à gauche) : trappe et épiscopes
    hull.box(6.2, 7.8, 1.0, 2.9, 3.9, 4.2, "paint", 0.12)
    hull.box(7.6, 8.0, 1.1, 2.8, 4.0, 4.4, "glass")
    hull.box(5.0, 6.0, -2.8, -1.4, 3.9, 4.15, "dark")                              # trappe de visite

    # --- Tourelle (pivot en 0,0)
    tur = Model()
    body = [(-7.0, -4.5), (3.8, -4.7), (7.4, -2.4), (8.0, -1.3), (8.0, 1.3), (7.4, 2.4), (3.8, 4.7), (-7.0, 4.5)]
    tur.prism([(x, y, 3.9) for x, y in body], [(x - 0.2, y * 0.96, 6.7) for x, y in body])   # caisse de tourelle basse
    tur.box(-7.6, 3.5, -4.25, 4.25, 6.7, 6.95, "paint", 0.1)                                 # toit
    # blindage avant en V de la série 2 (modules espacés, de part et d'autre du canon)
    for s in (1, -1):
        mirrored_prism(tur, [(4.2, 1.5, 4.1), (9.4, 1.5, 4.1), (6.6, 5.1, 4.1), (3.6, 5.0, 4.1)],
                       [(4.2, 1.5, 6.7), (9.0, 1.5, 6.7), (6.4, 4.9, 6.7), (3.6, 4.8, 6.7)], s, "paint", 0.06)
        mirrored_prism(tur, [(8.9, 1.5, 6.7), (9.4, 1.5, 4.1), (6.6, 5.1, 4.1), (6.4, 4.9, 6.7)],
                       [(9.0, 1.7, 6.8), (9.5, 1.7, 4.2), (6.7, 5.3, 4.2), (6.5, 5.1, 6.8)], s, "paint", 0.2)  # arête
    # nuque du chargeur automatique, longue et plate
    tur.box(-11.4, -6.8, -4.2, 4.2, 4.2, 6.7, "paint", 0.05)
    tur.box(-11.2, -7.0, -4.0, 4.0, 6.7, 6.9, "paint", 0.14)
    # cage grillagée (slat) autour de la nuque
    for k in range(7):
        y = -4.0 + k * 1.33
        tur.box(-12.4, -12.1, y - 0.12, y + 0.12, 4.4, 7.1, "dark")
    tur.box(-12.4, -11.4, -4.1, 4.1, 6.9, 7.2, "dark")
    for s in (1, -1):
        for k in range(5):
            x = -11.6 + k * 1.0
            tur.box(x - 0.12, x + 0.12, *sorted((s * 4.3, s * 4.6)), 4.4, 7.0, "dark")
    # mantelet et canon CN120-26 L52 : manchon thermique segmenté, référence de bouche
    tur.box(7.8, 9.6, -1.25, 1.25, 4.5, 6.5, "paint", 0.12)
    barrel(tur, 9.4, 23.6, 5.5, 0.6)
    for x0, x1 in ((9.6, 12.6), (12.9, 15.9), (16.2, 19.2), (19.5, 22.2)):          # segments du manchon
        tur.cylinder_x(x0, x1, 0, 5.5, 0.72, "paint", tint=0.1)
    tur.cylinder_x(23.0, 23.6, 0, 5.5, 0.68, "metal")                              # bouche
    tur.box(22.4, 23.0, -0.25, 0.25, 6.1, 6.5, "metal")                            # référence de bouche (MRS)
    tur.cylinder_x(8.4, 10.2, 1.9, 5.2, 0.24, "dark")                              # coaxiale 12,7 mm (gauche)
    # viseur panoramique HL-70 du chef (gauche) : colonne haute et tête stabilisée
    tur.box(0.4, 2.6, 1.6, 3.6, 6.9, 8.4, "metal", 0.1)
    tur.box(0.1, 2.9, 1.3, 3.9, 8.4, 9.9, "paint", 0.04)
    tur.box(2.9, 3.15, 1.8, 3.4, 8.8, 9.6, "glass")
    tur.box(0.1, 2.9, 1.3, 3.9, 9.9, 10.15, "paint", 0.18)
    # viseur HL-60 du tireur (droite), caisson bas vitré vers l'avant
    tur.box(3.2, 5.8, -3.8, -1.6, 6.9, 8.0, "paint", 0.1)
    tur.box(5.8, 6.05, -3.5, -1.9, 7.1, 7.8, "glass")
    # tourelleau du chef et trappe
    tur.box(-2.8, 0.0, 0.9, 3.8, 6.9, 7.35, "dark", 0.1)
    tur.box(-2.4, -0.4, 1.3, 3.4, 7.35, 7.6, "paint", 0.2)
    # tourelleau téléopéré XLR (7,62 mm), à droite derrière le viseur tireur
    tur.box(-4.6, -1.8, -3.5, -1.0, 6.9, 7.5, "dark")
    tur.box(-4.2, -2.4, -3.0, -1.5, 7.5, 8.6, "paint", 0.08)
    tur.cylinder_x(-2.4, 1.6, -2.25, 8.1, 0.18, "metal")
    tur.box(-2.6, -2.2, -3.3, -2.7, 8.2, 8.7, "glass")
    # lance-pots GALIX : 3 x 3 tubes sur chaque flanc, vers l'extérieur
    for s in (1, -1):
        tur.box(-6.6, -2.8, *sorted((s * 4.4, s * 4.9)), 4.6, 6.8, "dark", 0.1)
        for x in (-6.0, -4.7, -3.4):
            for z in (5.0, 5.7, 6.4):
                tur.cylinder_y(x, *sorted((s * 4.9, s * 5.6)), z, 0.3, "metal", sides=6)
        # détecteurs d'alerte laser aux coins avant
        tur.box(3.4, 3.9, *sorted((s * 4.3, s * 4.7)), 6.7, 7.1, "glass")
    # antennes SCORPION (fouets) et brouilleur anti-IED sur la nuque
    for y in (-3.4, 3.4):
        tur.box(-10.4, -10.1, y - 0.15, y + 0.15, 6.9, 12.5, "metal")
        tur.box(-10.6, -9.9, y - 0.4, y + 0.4, 6.9, 7.4, "dark")
    tur.box(-9.2, -7.4, -1.3, 1.3, 6.9, 7.8, "paint", 0.16)                        # brouilleur anti-IED
    for y in (-0.9, 0.0, 0.9):
        tur.box(-8.5, -8.2, y - 0.1, y + 0.1, 7.8, 9.0, "metal")
    tur.box(-6.6, -5.4, 2.6, 3.8, 6.9, 7.5, "white", 0.1)                          # antenne GPS / liaison
    return hull, tur, -1.5


# ===========================================================================
# RENFORTS NATIONAUX (rendu détaillé hd.py)
# ===========================================================================
JP2 = {"scale": 7.0, "seed": 17, "tones": [(0.42, 0.14), (1.1, 0.0)]}        # vert et brun des JGSDF
ES3 = {"scale": 7.0, "seed": 19, "tones": [(0.3, 0.16), (0.6, 0.0), (1.1, 0.08)]}
TR3 = {"scale": 7.5, "seed": 23, "tones": [(0.32, 0.15), (0.6, 0.0), (1.1, -0.07)]}


# ---------------------------------------------------------------------------
# VCI Puma : caisse haute et large, moteur à l'avant droit, modules de
# blindage latéraux épais sur toute la longueur, porte arrière, épiscopes
# des fantassins. Tourelle téléopérée RCT30 : canon MK30-2 de 30 mm,
# lanceur Spike à gauche, viseur panoramique du chef, lance-pots.
# ---------------------------------------------------------------------------
def puma():
    hull = Model()
    hd_tracks(hull, -11.5, 11.5, 5.7, 2.0, wheels=6, wheel_r=1.1, sprocket="front")
    hull.box(-11.3, 9.0, -3.7, 3.7, 0.7, 2.8, "dark")
    hull.box(-11.8, 8.6, -5.6, 5.6, 2.8, 5.4)
    hull.prism([(8.6, -5.6, 2.8), (12.2, -4.6, 3.4), (12.2, 4.6, 3.4), (8.6, 5.6, 2.8)],
               [(8.6, -5.6, 5.4), (10.2, -4.8, 5.0), (10.2, 4.8, 5.0), (8.6, 5.6, 5.4)])
    hd_skirts(hull, -11.6, 11.4, 5.6, 1.2, 5.2, panels=5, heavy=5, heavy_z0=1.2)
    hull.box(-12.3, -11.8, -3.2, 3.2, 1.4, 5.0, "paint", 0.12)                    # porte arrière
    hull.box(-12.4, -12.2, -2.6, 2.6, 1.8, 4.6, "dark")
    hull.box(1.2, 8.2, -5.0, -0.8, 5.4, 5.8, "paint", 0.1)                        # moteur (avant droit)
    for gx in (2.0, 3.8, 5.6):
        hull.box(gx, gx + 1.2, -4.4, -1.4, 5.8, 6.0, "dark")
    hatch(hull, 7.0, 2.8, 5.4, 0.9)                                              # pilote (avant gauche)
    periscope(hull, 7.8, 8.4, 1.8, 3.8, 5.4, 0.35)
    for x in (-10.0, -7.6, -5.2):                                                 # épiscopes du compartiment
        for s in (1, -1):
            periscope(hull, x, x + 1.2, *ys(s * 4.4, s * 5.2), 5.4, 0.35)
    hatch(hull, -8.8, 0.0, 5.4, 1.1)
    for s in (1, -1):
        lights(hull, 10.0, s * 4.0, 5.1, s)
        tow_cable(hull, -10.0, 0.0, s * 5.2, 5.55)
    hd_style(hull, camo=NATO3, dust=0.8)

    tur = Model()
    base = [(-4.8, -3.6), (3.2, -3.6), (4.6, -2.2), (4.6, 2.2), (3.2, 3.6), (-4.8, 3.6)]
    tur.prism([(x, y, 5.4) for x, y in base], [(x, y, 7.0) for x, y in scaled(base, 0.92, 0.85, -0.2)])
    tur.box(4.2, 5.6, -1.0, 1.0, 5.7, 6.8, "paint", 0.12)
    hd_barrel(tur, 5.4, 14.6, 6.3, 0.36, sleeves=((5.6, 8.4),), brake=0.9, mrs=False)
    tur.box(-3.4, 1.8, *ys(3.6, 5.6), 5.8, 7.4, "paint", 0.14)                    # lanceur Spike (gauche)
    for tz in (6.25, 7.0):
        tur.cylinder_x(1.8, 2.1, 4.6, tz, 0.38, "dark")
    tur.cylinder_z(-2.6, -2.2, 7.0, 8.0, 0.6, "metal")                           # panoramique du chef
    tur.box(-3.4, -1.8, -3.0, -1.4, 8.0, 9.0, "paint", 0.05)
    tur.box(-1.8, -1.55, -2.8, -1.6, 8.2, 8.8, "glass")
    tur.box(0.8, 2.8, 1.0, 2.6, 7.0, 7.9, "paint", 0.1)                           # viseur du tireur
    tur.box(2.8, 3.05, 1.2, 2.4, 7.2, 7.7, "glass")
    for s in (1, -1):
        smoke_launchers(tur, -4.4, s * 3.5, 6.6, s, 4, spacing=0.55)
    antenna(tur, -4.2, 2.4, 7.0, 5.5)
    hd_style(tur, camo=NATO3)
    return hull, tur, -3.0


# ---------------------------------------------------------------------------
# Skyranger 30 sur Boxer 8x8 : caisse haute à flancs biseautés, module de
# conduite et module de mission, 4 grandes roues par côté. Tourelle avec
# canon revolver de 30 mm, 4 panneaux radar AESA, capteur optronique.
# ---------------------------------------------------------------------------
def skyranger():
    hull = Model()
    for x in (8.6, 4.4, -3.8, -8.0):
        for s in (1, -1):
            wheel(hull, x, s * 3.3, s * 5.0, 1.85)
    hull.box(-11.6, 11.0, -3.2, 3.2, 1.3, 2.6, "dark")
    hull.tapered_box(-12, 9.6, -5.2, 5.2, 2.4, 6.6, inset_side=0.9, inset_back=0.3)
    hull.prism([(9.6, -5.2, 2.4), (12.6, -3.8, 3.2), (12.6, 3.8, 3.2), (9.6, 5.2, 2.4)],
               [(9.6, -4.3, 6.6), (11.2, -3.4, 5.6), (11.2, 3.4, 5.6), (9.6, 4.3, 6.6)])
    hull.box(-1.2, -0.9, -4.4, 4.4, 6.6, 6.7, "dark")                             # joint des modules
    for s in (1, -1):
        hull.box(-11.0, 10.4, *ys(s * 4.9, s * 5.4), 3.8, 4.2, "paint", 0.14)    # garde-boue
        hull.box(-10.4, -5.0, *ys(s * 4.6, s * 5.3), 4.3, 5.8, "paint", 0.16)    # coffres
        lights(hull, 11.0, s * 3.4, 5.4, s)
        hull.tube((10.2, s * 4.0, 6.0), (10.8, s * 5.4, 6.6), 0.2, "dark", sides=4)
        hull.box(10.6, 11.0, *ys(s * 5.2, s * 5.7), 6.2, 7.0, "dark")
    periscope(hull, 10.0, 10.8, 1.2, 3.4, 6.2, 0.35)
    hatch(hull, 8.6, 2.2, 6.6, 0.9)
    hatch(hull, -9.6, -2.0, 6.6, 1.0)
    hull.box(-12.4, -12.0, -3.0, 3.0, 2.8, 6.0, "paint", 0.12)                    # porte arrière
    hd_style(hull, camo=NATO3, dust=0.8, dust_height=2.8, track_period=1.6)

    tur = Model()
    body = [(-4.2, -3.2), (2.6, -3.2), (4.0, -1.8), (4.0, 1.8), (2.6, 3.2), (-4.2, 3.2)]
    tur.prism([(x, y, 6.6) for x, y in body], [(x, y, 9.0) for x, y in scaled(body, 0.9, 0.85, -0.2)])
    tur.box(3.6, 5.0, -0.9, 0.9, 7.2, 8.4, "paint", 0.12)
    hd_barrel(tur, 4.8, 15.0, 7.8, 0.38, sleeves=((4.8, 7.2),), brake=1.0, mrs=False)
    tur.box(7.8, 8.6, -0.25, 0.25, 8.2, 8.5, "dark")                               # capteur de vitesse initiale
    for s in (1, -1):                                                               # panneaux radar AESA
        mirrored_prism(tur, [(1.0, 3.2, 7.0), (3.6, 2.2, 7.0), (3.8, 2.6, 7.0), (1.2, 3.6, 7.0)],
                       [(1.0, 3.2, 8.8), (3.6, 2.2, 8.8), (3.8, 2.6, 8.8), (1.2, 3.6, 8.8)], s, "dark", 0.0)
        mirrored_prism(tur, [(-4.2, 2.6, 7.0), (-2.0, 3.4, 7.0), (-2.2, 3.8, 7.0), (-4.4, 3.0, 7.0)],
                       [(-4.2, 2.6, 8.8), (-2.0, 3.4, 8.8), (-2.2, 3.8, 8.8), (-4.4, 3.0, 8.8)], s, "dark", 0.0)
        smoke_launchers(tur, -1.8, s * 3.3, 7.8, s, 3, spacing=0.55)
    tur.cylinder_z(-1.2, 0.0, 9.0, 9.8, 0.9, "paint", sides=10, tint=0.08)       # boule optronique
    tur.box(-0.4, 0.0, -0.5, 0.5, 9.1, 9.7, "glass")
    antenna(tur, -3.6, -2.2, 9.0, 4.5)
    hd_style(tur, camo=NATO3)
    return hull, tur, -4.0


# ---------------------------------------------------------------------------
# Type 03 Chu-SAM : camion 6x6 à cabine avancée, plateau avec rampe
# orientable de 6 conteneurs de missiles (2 rangées de 3) relevée à 25°.
# ---------------------------------------------------------------------------
def chusam():
    hull = Model()
    for x in (8.0, -3.4, -7.6):
        for s in (1, -1):
            wheel(hull, x, s * 2.8, s * 4.4, 1.8)
    hull.box(-12.0, 11.0, -2.2, 2.2, 1.4, 2.4, "dark")
    hull.box(-12.0, 5.2, -3.6, 3.6, 2.4, 3.2, "dark", 0.1)
    hull.tapered_box(5.4, 11.8, -4.0, 4.0, 2.4, 7.4, inset_front=0.8, inset_side=0.3)   # cabine
    hull.box(11.4, 11.95, -3.4, 3.4, 5.0, 6.9, "glass")
    hull.box(11.7, 12.2, -3.4, 3.4, 2.8, 4.6, "dark")
    for s in (1, -1):
        hull.box(6.4, 10.2, *ys(s * 3.85, s * 4.05), 5.2, 6.8, "glass")
        hull.box(11.5, 12.1, *ys(s * 2.6, s * 3.5), 4.8, 5.3, "white", 0.05)
        hull.tube((9.8, s * 3.9, 6.4), (10.4, s * 5.0, 6.8), 0.2, "dark", sides=4)
        hull.box(10.2, 10.6, *ys(s * 4.9, s * 5.3), 5.8, 7.0, "dark")
        hull.box(6.2, 9.6, *ys(s * 3.4, s * 4.4), 1.4, 3.3, "paint", 0.2)
        hull.box(-10.2, -0.8, *ys(s * 3.5, s * 4.6), 2.8, 3.4, "paint", 0.18)
        hull.box(-1.0, 4.8, *ys(s * 3.3, s * 4.4), 3.2, 4.8, "paint", 0.12)       # coffres
        hull.box(-11.6, -10.4, *ys(s * 3.0, s * 4.0), 1.0, 3.2, "metal", 0.1)     # vérins de calage
    hull.box(-12.0, 5.0, -4.0, 4.0, 3.2, 3.8, "paint", 0.1)                        # plateau
    hull.cylinder_z(-4.9, 0.0, 3.8, 4.6, 2.6, "paint", sides=12, tint=0.08)       # couronne
    hd_style(hull, camo=JP2, dust=0.8, dust_height=2.6, track_period=1.6)

    tur = Model()
    tur.box(-2.4, 2.4, -2.2, 2.2, 4.6, 5.8, "paint", 0.04)                        # socle
    for s in (1, -1):
        tur.box(-1.0, 1.4, *ys(s * 2.2, s * 2.8), 4.6, 7.6, "paint", 0.12)       # bras
    el = math.radians(25)
    ce, se = math.cos(el), math.sin(el)
    L0, L1 = -6.0, 6.5
    for row in range(2):
        for col in range(3):
            y = -2.3 + col * 2.3
            zc = 6.8 + row * 1.9
            pts = []
            for x in (L0, L1):
                pts.append((x * ce, zc + x * se))
            (xa, za), (xb, zb) = pts
            tur.prism([(xa, y - 1.0, za - 0.85), (xb, y - 1.0, zb - 0.85), (xb, y + 1.0, zb - 0.85), (xa, y + 1.0, za - 0.85)],
                      [(xa, y - 1.0, za + 0.85), (xb, y - 1.0, zb + 0.85), (xb, y + 1.0, zb + 0.85), (xa, y + 1.0, za + 0.85)],
                      "paint", 0.06 + 0.08 * ((row + col) % 2))
            tur.box(xb - 0.05, xb + 0.15, y - 0.7, y + 0.7, zb - 0.6, zb + 0.6, "white", 0.15)   # couvercle
    antenna(tur, -2.0, 2.0, 5.8, 3.0)
    hd_style(tur, camo=JP2)
    return hull, tur, -4.9


# ---------------------------------------------------------------------------
# VCR 8x8 Dragón : caisse haute à nez en coin, 4 essieux, coffres latéraux,
# tourelleau téléopéré Guardian 30 (30 mm) avec viseur et lance-pots.
# ---------------------------------------------------------------------------
def dragon8x8():
    hull = Model()
    for x in (8.4, 4.4, -3.6, -7.6):
        for s in (1, -1):
            wheel(hull, x, s * 3.3, s * 4.9, 1.8)
    hull.box(-11.4, 10.8, -3.2, 3.2, 1.3, 2.6, "dark")
    hull.tapered_box(-12, 9.0, -5.1, 5.1, 2.4, 6.2, inset_side=0.8, inset_back=0.3)
    hull.prism([(9.0, -5.1, 2.4), (12.8, -2.8, 3.0), (12.8, 2.8, 3.0), (9.0, 5.1, 2.4)],
               [(9.0, -4.3, 6.2), (10.8, -3.0, 5.2), (10.8, 3.0, 5.2), (9.0, 4.3, 6.2)])
    hull.box(11.6, 12.9, -2.6, 2.6, 2.6, 3.2, "paint", 0.2)                        # déflecteur
    for s in (1, -1):
        hull.box(-10.6, 10.4, *ys(s * 4.8, s * 5.3), 3.6, 4.0, "paint", 0.14)
        for x0, x1 in ((-10.2, -6.0), (-1.8, 2.2)):
            hull.box(x0, x1, *ys(s * 4.5, s * 5.2), 4.0, 5.6, "paint", 0.16)
        lights(hull, 10.2, s * 3.2, 5.2, s)
        hull.box(-12.3, -11.9, *ys(s * 1.0, s * 4.0), 3.0, 5.2, "paint", 0.1)
    periscope(hull, 9.2, 9.9, 1.4, 3.6, 5.8, 0.35)
    hatch(hull, 8.0, 2.4, 6.2, 0.9)
    for x in (-9.4, -6.6):
        hatch(hull, x, 0.0, 6.2, 0.9)
    hull.box(-12.4, -12.1, -2.2, 2.2, 2.8, 5.4, "dark", 0.1)                       # rampe arrière
    antenna(hull, -11.0, -3.4, 6.2, 5.0)
    hd_style(hull, camo=ES3, dust=0.8, dust_height=2.8, track_period=1.6)

    tur = Model()
    base = [(-3.0, -2.4), (2.2, -2.4), (3.2, -1.4), (3.2, 1.4), (2.2, 2.4), (-3.0, 2.4)]
    tur.prism([(x, y, 6.2) for x, y in base], [(x, y, 7.8) for x, y in scaled(base, 0.9, 0.85)])
    hd_barrel(tur, 2.8, 10.6, 7.0, 0.34, sleeves=((2.8, 5.0),), brake=0.8, mrs=False)
    tur.box(-1.4, 0.8, *ys(2.4, 3.8), 6.6, 8.2, "paint", 0.12)                     # caisson à munitions
    tur.box(0.2, 1.8, -2.2, -0.8, 7.8, 8.8, "paint", 0.06)                           # viseur
    tur.box(1.8, 2.05, -2.0, -1.0, 8.0, 8.6, "glass")
    tur.cylinder_x(1.6, 3.8, -1.6, 6.7, 0.18, "dark")                               # coaxiale
    for s in (1, -1):
        smoke_launchers(tur, -2.8, s * 2.4, 7.4, s, 3, spacing=0.5)
    hd_style(tur, camo=ES3)
    return hull, tur, -1.0


# ---------------------------------------------------------------------------
# Altay : caisse longue à 7 galets, jupes à modules lourds à l'avant,
# grilles moteur. Tourelle anguleuse à blindage modulaire, capteurs radar et
# lanceurs de la protection active AKKOR, viseur du chef à droite,
# tourelleau SARP, nuque avec panier, canon de 120 mm L55.
# ---------------------------------------------------------------------------
def altay():
    hull = Model()
    hd_tracks(hull, -12.2, 12.2, 5.9, 2.2, wheels=7)
    hull.box(-12.0, 9.6, -3.7, 3.7, 0.7, 2.8, "dark")
    hull.box(-12.2, 9.6, -5.7, 5.7, 2.8, 4.3)
    hull.prism([(9.6, -5.7, 2.8), (12.8, -4.6, 3.5), (12.8, 4.6, 3.5), (9.6, 5.7, 2.8)],
               [(9.6, -5.7, 4.3), (11.0, -4.9, 4.3), (11.0, 4.9, 4.3), (9.6, 5.7, 4.3)])
    hull.prism([(9.4, -3.7, 0.8), (11.8, -3.7, 0.8), (11.8, 3.7, 0.8), (9.4, 3.7, 0.8)],
               [(9.4, -3.9, 2.8), (13.0, -3.9, 3.0), (13.0, 3.9, 3.0), (9.4, 3.9, 2.8)], "paint", 0.1)
    hd_skirts(hull, -12.0, 11.6, 5.7, 1.3, 4.2, panels=7, heavy=3)
    hull.box(-12.0, -4.8, -4.8, 4.8, 4.3, 4.6, "paint", 0.1)
    for gx in (-11.4, -9.4, -7.4):
        hull.box(gx, gx + 1.3, -4.0, 4.0, 4.6, 4.8, "dark")
    hull.box(-12.6, -12.0, -4.8, 4.8, 1.6, 4.3, "dark", 0.1)
    for s in (1, -1):
        hull.box(-12.7, -11.8, *ys(s * 3.0, s * 4.9), 2.6, 4.5, "paint", 0.2)
        tow_cable(hull, -10.4, 6.0, s * 5.0, 4.45)
        lights(hull, 10.8, s * 4.1, 4.3, s)
    hatch(hull, 8.2, 2.4, 4.3, 0.9)
    periscope(hull, 8.8, 9.5, 1.4, 3.4, 4.3, 0.4)
    hd_style(hull, camo=TR3, dust=0.8)

    tur = Model()
    body = [(-7.6, -4.5), (3.2, -4.8), (7.4, -3.2), (7.8, -1.4), (7.8, 1.4), (7.4, 3.2), (3.2, 4.8), (-7.6, 4.5)]
    tur.prism([(x, y, 4.3) for x, y in body], [(x - 0.2, y * 0.95, 7.3) for x, y in body])
    tur.box(-7.8, 3.4, -4.2, 4.2, 7.3, 7.5, "paint", 0.1)
    for s in (1, -1):                                                               # modules avant
        mirrored_prism(tur, [(3.4, 1.5, 4.5), (8.4, 1.5, 4.5), (7.2, 4.6, 4.5), (3.2, 5.0, 4.5)],
                       [(3.4, 1.5, 7.3), (8.0, 1.5, 7.3), (6.9, 4.4, 7.3), (3.2, 4.8, 7.3)], s, "paint", 0.06)
        mirrored_prism(tur, [(4.2, 4.9, 5.0), (6.8, 4.5, 5.0), (6.9, 4.9, 5.0), (4.3, 5.3, 5.0)],
                       [(4.2, 4.9, 7.1), (6.8, 4.5, 7.1), (6.9, 4.9, 7.1), (4.3, 5.3, 7.1)], s, "dark")   # radar AKKOR
        tur.box(-4.6, -1.8, *ys(s * 4.5, s * 5.4), 6.4, 7.6, "paint", 0.14)       # lanceurs AKKOR
        tur.cylinder_z(-3.2, s * 4.95, 7.6, 8.1, 0.5, "metal", sides=8)
        tur.box(-7.4, -4.8, *ys(s * 4.4, s * 5.2), 4.8, 6.6, "paint", 0.16)      # coffres
        smoke_launchers(tur, -1.4, s * 4.6, 6.8, s, 4, spacing=0.55)
    tur.box(-11.4, -7.4, -4.0, 4.0, 4.6, 7.0, "paint", 0.06)                        # nuque
    for k in range(6):
        tur.box(-12.2, -11.9, -3.6 + k * 1.44, -3.3 + k * 1.44, 5.0, 7.3, "dark")
    tur.box(-12.1, -11.5, -3.3, 3.3, 5.2, 6.9, "olive", 0.1)
    tur.box(7.4, 9.0, -1.2, 1.2, 4.9, 6.9, "paint", 0.12)
    hd_barrel(tur, 8.8, 24.0, 5.9, 0.62, sleeves=((9.2, 12.8), (16.4, 19.6), (19.9, 22.8)), evacuator=(13.2, 16.0))
    tur.cylinder_z(-2.2, -2.6, 7.4, 8.8, 0.8, "metal")                            # viseur du chef (droite)
    tur.box(-3.2, -1.2, -3.6, -1.6, 8.8, 9.9, "paint", 0.06)
    tur.box(-1.2, -0.95, -3.3, -1.9, 9.1, 9.7, "glass")
    tur.box(2.0, 4.6, 1.8, 3.8, 7.4, 8.4, "paint", 0.1)                             # viseur du tireur
    tur.box(4.6, 4.85, 2.1, 3.5, 7.6, 8.2, "glass")
    tur.box(-5.6, -3.8, 0.6, 2.4, 7.4, 8.0, "dark")                                 # tourelleau SARP
    tur.box(-5.3, -4.0, 0.9, 2.1, 8.0, 8.9, "paint", 0.08)
    tur.tube((-4.2, 1.5, 8.5), (-1.8, 1.5, 8.55), 0.22, "metal", sides=4)
    hatch(tur, -2.0, 2.6, 7.4, 0.9)
    for y in (-3.2, 3.2):
        antenna(tur, -9.6, y, 7.0, 6.5)
    hd_style(tur, camo=TR3)
    return hull, tur, -2.0


# ---------------------------------------------------------------------------
# Porte-avions Izumo : pont d'envol continu, îlot à tribord (radars plats,
# mât, cheminées), ascenseurs, marquages blancs des spots d'appontage,
# systèmes CIWS à la proue et à la poupe, deux F-35B garés sur le pont.
# Sprite de 96 x 96.
# ---------------------------------------------------------------------------
def izumo():
    m = Model()
    hull_wl = [(-36, -5.0), (26, -5.4), (34, -3.0), (38, 0.0), (34, 3.0), (26, 5.4), (-36, 5.0)]
    deck = [(-38, -6.6), (27, -6.8), (35, -3.8), (39, 0.0), (35, 3.8), (27, 6.8), (-38, 6.6)]
    m.prism([(x, y, 0.0) for x, y in ccw(hull_wl)], [(x, y, 3.2) for x, y in ccw(deck)], "paint", 0.1)
    m.extrude(ccw(deck), 3.2, 3.8, "dark", 0.15)                                     # pont d'envol
    for x in range(-34, 36, 4):                                                     # axe central pointillé
        m.box(x, x + 2.0, -0.25, 0.25, 3.8, 3.85, "white", 0.05)
    for x in (-26, -14, -2, 10, 22):                                                # spots d'appontage
        m.box(x - 1.3, x + 1.3, 2.4, 5.0, 3.8, 3.85, "white", 0.2)
        m.box(x - 0.7, x + 0.7, 3.1, 4.3, 3.84, 3.86, "dark", 0.15)
    for x0, x1 in ((-22, -16), (14, 20)):                                           # ascenseurs
        m.box(x0, x1, -5.6, -2.0, 3.8, 3.82, "dark", 0.3)
        for xa, xb, ya, yb in ((x0, x1, -5.6, -5.4), (x0, x1, -2.2, -2.0), (x0, x0 + 0.2, -5.6, -2.0), (x1 - 0.2, x1, -5.6, -2.0)):
            m.box(xa, xb, ya, yb, 3.8, 3.87, "white", 0.1)
    # îlot à tribord
    m.box(-8, 14, -7.0, -4.6, 3.8, 8.4, "paint", 0.02)
    m.box(-6, 12, -6.8, -4.9, 8.4, 11.0, "paint", 0.06)
    m.box(-3, 8, -6.6, -5.1, 11.0, 13.2, "paint", 0.1)
    for x0, x1 in ((-6.5, -3.5), (5.5, 8.5)):                                      # cheminées
        m.box(x0, x1, -6.4, -5.2, 11.0, 12.8, "dark", 0.1)
    for x, zz in ((12.3, 9.2), (-6.3, 9.2)):                                        # radars plats FCS-3
        m.box(x, x + 0.3, -6.6, -5.0, zz, zz + 1.8, "dark")
    m.box(8.0, 8.3, -6.4, -5.3, 11.2, 12.8, "glass")
    m.box(12.0, 12.25, -6.8, -4.8, 8.6, 9.2, "glass")                               # passerelle
    m.tube((2.0, -5.8, 13.2), (2.0, -5.8, 18.0), 0.35, "metal", sides=6)            # mât
    m.box(1.0, 3.0, -6.8, -4.8, 16.0, 16.3, "metal")
    m.box(1.6, 2.4, -6.1, -5.5, 18.0, 18.6, "white")
    # CIWS et lance-missiles SeaRAM
    for x, y in ((34.0, 2.2), (-36.0, -3.0), (-35.0, 3.2)):
        m.cylinder_z(x, y, 3.8, 4.4, 0.9, "white", sides=8, tint=0.05)
        m.cylinder_z(x, y, 4.4, 5.6, 0.6, "white", sides=8)
    # deux F-35B garés
    for x0 in (-30.0, -24.5):                                                       # sur l'axe, à l'arrière
        m.loft_x([(x0 - 2.4, 0.3, 0.3, 4.3), (x0 - 1.0, 0.7, 0.4, 4.3), (x0 + 1.6, 0.6, 0.4, 4.3), (x0 + 2.6, 0.1, 0.1, 4.2)],
                 "metal", 8, tint=0.1)
        for s in (1, -1):
            m.plate([(x0 + 0.2, s * 0.6, 4.2), (x0 - 1.4, s * 2.8, 4.2), (x0 - 2.2, s * 2.8, 4.2), (x0 - 1.6, s * 0.6, 4.2)],
                    0.2, "metal", 0.1)
    # bord de coque : ligne de flottaison sombre
    m.prism([(x, y * 1.01, -0.2) for x, y in ccw(hull_wl)], [(x, y * 1.01, 0.6) for x, y in ccw(hull_wl)], "dark", 0.1)
    return hd_style(m, camo=None, dust=0.0)
