"""Génère « Encyclopédie ultime du mod.txt » à la racine du dépôt.

Les statistiques sont lues dans les règles du jeu (regles.py, stats.py) : relancer
ce script après un rééquilibrage met l'encyclopédie à jour. Le lore et les
stratégies sont dans textes_*.py.

Usage : python3 tools/encyclopedie/generer.py
"""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(__file__))
import regles  # noqa: E402
import stats  # noqa: E402
from textes_vehicules import TEXTES as T_VEH  # noqa: E402
from textes_infanterie import TEXTES as T_INF  # noqa: E402
from textes_air_mer import TEXTES as T_AIRMER  # noqa: E402
from textes_batiments import TEXTES as T_BAT  # noqa: E402
from textes_pouvoirs import TEXTES as T_POW  # noqa: E402

SORTIE = os.path.join(regles.ROOT, "Encyclopédie ultime du mod.txt")
LARGEUR = 92
TEXTES = {**T_VEH, **T_INF, **T_AIRMER, **T_BAT}
LEURRES = {"ATEF", "DOMF", "FACF", "FAPW", "FIXF", "FPWR", "MSLF", "PDOF", "SYRF", "TENF", "WEAF"}

SECTIONS = [
    ("BÂTIMENTS", lambda s: s["queue"] == "Building"),
    ("DÉFENSES ET SUPERARMES", lambda s: s["queue"] == "Defense" and s["key"] not in LEURRES),
    ("LEURRES", lambda s: s["key"] in LEURRES),
    ("INFANTERIE", lambda s: s["queue"] == "Infantry"),
    ("VÉHICULES", lambda s: s["queue"] == "Vehicle"),
    ("AVIATION", lambda s: s["queue"] == "Aircraft"),
    ("MARINE", lambda s: s["queue"] == "Ship"),
]
ORDRE_FACTIONS = ["toutes", "tous les Alliés", "tous les Soviétiques", "France", "Allemagne", "Royaume-Uni",
                  "USA", "Espagne", "Japon", "Russie", "Ukraine", "Chine", "Turquie", "Grèce", "Inde"]


def ordre_faction(f):
    for i, nom in enumerate(ORDRE_FACTIONS):
        if f == nom:
            return i
    return len(ORDRE_FACTIONS)


def para(texte, retrait="    "):
    return textwrap.fill(texte, LARGEUR, initial_indent=retrait, subsequent_indent=retrait)


def bloc_stats(s):
    lignes = []
    l1 = []
    if s["cost"]:
        l1.append(f"Coût {stats.fmt_int(s['cost'])} $")
    if s["hp"]:
        l1.append(f"PV {stats.fmt_int(s['hp'])}")
    if s["armor"]:
        l1.append("Blindage " + " + ".join(s["armor"]))
    if s["speed"]:
        l1.append(f"Vitesse {s['speed']}")
    if s["vision"]:
        l1.append(f"Vision {stats.fmt_cells(s['vision'])}")
    if l1:
        lignes.append(" · ".join(l1))
    for w in s["weapons"]:
        lignes.append("Arme : " + stats.weapon_line(w))
    if not s["weapons"] and s["queue"] in ("Infantry", "Vehicle", "Aircraft", "Ship"):
        lignes.append("Arme : aucune")
    l3 = []
    if s["power"]:
        p = int(s["power"])
        l3.append(f"Énergie {'+' if p > 0 else ''}{p}")
    if s["cargo"]:
        l3.append(f"Transport {s['cargo']} places")
    if s["cloak"]:
        l3.append("Furtif")
    if s["detect"]:
        l3.append(f"Détecte les furtifs ({stats.fmt_cells(s['detect'])})")
    if s["limit"]:
        l3.append(f"Limite {s['limit']} exemplaire{'s' if int(s['limit']) > 1 else ''}")
    if l3:
        lignes.append(" · ".join(l3))
    req = f"Prérequis : {s['prereq_text']}"
    if s["techlevel"]:
        req += f" · Niveau technologique : {s['techlevel']}"
    lignes.append(req)
    for p in s["powers"]:
        charge = f" (recharge {stats.fmt_ticks(p['charge'])})" if p["charge"] else ""
        nom = T_POW.get(p["name"], (p["name"],))[0]
        lignes.append(f"Pouvoir de soutien : {nom}{charge}")
    return lignes


def entree(s, manquants):
    nom, lore, strat = TEXTES.get(s["key"], (None, None, None))
    if nom is None:
        manquants.append(s["key"])
        nom = s["name"]
    titre = nom.upper()
    if s["name"] and s["name"].lower() != nom.lower():
        titre += f"  ({s['name']})"
    out = ["-" * LARGEUR, f"■ {titre}", f"  Faction : {s['faction']}"]
    if lore:
        out.append("  Lore :")
        out += ["    " + l.strip() for l in lore.strip().splitlines()]
    out.append("  Statistiques :")
    for l in bloc_stats(s):
        out.append(para(l, "    ").replace("    ", "    ", 1))
    if strat:
        out.append("  Stratégie :")
        out.append(para(strat))
    return out


def main():
    R = regles.load_rules()
    W = regles.load_weapons()
    tous = [stats.actor_stats(R, W, k) for k in stats.buildable(R)]
    manquants = []
    out = []
    out += ["=" * LARGEUR,
            "ENCYCLOPÉDIE ULTIME DU MOD".center(LARGEUR),
            "Mod moderne pour OpenRA Red Alert".center(LARGEUR),
            "=" * LARGEUR, "",
            para("Chaque bâtiment, défense, unité et pouvoir de soutien du jeu : un peu d'histoire, "
                 "les statistiques et la façon de s'en servir.", ""),
            "",
            para("Les statistiques sont lues directement dans les règles du jeu par "
                 "tools/encyclopedie/generer.py : après un rééquilibrage, relancez ce script pour mettre "
                 "l'encyclopédie à jour.", ""),
            "",
            "Repères :",
            "  • PV : points de vie. Une case = une case de la carte.",
            "  • Les durées sont données à la vitesse de jeu normale (25 images par seconde).",
            "  • Faction « toutes » : disponible pour tout le monde ; « tous les Alliés » / « tous les",
            "    Soviétiques » : pour toutes les nations du camp.",
            "  • Blindage : aucun (infanterie), léger, lourd, béton, léger de bâtiment (bois) ; le blindage",
            "    réactif (ERA) et la protection active (APS) réduisent les dégâts des missiles antichar.",
            ""]
    sommaire = []
    corps = []
    for i, (titre, filtre) in enumerate(SECTIONS, 1):
        items = sorted((s for s in tous if filtre(s)),
                       key=lambda s: (ordre_faction(s["faction"]), TEXTES.get(s["key"], (s["name"],))[0].lower()))
        sommaire.append(f"  {i}. {titre} ({len(items)})")
        corps += ["", "=" * LARGEUR, f"{i}. {titre}".center(LARGEUR), "=" * LARGEUR]
        faction_courante = None
        for s in items:
            if s["faction"] != faction_courante:
                faction_courante = s["faction"]
                corps += ["", f"  ▶ Faction : {faction_courante}".upper(), ""]
            corps += entree(s, manquants)
    # Pouvoirs de soutien, regroupés par nom
    pouvoirs = {}
    for s in tous:
        for p in s["powers"]:
            pouvoirs.setdefault(p["name"], []).append((s, p))
    n = len(SECTIONS) + 1
    sommaire.append(f"  {n}. POUVOIRS DE SOUTIEN ({len(pouvoirs)})")
    corps += ["", "=" * LARGEUR, f"{n}. POUVOIRS DE SOUTIEN".center(LARGEUR), "=" * LARGEUR]
    for nom_regles, porteurs in sorted(pouvoirs.items(), key=lambda kv: T_POW.get(kv[0], (kv[0],))[0].lower()):
        nom, lore, strat = T_POW.get(nom_regles, (None, None, None))
        if nom is None:
            manquants.append(f"pouvoir « {nom_regles} »")
            nom = nom_regles
        corps += ["-" * LARGEUR, f"■ {nom.upper()}"]
        if lore:
            corps.append("  Lore :")
            corps += ["    " + l.strip() for l in lore.strip().splitlines()]
        corps.append("  Statistiques :")
        vus = set()
        for s, p in porteurs:
            porteur = TEXTES.get(s["key"], (s["name"],))[0]
            if porteur in vus:
                continue
            vus.add(porteur)
            charge = f", recharge {stats.fmt_ticks(p['charge'])}" if p["charge"] else ""
            corps.append(para(f"Porté par : {porteur} ({s['faction']}){charge}"))
        desc = porteurs[0][1]["description"]
        if desc and not lore:                       # sinon le lore décrit déjà l'effet, en français
            corps.append(para(f"Effet : {desc}"))
        if strat:
            corps.append("  Stratégie :")
            corps.append(para(strat))
    out += ["SOMMAIRE"] + sommaire + corps + ["", "=" * LARGEUR, "Fin de l'encyclopédie.".center(LARGEUR), "=" * LARGEUR]
    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    total = len(tous) + len(pouvoirs)
    print(f"{SORTIE} : {len(tous)} éléments constructibles + {len(pouvoirs)} pouvoirs = {total} entrées")
    if manquants:
        print("SANS TEXTE :", ", ".join(manquants))
    textes_inutiles = set(TEXTES) - {s["key"] for s in tous}
    if textes_inutiles:
        print("Textes sans élément correspondant :", ", ".join(sorted(textes_inutiles)))


if __name__ == "__main__":
    main()
