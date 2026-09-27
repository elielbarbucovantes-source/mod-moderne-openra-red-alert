"""Génère les feuilles de sprites PNG des véhicules RATC dans mods/ratc/bits/.

Usage : python3 build.py CHEMIN/temperat.pal [nom ...]
(temperat.pal s'extrait avec : ./utility.sh --extract temperat.pal)
"""
import math
import os
import sys
import render
import models
import aircraft
from render import Model

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "mods", "ratc", "bits")
SIZE = (48, 48)

# nom -> (fonction du modèle, couleur de l'icône, nom affiché sur l'icône)
VEHICLES = {
    "leopard": (models.leopard, (84, 96, 58), "LEOPARD 2"),
    "leclerc": (models.leclerc, (128, 136, 96), "LECLERC"),
    "challenger": (models.challenger, (150, 132, 92), "CHALL. 3"),
    "t90m": (models.t90m, (70, 88, 52), "T-90M"),
    "bmpt": (models.bmpt, (78, 90, 56), "BMPT"),
    "jaguar": (models.jaguar, (100, 104, 72), "JAGUAR"),
    "pzh": (models.pzh, (84, 96, 58), "PZH 2000"),
    "as90": (models.as90, (150, 132, 92), "AS-90"),
    "cesar": (models.cesar, (100, 104, 72), "CAESAR"),
    "m777": (models.m777, (90, 98, 64), "M777"),
    "grad": (models.grad, (82, 96, 60), "BM-21 GRAD"),
    "ravit": (models.ravit, (96, 104, 70), "RAVITAILL."),
    # Japon
    "type10": (models.type10, (96, 104, 70), "TYPE 10"),
    "type16": (models.type16, (96, 104, 70), "TYPE 16"),
    "type19": (models.type19, (96, 104, 70), "TYPE 19"),
    # Inde
    "arjun": (models.arjun, (150, 128, 84), "ARJUN"),
    "namica": (models.namica, (150, 128, 84), "NAG"),
    "dhanush": (models.dhanush, (150, 128, 84), "DHANUSH"),
}


# Aéronefs : nom -> (modèle, taille d'image, échelle de l'icône, couleur, nom affiché)
AIRCRAFT = {
    "reaper": (aircraft.reaper, (64, 64), 1.05, (132, 136, 134), "REAPER"),
    "patroller": (aircraft.patroller, (64, 64), 1.25, (150, 152, 146), "PATROLLER"),
    "colibri": (aircraft.colibri, (32, 32), 3.4, (110, 116, 100), "COLIBRI"),
    # Allemagne
    "kzo": (aircraft.kzo, (48, 48), 2.0, (120, 128, 110), "KZO"),
    "luna": (aircraft.luna, (48, 48), 1.7, (140, 144, 138), "LUNA"),
    "aladin": (aircraft.aladin, (48, 48), 1.9, (110, 118, 96), "ALADIN"),
    # Royaume-Uni
    "watchkeeper": (aircraft.watchkeeper, (64, 64), 1.3, (136, 140, 140), "WK450"),
    "protector": (aircraft.protector, (64, 64), 0.8, (150, 154, 156), "PROTECTOR"),
    "blackhornet": (aircraft.black_hornet, (32, 32), 2.6, (70, 72, 64), "HORNET"),
    # Ukraine
    "leleka": (aircraft.leleka_air, (48, 48), 1.5, (120, 124, 120), "LELEKA"),
    "shark": (aircraft.shark, (48, 48), 1.7, (132, 138, 136), "SHARK"),
    "fpvquad": (aircraft.fpv_quad, (24, 24), 4.0, (90, 96, 70), "FPV"),
    # Russie
    "orlan10": (aircraft.orlan10, (48, 48), 2.0, (150, 150, 146), "ORLAN-10"),
    "lancet": (aircraft.lancet, (32, 32), 3.0, (120, 124, 116), "LANCET"),
    "orion": (aircraft.orion, (64, 64), 1.0, (140, 144, 146), "ORION"),
    # Japon
    "seaguardian": (aircraft.seaguardian, (64, 64), 0.8, (150, 154, 156), "SEAGUARD"),
    # Inde
    "tapas": (aircraft.tapas, (64, 64), 1.1, (140, 144, 138), "TAPAS"),
}
SKY = ((104, 140, 176), (176, 196, 208))
# Échelle d'icône propre à certains véhicules (défaut : 1.25).
ICON_SCALE = {"leclerc": 1.4}


def build_aircraft(name, palette):
    fn, size, icon_scale, color, title = AIRCRAFT[name]
    model = fn()
    frames = render.render_rotations(model, size, shadow=False)     # l'ombre est dessinée par le jeu
    if name == "colibri":                                          # image du piqué final
        frames.append(render.outline(render.render_frame(aircraft.colibri_diving(), 0.0, size, shadow=False)))
    render.save_sheet(frames, os.path.join(OUT, f"{name}.png"), palette)
    icon = render.render_icon(model, palette, scale=icon_scale, facing=0.86, paint=color, bg=SKY)
    render.save_sheet([render.label(icon, title)], os.path.join(OUT, f"{name}icon.png"), palette)
    print(f"{name}: {len(frames)} images + icône")


def combined(hull, turret, offset):
    """Caisse + tourelle en un seul modèle (pour l'icône)."""
    m = Model()
    m.__dict__.update({k: v for k, v in vars(hull).items() if k != "solids"})
    m.solids = list(hull.solids)
    for s in turret.solids:
        if s[0] in ("quad", "poly"):
            m.solids.append((s[0], [(x + offset, y, z) for x, y, z in s[1]], s[2], s[3]))
        else:
            b, t, mat, tint = s
            m.solids.append(([(x + offset, y, z) for x, y, z in b], [(x + offset, y, z) for x, y, z in t], mat, tint))
    return m


def build(name, palette):
    fn, icon_color, title = VEHICLES[name]
    built = fn()
    if isinstance(built, tuple):
        hull, turret, offset = built
        frames = render.render_rotations(hull, SIZE) + render.render_rotations(turret, SIZE, shadow=False)
        icon_model = combined(hull, turret, offset)
    else:
        frames = render.render_rotations(built, SIZE)
        icon_model = built
    render.save_sheet(frames, os.path.join(OUT, f"{name}.png"), palette)
    icon = render.label(render.render_icon(icon_model, palette, scale=ICON_SCALE.get(name, 1.25), paint=icon_color), title)
    render.save_sheet([icon], os.path.join(OUT, f"{name}icon.png"), palette)
    print(f"{name}: {len(frames)} images + icône")


if __name__ == "__main__":
    pal = render.load_palette(sys.argv[1])
    for n in sys.argv[2:] or list(VEHICLES) + list(AIRCRAFT):
        (build_aircraft if n in AIRCRAFT else build)(n, pal)
