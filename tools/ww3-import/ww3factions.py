"""Generate mods/ratc/ww3/factions.yaml: 5 new selectable factions and their production prerequisites."""
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

out = ["# Nouvelles factions issues de la carte WW3 (USA, Espagne, Chine, Turquie, Grèce).", ""]

# Lobby factions
out.append("^BaseWorld:")
for i, (k, (name, side, _, desc)) in enumerate(NEW.items()):
    out += [f"\tFaction@{k}:", f"\t\tName: {name}", f"\t\tInternalName: {k}", f"\t\tSide: {side}",
            f"\t\tDescription: {desc}"]
out += ["\tFaction@randomallies:", "\t\tRandomFactionMembers: england, france, germany, usa, spain",
        "\tFaction@randomsoviet:", "\t\tRandomFactionMembers: russia, ukraine, china, turkey, greece", ""]

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
