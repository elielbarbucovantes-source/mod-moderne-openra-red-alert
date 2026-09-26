"""Drones français RATC : MQ-9 Reaper, Patroller, munition rôdeuse Larinae/Colibri.

Échelle des aéronefs : ~1,7 px par mètre (les avions RA sont eux aussi réduits),
avec épaississement des pièces fines pour qu'elles restent lisibles.
L'altitude est gérée par le jeu : les modèles sont centrés sur z = 0.
"""
import math
from render import Model


def pylon_with_gbu(m, x, y, z):
    """Pylône + bombe guidée laser GBU-12 (corps, autodirecteur, ailettes en croix)."""
    m.box(x - 1.0, x + 0.8, y - 0.25, y + 0.25, z - 0.6, z, "dark")
    bomb = Model()
    bomb.loft_x([(x - 2.2, 0.35, 0.35, z - 1.0), (x - 1.6, 0.55, 0.55, z - 1.0),
                 (x + 1.2, 0.55, 0.55, z - 1.0), (x + 2.0, 0.3, 0.3, z - 1.0)], "metal", 8)
    bomb.loft_x([(x + 2.0, 0.3, 0.3, z - 1.0), (x + 2.6, 0.12, 0.12, z - 1.0)], "glass", 6)
    for a in (0, 90, 180, 270):
        dy, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        bomb.plate([(x - 2.2, 0, z - 1.0), (x - 1.4, 0, z - 1.0),
                    (x - 1.8, dy * 0.9, z - 1.0 + dz * 0.9), (x - 2.3, dy * 0.9, z - 1.0 + dz * 0.9)],
                   0.15, "metal")
    m.solids += shift_y(bomb, y).solids


def shift_y(sections_model, dy):
    return sections_model.transformed(lambda x, y, z: (x, y + dy, z))


# ---------------------------------------------------------------------------
# MQ-9 Reaper : grand drone MALE. Fuselage effilé avec le dôme SATCOM bombé
# du nez, boule optronique MTS-B sous le nez, grandes ailes droites
# d'allongement élevé, empennage en V plus dérive ventrale, hélice propulsive
# tripale, 4 pylônes (2 GBU-12 + 2 rails de missiles).
# ---------------------------------------------------------------------------
def reaper():
    m = Model()
    # Fuselage (de l'arrière vers l'avant)
    m.loft_x([(-9.2, 0.35, 0.35, 0.2), (-8.0, 0.7, 0.7, 0.2), (-4.0, 1.25, 1.2, 0.1),
              (1.0, 1.45, 1.4, 0.1), (5.0, 1.4, 1.6, 0.4), (7.5, 1.2, 1.55, 0.6),
              (9.0, 0.8, 1.0, 0.5), (9.7, 0.3, 0.4, 0.3)], "paint", 14)
    # Dôme SATCOM sur le nez (bosse caractéristique)
    m.loft_x([(4.0, 0.6, 0.3, 1.6), (5.5, 1.15, 0.8, 1.7), (7.2, 1.0, 0.7, 1.6), (8.4, 0.4, 0.25, 1.3)],
             "paint", 10, tint=-0.05)
    # Boule optronique MTS-B sous le nez
    m.loft_x([(6.4, 0.2, 0.2, -1.5), (6.8, 0.75, 0.75, -1.6), (7.7, 0.75, 0.75, -1.6), (8.1, 0.2, 0.2, -1.5)],
             "dark", 10)
    m.box(7.6, 8.0, -0.35, 0.35, -1.9, -1.3, "glass")
    # Prise d'air dorsale et échappement
    m.loft_x([(-3.0, 0.2, 0.1, 1.25), (-1.6, 0.55, 0.45, 1.3), (-0.6, 0.55, 0.45, 1.3)], "dark", 8)
    m.box(-7.6, -6.6, -0.5, 0.5, 0.7, 1.0, "dark")
    # Antennes (lame dorsale, fouet ventral)
    m.plate([(2.0, 0, 1.4), (3.2, 0, 1.4), (2.6, 0, 2.6), (2.2, 0, 2.6)], 0.15, "metal")
    m.plate([(-2.0, 0, -1.1), (-1.2, 0, -1.1), (-1.8, 0, -2.0)], 0.12, "metal")
    # Ailes droites, à léger effilement, avec saumons
    for s in (1, -1):
        m.plate([(1.4, s * 1.2, 0.2), (1.2, s * 16.5, 0.6), (-0.3, s * 16.5, 0.6), (-1.4, s * 1.2, 0.2)], 0.55)
        m.plate([(1.2, s * 16.5, 0.6), (1.0, s * 17.2, 0.9), (-0.2, s * 17.2, 0.9), (-0.3, s * 16.5, 0.6)],
                0.4, "paint", 0.12)                               # saumon
        m.plate([(-0.6, s * 9.5, 0.45), (-0.6, s * 15.8, 0.6), (-1.3, s * 15.8, 0.6), (-1.35, s * 9.5, 0.45)],
                0.6, "paint", 0.16)                               # aileron
        m.plate([(-0.6, s * 2.0, 0.25), (-0.6, s * 9.2, 0.45), (-1.3, s * 9.2, 0.45), (-1.4, s * 2.0, 0.25)],
                0.6, "paint", 0.08)                               # volet
        pylon_with_gbu(m, 0.2, s * 5.0, -0.1)                     # GBU-12 intérieures
        m.box(-0.6, 0.9, s * 9.0 - 0.2, s * 9.0 + 0.2, -0.3, 0.3, "dark")   # rail extérieur
    # 2 missiles sous chaque rail extérieur
    for s in (1, -1):
        for dy in (-0.45, 0.45):
            missile = Model().loft_x([(-0.9, 0.22, 0.22, -0.6), (1.4, 0.22, 0.22, -0.6), (1.9, 0.08, 0.08, -0.6)],
                                     "metal", 6)
            m.solids += shift_y(missile, s * 9.0 + dy).solids
    # Empennage en V (vers le haut) + dérive ventrale
    for s in (1, -1):
        m.plate([(-6.4, s * 0.5, 0.8), (-8.6, s * 0.5, 0.8), (-9.4, s * 4.4, 4.2), (-8.2, s * 4.4, 4.2)], 0.4)
        m.plate([(-8.3, s * 3.0, 2.9), (-9.1, s * 3.0, 2.9), (-9.4, s * 4.4, 4.2), (-8.9, s * 4.4, 4.2)],
                0.45, "paint", 0.16)                              # gouverne
    m.plate([(-6.8, 0, -0.9), (-8.6, 0, -0.8), (-9.2, 0, -3.2), (-8.4, 0, -3.2)], 0.4, "paint", 0.06)
    # Hélice propulsive tripale
    m.loft_x([(-10.0, 0.15, 0.15, 0.2), (-9.4, 0.35, 0.35, 0.2), (-9.1, 0.3, 0.3, 0.2)], "dark", 8)
    for a in (90, 210, 330):
        dy, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        m.plate([(-9.7, dy * 0.3, 0.2 + dz * 0.3), (-9.5, dy * 0.3, 0.2 + dz * 0.3),
                 (-9.6, dy * 3.2, 0.2 + dz * 3.2), (-9.8, dy * 3.0, 0.2 + dz * 3.0)], 0.2, "dark")
    # Feux de position (bouts d'aile)
    m.box(-0.1, 0.5, 17.0, 17.4, 0.7, 1.1, "glass")
    m.box(-0.1, 0.5, -17.4, -17.0, 0.7, 1.1, "glass")
    return m


# ---------------------------------------------------------------------------
# Patroller (Safran, dérivé du motoplaneur Stemme S15) : fuselage en goutte
# avec verrière, hélice tractrice dans le nez, très longues ailes fines de
# planeur, poutre de queue mince, empennage en T, boule optronique Euroflir
# sous le fuselage, 4 points d'emport (roquettes guidées laser).
# ---------------------------------------------------------------------------
def patroller():
    m = Model()
    m.loft_x([(-10.5, 0.25, 0.3, 0.9), (-6.5, 0.4, 0.45, 0.8), (-3.0, 0.9, 1.0, 0.4),
              (0.5, 1.35, 1.45, 0.1), (3.5, 1.35, 1.4, 0.0), (5.6, 1.0, 1.0, -0.1), (6.4, 0.5, 0.5, -0.1)],
             "paint", 14)
    # Verrière (motoplaneur optionnellement piloté)
    m.loft_x([(0.2, 0.3, 0.2, 1.3), (1.2, 1.0, 0.7, 1.35), (3.6, 1.0, 0.65, 1.2), (4.8, 0.3, 0.2, 0.8)],
             "glass", 12)
    # Casserole d'hélice et hélice tractrice bipale
    m.loft_x([(6.2, 0.55, 0.55, -0.1), (7.1, 0.3, 0.3, -0.1), (7.5, 0.05, 0.05, -0.1)], "metal", 8)
    for s in (1, -1):
        m.plate([(6.9, 0, -0.1), (7.1, 0, -0.1), (7.0, s * 3.4, -0.1 + s * 0.3), (6.8, s * 3.2, -0.1 + s * 0.3)],
                0.2, "dark")
    # Boule Euroflir sous le fuselage
    m.loft_x([(1.4, 0.2, 0.2, -1.5), (1.8, 0.8, 0.8, -1.7), (2.8, 0.8, 0.8, -1.7), (3.2, 0.2, 0.2, -1.5)],
             "dark", 10)
    m.box(3.0, 3.3, -0.3, 0.3, -2.0, -1.4, "glass")
    # Ailes de planeur (grand allongement, dièdre léger)
    for s in (1, -1):
        m.plate([(1.8, s * 1.2, 0.9), (1.1, s * 9.0, 1.3), (0.6, s * 15.0, 1.7), (-0.4, s * 15.0, 1.7),
                 (-0.5, s * 9.0, 1.3), (-0.7, s * 1.2, 0.9)], 0.45)
        m.plate([(-0.3, s * 9.0, 1.3), (-0.3, s * 14.6, 1.7), (-0.6, s * 14.6, 1.7), (-0.6, s * 9.0, 1.3)],
                0.5, "paint", 0.15)                               # aileron
        for py, rockets in ((4.0, 3), (7.0, 3)):                  # pylônes + paniers de roquettes
            m.box(-0.1, 1.1, s * py - 0.2, s * py + 0.2, 0.3, 1.0, "dark")
            pod = Model().loft_x([(-1.2, 0.45, 0.45, 0.0), (1.4, 0.45, 0.45, 0.0), (1.9, 0.25, 0.25, 0.0)],
                                 "metal", 8)
            m.solids += shift_y(pod, s * py).solids
            m.box(1.85, 1.95, s * py - 0.2, s * py + 0.2, -0.2, 0.2, "dark")
        m.box(0.0, 0.6, s * 15.0 - 0.2, s * 15.0 + 0.2, 1.6, 2.0, "glass")   # feu de bout d'aile
    # Poutre de queue et empennage en T
    m.plate([(-8.0, 0, 1.0), (-10.4, 0, 1.0), (-10.8, 0, 4.4), (-9.6, 0, 4.4)], 0.4)            # dérive
    m.plate([(-9.9, 0, 3.0), (-10.5, 0, 3.0), (-10.9, 0, 4.4), (-10.6, 0, 4.4)], 0.45, "paint", 0.15)
    for s in (1, -1):
        m.plate([(-9.4, 0, 4.5), (-9.6, s * 4.2, 4.5), (-10.6, s * 4.2, 4.5), (-10.9, 0, 4.5)], 0.35)
        m.plate([(-10.3, s * 0.4, 4.5), (-10.4, s * 4.1, 4.5), (-10.8, s * 4.1, 4.5), (-10.9, s * 0.4, 4.5)],
                0.4, "paint", 0.15)                               # profondeur
    # Antennes de liaison de données
    m.plate([(-2.0, 0, 1.1), (-1.2, 0, 1.2), (-1.7, 0, 2.3)], 0.12, "metal")
    m.plate([(-4.0, 0, -0.4), (-3.3, 0, -0.5), (-3.8, 0, -1.4)], 0.12, "metal")
    return m


# ---------------------------------------------------------------------------
# Munition télé-opérée Larinae / Colibri : corps tubulaire lancé depuis un
# tube, ailes tandem déployables en X, hélice propulsive, autodirecteur
# optronique vitré, charge militaire à l'avant. Agrandie ~5x.
# ---------------------------------------------------------------------------
def colibri():
    m = Model()
    m.loft_x([(-5.2, 0.5, 0.5, 0), (-4.6, 0.95, 0.95, 0), (3.2, 0.95, 0.95, 0),
              (4.4, 0.8, 0.8, 0), (5.2, 0.45, 0.45, 0)], "paint", 12)
    m.loft_x([(5.1, 0.46, 0.46, 0), (5.7, 0.2, 0.2, 0)], "glass", 10)              # autodirecteur
    m.loft_x([(2.6, 1.0, 1.0, 0), (3.2, 1.0, 1.0, 0)], "paint", 12, tint=0.2)       # bague de charge
    m.box(0.0, 1.6, -0.25, 0.25, 0.8, 1.35, "dark")                                 # antenne liaison
    for a in (45, 135, 225, 315):                                                   # ailes tandem en X
        dy, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        m.plate([(2.4, dy * 0.8, dz * 0.8), (1.0, dy * 0.8, dz * 0.8),
                 (0.8, dy * 5.2, dz * 5.2), (1.6, dy * 5.2, dz * 5.2)], 0.25)
        m.plate([(-2.6, dy * 0.8, dz * 0.8), (-4.2, dy * 0.8, dz * 0.8),
                 (-4.4, dy * 4.0, dz * 4.0), (-3.4, dy * 4.0, dz * 4.0)], 0.25, "paint", 0.1)
    m.loft_x([(-5.8, 0.15, 0.15, 0), (-5.3, 0.3, 0.3, 0)], "dark", 8)
    for a in (0, 120, 240):                                                         # hélice
        dy, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        m.plate([(-5.7, dy * 0.2, dz * 0.2), (-5.5, dy * 0.2, dz * 0.2),
                 (-5.6, dy * 2.4, dz * 2.4), (-5.8, dy * 2.2, dz * 2.2)], 0.2, "dark")
    return m


def colibri_diving():
    """Même drone, piqué presque à la verticale (image de l'attaque finale)."""
    a = math.radians(70)
    return colibri().transformed(lambda x, y, z: (x * math.cos(a) - z * math.sin(a), y,
                                                  x * math.sin(a) * -1 + z * math.cos(a)))


# ===========================================================================
# Outils communs aux drones
# ===========================================================================
def wing(m, x_le_root, x_te_root, x_le_tip, x_te_tip, y_root, y_tip, z_root, z_tip, th=0.45, tint=0.0):
    """Paire d'ailes symétriques (bord d'attaque / de fuite à l'emplanture et au saumon)."""
    for s in (1, -1):
        m.plate([(x_le_root, s * y_root, z_root), (x_le_tip, s * y_tip, z_tip),
                 (x_te_tip, s * y_tip, z_tip), (x_te_root, s * y_root, z_root)], th, "paint", tint)


def prop(m, x, z, r, blades=2, y=0.0, mat="dark"):
    """Hélice (pales) dans le plan y-z, centrée en (x, y, z)."""
    m.loft_x([(x - 0.3, 0.2, 0.2, z), (x + 0.3, 0.3, 0.3, z)], "metal", 8)
    for k in range(blades):
        a = math.radians(90 + 360 * k / blades)
        dy, dz = math.cos(a), math.sin(a)
        pr = Model().plate([(x - 0.1, dy * 0.3, z + dz * 0.3), (x + 0.1, dy * 0.3, z + dz * 0.3),
                            (x, dy * r, z + dz * r), (x - 0.2, dy * (r - 0.3), z + dz * (r - 0.3))], 0.2, mat)
        m.solids += shift_y(pr, y).solids


def sensor_ball(m, x, z, r, y=0.0):
    ball = Model().loft_x([(x - r, 0.2, 0.2, z), (x - r * 0.5, r, r, z), (x + r * 0.5, r, r, z),
                           (x + r, 0.2, 0.2, z)], "dark", 10)
    ball.box(x + r * 0.6, x + r * 1.05, -0.3, 0.3, z - 0.3, z + 0.3, "glass")
    m.solids += shift_y(ball, y).solids


def missile_under(m, x, y, z, length=2.4, r=0.22):
    mis = Model().loft_x([(x - length / 2, r, r, z), (x + length / 2 - 0.4, r, r, z), (x + length / 2, 0.06, 0.06, z)],
                         "metal", 6)
    for a in (45, 135, 225, 315):
        dy, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        mis.plate([(x - length / 2, 0, z), (x - length / 2 + 0.5, 0, z),
                   (x - length / 2 + 0.3, dy * 0.6, z + dz * 0.6), (x - length / 2, dy * 0.6, z + dz * 0.6)],
                  0.1, "metal")
    m.solids += shift_y(mis, y).solids


def antenna(m, x, z, h, y=0.0, down=False):
    sgn = -1 if down else 1
    m.plate([(x - 0.4, y, z), (x + 0.4, y, z), (x + 0.1, y, z + sgn * h), (x - 0.2, y, z + sgn * h)], 0.12, "metal")


# ===========================================================================
# ALLEMAGNE
# ===========================================================================
def kzo():
    """KZO (Rheinmetall) : fuselage trapu à section carrée, ailes droites à
    saumons relevés, hélice propulsive carénée, dérives jumelles, boule
    optronique ventrale. Agrandi ~2x (envergure réelle 3,4 m)."""
    m = Model()
    m.loft_x([(-5.2, 0.9, 0.8, 0.2), (-3.5, 1.4, 1.2, 0.2), (2.0, 1.5, 1.3, 0.2),
              (4.2, 1.2, 1.1, 0.1), (5.4, 0.6, 0.6, 0.0)], "paint", 8)          # section presque carrée
    m.box(-2.5, 2.5, -0.8, 0.8, 1.4, 1.8, "paint", 0.1)                            # capot dorsal
    wing(m, 1.2, -0.8, 0.9, -0.6, 1.3, 7.0, 0.9, 1.0, 0.5)
    for s in (1, -1):
        m.plate([(0.9, s * 7.0, 1.0), (-0.6, s * 7.0, 1.0), (-0.8, s * 7.1, 2.6), (0.4, s * 7.1, 2.6)],
                0.35, "paint", 0.12)                                               # saumons relevés
        m.plate([(-3.4, s * 1.2, 0.6), (-5.4, s * 1.2, 0.6), (-6.0, s * 1.6, 3.0), (-4.6, s * 1.6, 3.0)],
                0.35)                                                              # dérives jumelles
    m.plate([(-4.6, -1.6, 2.2), (-4.6, 1.6, 2.2), (-5.8, 1.6, 2.2), (-5.8, -1.6, 2.2)], 0.3)  # stabilisateur
    # Carénage annulaire de l'hélice propulsive
    for k in range(10):
        a0, a1 = 2 * math.pi * k / 10, 2 * math.pi * (k + 1) / 10
        m.plate([(-6.4, 1.9 * math.cos(a0), 0.2 + 1.9 * math.sin(a0)), (-5.6, 1.9 * math.cos(a0), 0.2 + 1.9 * math.sin(a0)),
                 (-5.6, 1.9 * math.cos(a1), 0.2 + 1.9 * math.sin(a1)), (-6.4, 1.9 * math.cos(a1), 0.2 + 1.9 * math.sin(a1))],
                0.25, "paint", 0.18)
    prop(m, -6.0, 0.2, 1.7, blades=3)
    sensor_ball(m, 3.2, -1.3, 0.8)
    antenna(m, 0.5, 1.8, 1.2)
    m.box(-1.0, 0.0, -0.3, 0.3, -1.3, -0.9, "dark")                                # parachute de récupération
    return m


def luna():
    """LUNA X-2000 : planeur « pod-and-boom », longues ailes fines, moteur
    propulsif au-dessus de l'aile, poutre de queue mince et empennage en V.
    Agrandi ~2,5x (envergure réelle 4,2 m)."""
    m = Model()
    m.loft_x([(-2.5, 0.4, 0.4, 0.0), (-1.0, 1.0, 1.0, 0.0), (2.5, 1.1, 1.1, 0.0),
              (4.2, 0.8, 0.8, -0.1), (5.0, 0.3, 0.3, -0.2)], "paint", 10)
    m.cylinder_x(-9.5, -2.0, 0, 0.4, 0.3, "paint")                                 # poutre de queue
    wing(m, 1.4, -0.2, 1.0, 0.1, 0.6, 10.5, 1.1, 1.6, 0.4)
    for s in (1, -1):
        m.plate([(-0.1, s * 7.0, 1.4), (-0.1, s * 10.4, 1.6), (-0.4, s * 10.4, 1.6), (-0.4, s * 7.0, 1.4)],
                0.45, "paint", 0.14)
        m.plate([(-8.2, s * 0.3, 0.5), (-9.8, s * 0.3, 0.5), (-10.3, s * 3.0, 2.6), (-9.2, s * 3.0, 2.6)], 0.3)
    m.loft_x([(-1.6, 0.3, 0.3, 2.0), (-0.8, 0.55, 0.5, 2.0), (0.8, 0.5, 0.45, 2.0)], "paint", 8, tint=0.1)  # moteur
    m.box(-0.3, 0.3, -0.25, 0.25, 1.2, 1.6, "dark")                                # mât moteur
    prop(m, -1.8, 2.0, 1.4)
    # Tourelle du désignateur laser (optique verte)
    ball = Model().loft_x([(2.6, 0.2, 0.2, -1.2), (3.0, 0.7, 0.7, -1.3), (3.8, 0.7, 0.7, -1.3), (4.2, 0.2, 0.2, -1.2)],
                          "dark", 10)
    m.solids += ball.solids
    m.box(4.0, 4.4, -0.35, 0.35, -1.6, -1.0, "glass")
    antenna(m, 1.0, 1.1, 1.0)
    return m


def aladin():
    """ALADIN : mini-drone lancé à la main, aile haute sur pylône, hélice
    tractrice, empennage classique ; ici équipé de nacelles de brouillage
    et d'antennes ECM. Agrandi ~5x (envergure réelle 1,5 m)."""
    m = Model()
    m.loft_x([(-7.5, 0.3, 0.3, 0.2), (-4.0, 0.7, 0.8, 0.1), (1.5, 1.0, 1.1, 0.0),
              (3.6, 0.9, 1.0, 0.0), (4.4, 0.4, 0.5, 0.0)], "paint", 10)
    m.box(-0.6, 1.2, -0.35, 0.35, 1.0, 2.0, "paint", 0.1)                          # pylône d'aile
    wing(m, 1.8, 0.0, 1.5, 0.2, 0.3, 7.5, 2.1, 2.3, 0.4)
    m.plate([(-5.8, 0, 0.6), (-7.6, 0, 0.6), (-8.0, 0, 3.2), (-7.0, 0, 3.2)], 0.3)   # dérive
    m.plate([(-6.6, -2.8, 0.5), (-6.6, 2.8, 0.5), (-7.8, 2.8, 0.5), (-7.8, -2.8, 0.5)], 0.3)
    prop(m, 4.7, 0.0, 1.6)
    for s in (1, -1):                                                              # nacelles de brouillage
        pod = Model().loft_x([(-0.8, 0.35, 0.35, 1.6), (1.6, 0.35, 0.35, 1.6), (2.1, 0.12, 0.12, 1.6)], "dark", 8)
        m.solids += shift_y(pod, s * 4.5).solids
        for dx in (-0.5, 0.6):
            antenna(m, dx, 2.3, 1.4, y=s * 4.5)
        antenna(m, 0.3, 1.2, 1.1, y=s * 4.5, down=True)
    for dx in (-2.5, -1.2):                                                        # antennes dorsales ECM
        antenna(m, dx, 1.0, 1.6)
    m.box(2.0, 2.8, -0.3, 0.3, -1.2, -0.8, "glass")
    return m


# ===========================================================================
# ROYAUME-UNI
# ===========================================================================
def watchkeeper():
    """Watchkeeper WK450 (dérivé Hermes 450) : fuselage fin, ailes droites
    d'allongement élevé, empennage en V inversé, hélice propulsive, boule
    optronique avant et radar SAR/GMTI en nacelle ventrale. Agrandi ~1,6x."""
    m = Model()
    m.loft_x([(-8.0, 0.3, 0.3, 0.3), (-6.5, 0.7, 0.7, 0.2), (-2.0, 1.1, 1.1, 0.1),
              (3.5, 1.15, 1.2, 0.1), (6.0, 0.9, 1.0, 0.1), (7.2, 0.35, 0.4, 0.0)], "paint", 12)
    wing(m, 1.4, -0.4, 1.0, -0.2, 1.0, 14.0, 1.0, 1.4, 0.45)
    for s in (1, -1):
        m.plate([(-0.2, s * 9.0, 1.2), (-0.2, s * 13.8, 1.4), (-0.6, s * 13.8, 1.4), (-0.6, s * 9.0, 1.2)],
                0.5, "paint", 0.14)
        m.plate([(-5.8, s * 0.5, 0.0), (-7.8, s * 0.5, 0.0), (-8.4, s * 4.0, -2.4), (-7.2, s * 4.0, -2.4)], 0.35)
    prop(m, -8.4, 0.3, 2.4)
    sensor_ball(m, 5.0, -1.3, 0.8)
    m.loft_x([(-2.5, 0.3, 0.2, -1.2), (-1.5, 0.7, 0.5, -1.3), (1.8, 0.7, 0.5, -1.3), (2.6, 0.3, 0.2, -1.2)],
             "paint", 10, tint=0.16)                                                # radar SAR/GMTI
    antenna(m, 1.5, 1.2, 1.3)
    m.loft_x([(2.5, 0.3, 0.2, 1.2), (3.5, 0.6, 0.35, 1.3), (5.0, 0.3, 0.2, 1.2)], "paint", 8, tint=-0.05)  # SATCOM
    return m


def protector():
    """Protector RG Mk1 (MQ-9B SkyGuardian) : silhouette de Reaper mais ailes
    beaucoup plus longues (24 m) munies de winglets, antennes de liaison,
    2 missiles légers guidés sous chaque aile."""
    m = Model()
    m.loft_x([(-9.6, 0.35, 0.35, 0.2), (-8.2, 0.75, 0.75, 0.2), (-4.0, 1.3, 1.25, 0.1),
              (1.0, 1.5, 1.45, 0.1), (5.0, 1.45, 1.65, 0.4), (7.6, 1.25, 1.6, 0.6),
              (9.2, 0.8, 1.0, 0.5), (10.0, 0.3, 0.4, 0.3)], "paint", 14)
    m.loft_x([(4.0, 0.6, 0.3, 1.7), (5.6, 1.2, 0.85, 1.8), (7.4, 1.05, 0.75, 1.7), (8.6, 0.4, 0.25, 1.4)],
             "paint", 10, tint=-0.05)                                               # dôme SATCOM
    sensor_ball(m, 7.2, -1.6, 0.75)
    wing(m, 1.4, -1.4, 1.1, -0.4, 1.2, 20.0, 0.2, 0.9, 0.5)
    for s in (1, -1):
        m.plate([(1.1, s * 20.0, 0.9), (-0.4, s * 20.0, 0.9), (-0.7, s * 20.3, 3.2), (0.2, s * 20.3, 3.2)],
                0.35, "paint", 0.1)                                                 # winglets
        m.plate([(-6.4, s * 0.5, 0.8), (-8.6, s * 0.5, 0.8), (-9.4, s * 4.6, 4.3), (-8.2, s * 4.6, 4.3)], 0.4)
        m.box(-0.5, 0.9, s * 7.0 - 0.2, s * 7.0 + 0.2, -0.3, 0.3, "dark")
        missile_under(m, 0.3, s * 7.0, -0.6, 3.0, 0.25)                             # missile léger guidé
        m.box(-0.1, 0.5, s * 20.1 - 0.2, s * 20.1 + 0.2, 1.0, 1.4, "glass")
    m.plate([(-6.8, 0, -0.9), (-8.6, 0, -0.8), (-9.2, 0, -3.2), (-8.4, 0, -3.2)], 0.4, "paint", 0.06)
    prop(m, -9.9, 0.2, 3.0, blades=3)
    for dx in (2.0, -1.5, -3.5):
        antenna(m, dx, 1.4, 1.0)
    return m


def black_hornet():
    """Black Hornet : nano-hélicoptère (16 cm). Fuselage en goutte, rotor
    principal bipale, rotor anticouple en queue, caméras dans le nez.
    Agrandi ~25x pour rester visible."""
    m = Model()
    m.loft_x([(-6.0, 0.25, 0.3, 0.8), (-3.0, 0.5, 0.6, 0.6), (-0.5, 1.4, 1.6, 0.2),
              (1.8, 1.5, 1.6, 0.1), (3.2, 1.0, 1.1, 0.0), (3.9, 0.3, 0.3, -0.1)], "paint", 12)
    m.box(3.2, 3.8, -0.8, 0.8, -0.5, 0.3, "glass")                                 # caméras
    m.cylinder_x(-0.4, 0.4, 0, 2.3, 0.4, "metal")                                  # mât rotor
    m.loft_x([(-0.4, 0.2, 0.2, 2.0), (0.4, 0.35, 0.35, 2.0)], "metal", 8)
    for s in (1, -1):                                                              # rotor principal bipale
        m.plate([(0.4, 0, 2.5), (-0.4, 0, 2.5), (-0.5, s * 7.5, 2.6), (0.3, s * 7.5, 2.6)], 0.2, "dark")
    m.plate([(-5.2, 0, 0.8), (-6.4, 0, 0.8), (-6.6, 0, 2.2), (-5.8, 0, 2.2)], 0.25)     # dérive
    for s in (1, -1):                                                              # rotor anticouple
        m.plate([(-6.2, 0.3, 1.5), (-6.0, 0.3, 1.5), (-6.1, 0.3, 1.5 + s * 1.3), (-6.3, 0.3, 1.5 + s * 1.2)],
                0.15, "dark")
    return m


# ===========================================================================
# UKRAINE
# ===========================================================================
def leleka_air():
    """Leleka-100 en vol (sans altitude figée : le jeu gère l'altitude et l'ombre)."""
    import models
    return models.leleka().transformed(lambda x, y, z: (x, y, z - 11.0))


def shark():
    """Shark (Ukrspecsystems) : bipoutre, aile haute rectangulaire, hélice
    propulsive entre les poutres, empennage en V inversé reliant les poutres,
    grosse boule optronique ventrale. Agrandi ~2x."""
    m = Model()
    m.loft_x([(-3.0, 0.5, 0.5, 0.4), (-1.5, 1.1, 1.1, 0.3), (3.0, 1.2, 1.2, 0.2),
              (4.8, 0.8, 0.9, 0.1), (5.6, 0.3, 0.35, 0.0)], "paint", 12)
    wing(m, 1.8, -0.4, 1.6, -0.2, 1.1, 10.5, 1.2, 1.5, 0.45)
    for s in (1, -1):
        m.plate([(-0.2, s * 7.0, 1.4), (-0.2, s * 10.3, 1.5), (-0.5, s * 10.3, 1.5), (-0.5, s * 7.0, 1.4)],
                0.5, "paint", 0.14)
        boom = Model().loft_x([(-9.0, 0.25, 0.25, 1.0), (1.2, 0.35, 0.35, 1.1), (2.0, 0.2, 0.2, 1.1)], "paint", 8)
        m.solids += shift_y(boom, s * 3.0).solids
        m.plate([(-7.6, s * 3.0, 1.2), (-9.2, s * 3.0, 1.2), (-9.5, s * 1.0, 3.2), (-8.3, s * 1.0, 3.2)], 0.35)
    prop(m, -3.4, 0.4, 2.2)
    sensor_ball(m, 3.0, -1.4, 1.0)
    antenna(m, 0.5, 1.3, 1.1)
    return m


def fpv_quad():
    """Drone FPV kamikaze : châssis en X, 4 moteurs et hélices, batterie sur le
    dos, charge (ogive de RPG) fixée dessous, pointée vers l'avant. Agrandi ~15x."""
    m = Model()
    m.box(-1.2, 1.2, -1.0, 1.0, 0.0, 0.5, "dark")                                  # plaque centrale
    m.box(-1.0, 0.8, -0.7, 0.7, 0.5, 1.3, "paint")                                 # batterie
    m.box(0.9, 1.3, -0.3, 0.3, 0.5, 1.1, "glass")                                  # caméra FPV
    for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        m.plate([(0.3 * sx, 0.3 * sy, 0.25), (0.6 * sx, 0.0, 0.25),
                 (3.6 * sx, 3.3 * sy, 0.25), (3.3 * sx, 3.6 * sy, 0.25)], 0.3, "dark")   # bras
        mot = Model().loft_x([(3.1 * sx - 0.5, 0.5, 0.5, 0.6), (3.1 * sx + 0.5, 0.5, 0.5, 0.6)], "metal", 8)
        m.solids += shift_y(mot, 3.1 * sy).solids
        for k in range(2):                                                          # hélices bipales
            a = math.radians(30 + 90 * k + (0 if sx * sy > 0 else 45))
            m.plate([(3.1 * sx - 1.8 * math.cos(a), 3.1 * sy - 1.8 * math.sin(a), 1.2),
                     (3.1 * sx - 1.6 * math.cos(a) - 0.3 * math.sin(a), 3.1 * sy - 1.6 * math.sin(a) + 0.3 * math.cos(a), 1.2),
                     (3.1 * sx + 1.8 * math.cos(a), 3.1 * sy + 1.8 * math.sin(a), 1.2),
                     (3.1 * sx + 1.6 * math.cos(a) + 0.3 * math.sin(a), 3.1 * sy + 1.6 * math.sin(a) - 0.3 * math.cos(a), 1.2)],
                    0.12, "metal")
    m.loft_x([(-1.6, 0.45, 0.45, -0.6), (0.8, 0.45, 0.45, -0.6), (1.6, 0.8, 0.8, -0.6),
              (2.8, 0.8, 0.8, -0.6), (3.6, 0.2, 0.2, -0.6)], "paint", 10, tint=0.15)  # ogive de RPG
    return m


# ===========================================================================
# RUSSIE
# ===========================================================================
def orlan10():
    """Orlan-10 : petit avion à aile haute haubanée, hélice tractrice, nez
    arrondi, empennage classique, boule optique sous le fuselage. Agrandi ~2,5x."""
    m = Model()
    m.loft_x([(-7.5, 0.35, 0.35, 0.5), (-4.0, 0.8, 0.9, 0.3), (1.0, 1.1, 1.2, 0.1),
              (3.8, 1.0, 1.1, 0.0), (4.8, 0.5, 0.55, 0.0)], "paint", 12)
    wing(m, 1.8, 0.0, 1.6, 0.2, 0.3, 7.8, 1.4, 1.7, 0.4)
    for s in (1, -1):                                                              # haubans
        m.plate([(0.9, s * 0.9, -0.3), (1.1, s * 0.9, -0.3), (1.0, s * 4.2, 1.5), (0.8, s * 4.2, 1.5)], 0.15, "metal")
    m.plate([(-6.0, 0, 0.8), (-7.7, 0, 0.8), (-8.1, 0, 3.4), (-7.1, 0, 3.4)], 0.3)
    m.plate([(-6.6, -3.0, 0.7), (-6.6, 3.0, 0.7), (-7.9, 3.0, 0.7), (-7.9, -3.0, 0.7)], 0.3)
    prop(m, 5.1, 0.0, 1.9)
    sensor_ball(m, 1.8, -1.4, 0.7)
    antenna(m, -2.0, 1.1, 1.3)
    m.box(-3.4, -2.0, -0.5, 0.5, 1.1, 1.5, "dark")                                 # conteneur parachute
    return m


def lancet():
    """ZALA Lancet : corps cylindrique, double jeu d'ailes en X (petites à
    l'avant, grandes à l'arrière), hélice propulsive, caméra dans le nez.
    Agrandi ~5x."""
    m = Model()
    m.loft_x([(-6.0, 0.45, 0.45, 0), (-5.4, 0.85, 0.85, 0), (3.8, 0.85, 0.85, 0),
              (5.2, 0.7, 0.7, 0), (6.0, 0.35, 0.35, 0)], "paint", 12)
    m.loft_x([(5.9, 0.36, 0.36, 0), (6.4, 0.1, 0.1, 0)], "glass", 8)
    for a in (45, 135, 225, 315):
        dy, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        m.plate([(3.6, dy * 0.7, dz * 0.7), (2.2, dy * 0.7, dz * 0.7),
                 (2.4, dy * 3.8, dz * 3.8), (3.2, dy * 3.8, dz * 3.8)], 0.22)               # X avant
        m.plate([(-1.4, dy * 0.7, dz * 0.7), (-4.2, dy * 0.7, dz * 0.7),
                 (-4.0, dy * 6.0, dz * 6.0), (-2.4, dy * 6.0, dz * 6.0)], 0.22, "paint", 0.08)  # X arrière
    m.loft_x([(-6.8, 0.15, 0.15, 0), (-6.1, 0.3, 0.3, 0)], "dark", 8)
    for a in (90, 270):
        dy, dz = math.cos(math.radians(a)), math.sin(math.radians(a))
        m.plate([(-6.6, dy * 0.2, dz * 0.2), (-6.4, dy * 0.2, dz * 0.2),
                 (-6.5, dy * 2.4, dz * 2.4), (-6.7, dy * 2.2, dz * 2.2)], 0.2, "dark")
    m.loft_x([(1.8, 0.9, 0.9, 0), (2.4, 0.9, 0.9, 0)], "paint", 12, tint=0.2)   # bague de charge
    return m


def orion():
    """Kronshtadt Orion : drone MALE russe, fuselage épais à nez bombé, ailes
    droites effilées, empennage en V, hélice propulsive, boule optronique
    et 2 missiles air-sol sous les ailes."""
    m = Model()
    m.loft_x([(-8.4, 0.35, 0.35, 0.3), (-7.0, 0.8, 0.8, 0.2), (-3.0, 1.35, 1.3, 0.1),
              (2.5, 1.5, 1.5, 0.1), (5.5, 1.35, 1.55, 0.3), (7.4, 0.9, 1.1, 0.3), (8.2, 0.3, 0.4, 0.2)],
             "paint", 14)
    wing(m, 1.6, -0.8, 0.9, -0.3, 1.3, 16.0, 0.6, 1.2, 0.5)
    for s in (1, -1):
        m.plate([(-0.4, s * 10.0, 1.0), (-0.4, s * 15.8, 1.2), (-0.8, s * 15.8, 1.2), (-0.9, s * 10.0, 1.0)],
                0.55, "paint", 0.14)
        m.plate([(-5.8, s * 0.5, 0.9), (-7.9, s * 0.5, 0.9), (-8.6, s * 4.2, 4.0), (-7.5, s * 4.2, 4.0)], 0.4)
        m.box(-0.4, 1.0, s * 5.5 - 0.2, s * 5.5 + 0.2, 0.2, 0.6, "dark")
        missile_under(m, 0.4, s * 5.5, -0.2, 3.2, 0.3)                              # Kh-BPLA
    prop(m, -8.8, 0.3, 2.6, blades=3)
    sensor_ball(m, 5.8, -1.6, 0.9)
    antenna(m, 1.0, 1.5, 1.3)
    antenna(m, -3.0, -1.2, 1.0, down=True)
    return m
