"""Generate mods/ratc/ww3/factions.yaml: the selectable factions added to Red Alert (5 from the WW3 map,
plus Japan and India from ratc) and their production prerequisites."""
import re, sys
MOD = sys.argv[1]
RA = f"{MOD}/engine/mods/ra/rules"

NEW = {  # internal name: (display name, side, template faction, description)
    "usa": ("USA", "Allies", "france",
            "USA : puissance aérienne\\nUnités spéciales : A-10, F-22, Apache, Humvee"),
    "spain": ("Espagne", "Allies", "france",
              "Espagne : prismes et antigravité\\nUnités spéciales : char prisme, canon à prisme"),
    "china": ("Chine", "Soviet", "russia",
              "Chine : maîtres des blindés\\nUnités spéciales : chars lourds, tour de propagande"),
    "turkey": ("Turquie", "Soviet", "russia",
               "Turquie : subversion et armes chimiques\\nUnités spéciales : lance-Scud, Katioucha"),
    "greece": ("Grèce", "Soviet", "russia",
               "Grèce : infanterie en armure avancée\\nUnités spéciales : hoplites, Titan"),
    # Factions propres au mod ratc (pas issues de la carte WW3)
    "japan": ("Japon", "Allies", "france",
              "Japon : précision, technologie et mobilité\\nUnités spéciales : Type 10, Type 16, Type 19, SeaGuardian"),
    "india": ("Inde", "Soviet", "russia",
              "Inde : polyvalence, volume et saturation\\nUnités spéciales : Arjun, Nag, Dhanush, TAPAS"),
}
ALLIED = [k for k, v in NEW.items() if v[1] == "Allies"]
SOVIET = [k for k, v in NEW.items() if v[1] == "Soviet"]

def ra_blocks(path):
    """{actor: {trait: [lines]}} for traits that have a Factions: field."""
    res, actor, trait = {}, None, None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        m = re.match(r'^([^\s#][^:]*):', line)
        if m:
            actor, trait = m.group(1), None
            continue
        m = re.match(r'^\t([^\t:]+):', line)
        if m:
            trait = m.group(1)
            res.setdefault(actor, {})[trait] = []
            continue
        if actor and trait and line.startswith("\t\t"):
            res[actor][trait].append(line)
    return {a: {t: b for t, b in ts.items() if any(l.strip().startswith("Factions:") for l in b)}
            for a, ts in res.items()}

out = ["# Nouvelles factions : USA, Espagne, Chine, Turquie, Grèce (carte WW3), Japon et Inde (ratc).",
       "# Généré par tools/ww3-import/ww3factions.py.", ""]

# Lobby factions
out.append("^BaseWorld:")
for i, (k, (name, side, _, desc)) in enumerate(NEW.items()):
    out += [f"\tFaction@{k}:", f"\t\tName: {name}", f"\t\tInternalName: {k}", f"\t\tSide: {side}",
            f"\t\tDescription: {desc}"]
out += ["\tFaction@randomallies:", "\t\tRandomFactionMembers: " + ", ".join(["england", "france", "germany"] + ALLIED),
        "\tFaction@randomsoviet:", "\t\tRandomFactionMembers: " + ", ".join(["russia", "ukraine"] + SOVIET), ""]

def extend(factions):
    fs = [f.strip() for f in factions.split(",")]
    add = []
    if "allies" in fs and len(fs) > 1:
        add += ALLIED
    if "soviet" in fs and len(fs) > 1:
        add += SOVIET
    return ", ".join(fs + [a for a in add if a not in fs])

for path in (f"{RA}/world.yaml", f"{RA}/structures.yaml"):
    for actor, traits in ra_blocks(path).items():
        lines = []
        for trait, body in traits.items():
            fac = next(l for l in body if l.strip().startswith("Factions:")).split(":", 1)[1]
            fs = [f.strip() for f in fac.split(",")]
            if len(fs) > 1:                         # umbrella list: add the new factions of the same side
                new = extend(fac)
                if new != ", ".join(fs):
                    lines += [f"\t{trait}:", f"\t\tFactions: {new}"]
            elif fs[0] in ("france", "russia") and trait.endswith("@" + fs[0]):
                src = fs[0]
                for k, (_, side, tmpl, _) in NEW.items():
                    if tmpl != src:
                        continue
                    lines.append(f"\t{trait.rsplit('@', 1)[0]}@{k}:")
                    lines += [re.sub(r'\b' + src + r'\b', k, l) for l in body]
        if lines:
            out += [f"{actor}:"] + lines + [""]

open(f"{MOD}/mods/ratc/ww3/factions.yaml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out[:60]))

# Voice variants: every voice set with per-faction variants needs an entry for each new faction
# (same variant as its side), otherwise the new faction's units stay silent.
variants, order = {}, []
for path in (f"{MOD}/engine/mods/ra/audio/voices.yaml", f"{MOD}/mods/ratc/ww3/voices.yaml"):
    voice, in_var = None, False
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        m = re.match(r'^([^\s#][^:]*):', line)
        if m:
            voice, in_var = m.group(1), False
            continue
        if re.match(r'^\tVariants:', line):
            in_var = True
            if voice not in variants:
                variants[voice] = {}
                order.append(voice)
            continue
        if re.match(r'^\t[^\t]', line):
            in_var = False
        elif in_var and line.startswith("\t\t"):
            k, _, v = line.strip().partition(":")
            variants[voice][k.strip()] = v.strip()

vout = ["# Variantes de voix des nouvelles factions (généré par tools/ww3-import/ww3factions.py).", ""]
for voice in order:
    var = variants[voice]
    add = [f"\t\t{k}: {var[side.lower()]}" for k, (_, side, _, _) in NEW.items()
           if k not in var and side.lower() in var]
    if add:
        vout += [f"{voice}:", "\tVariants:"] + add + [""]
open(f"{MOD}/mods/ratc/ww3/faction-voices.yaml", "w", encoding="utf-8").write("\n".join(vout) + "\n")
