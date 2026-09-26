"""Convert the Europe WW3 map rules into additive ratc mod files (mods/ratc/ww3/).
Only NEW content is imported; RA / ratc actors, templates, images, weapons and voices keep their definitions.
New actors that inherit a WW3-modified RA/ratc actor or template get a private copy ^WW3Base_<name>."""
import glob, os, re, sys

SRC, MOD = sys.argv[1], sys.argv[2]          # unpacked map dir, repo root
RA = f"{MOD}/engine/mods/ra"
OUT = f"{MOD}/mods/ratc/ww3"

TOP = re.compile(r'^([^\s#][^:]*):(.*)$')

def blocks(path):
    """Ordered list of (name, header_value, body_lines) for top-level MiniYaml nodes (comments dropped)."""
    out, cur = [], None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n").rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = TOP.match(line)
        if m:
            cur = [m.group(1).strip(), m.group(2), []]
            out.append(cur)
        elif cur is not None:
            cur[2].append(line)
    return out

def names(paths):
    s = set()
    for p in paths:
        for n, _, _ in blocks(p):
            s.add(n.lower())
    return s

def children(body):
    """Split a node body into its direct children: list of (key, value, sub_lines)."""
    out = []
    for line in body:
        if re.match(r'^\t[^\t]', line):
            k, _, v = line.strip().partition(":")
            out.append([k.strip(), v, []])
        elif out:
            out[-1][2].append(line)
    return out

def emit(name, value, body):
    return f"{name}:{value}\n" + "".join(l + "\n" for l in body) + "\n"

# ---------------------------------------------------------------- existing content
ra_rules = glob.glob(f"{RA}/rules/*.yaml")
existing_rules = names(ra_rules + [f"{MOD}/mods/ratc/rules.yaml"])
existing_images = names(glob.glob(f"{RA}/sequences/*.yaml") + [f"{MOD}/mods/ratc/sequences.yaml"])
existing_weapons = names(glob.glob(f"{RA}/weapons/*.yaml") + [f"{MOD}/mods/ratc/weapons.yaml"])
existing_voices = names([f"{RA}/audio/voices.yaml"])
existing_speech = set()
for n, v, body in blocks(f"{RA}/audio/notifications.yaml"):
    for k, _, sub in children(body):
        for l in sub:
            existing_speech.add(l.strip().split(":")[0].lower())

RULE_FILES = ["WW3_Defaults.yaml", "WW3_Aircraft.yaml", "WW3_Buildings.yaml", "WW3_Infantry.yaml",
              "WW3_Ships.yaml", "WW3_Vehicles.yaml"]
EXCLUDE = {"harr", "harr.husk", "icbmsub", "icbmsub.nuclear",          # ratc already has Harrier and SNLE
           }

ww_rules = []
for f in RULE_FILES:
    ww_rules += blocks(f"{SRC}/{f}")
ww_rules += [b for b in blocks(f"{SRC}/WW3_Misc.yaml") if b[0] == "MINS"]      # sea mines used by the minelayer

# Merge deltas of every WW3 top-level name (a name can appear in several files)
deltas = {}
for n, v, body in ww_rules:
    deltas.setdefault(n.lower(), (n, []))[1].extend(body)

new_names = [n for n, v, b in ww_rules
             if n.lower() not in existing_rules and n.lower() not in EXCLUDE]
seen = set()
new_blocks = []
for n, v, b in ww_rules:
    if n.lower() in existing_rules or n.lower() in EXCLUDE or n.lower() in seen:
        continue
    seen.add(n.lower())
    new_blocks.append([n, v, list(deltas[n.lower()][1])])

# ---------------------------------------------------------------- renames for colliding images / weapons / voices
img_blocks = blocks(f"{SRC}/sequences.yaml") + blocks(f"{SRC}/unitsequences.yaml")
wpn_blocks = blocks(f"{SRC}/WW3_Weapons.yaml")
voice_blocks = blocks(f"{SRC}/WW3_Voices.yaml")
ratc_images = names([f"{MOD}/mods/ratc/sequences.yaml"])
image_rename = {n.lower(): "ww3" + n.lower() for n, _, _ in img_blocks if n.lower() in ratc_images}   # howi, katy
weapon_rename = {n.lower(): "WW3" + n for n, _, _ in wpn_blocks if n.lower() in existing_weapons}
voice_skip = {n.lower() for n, _, _ in voice_blocks if n.lower() in existing_voices}

def fix_refs(line):
    m = re.match(r'^(\s*)(\S[^:]*):\s*(.*)$', line)
    if not m:
        return line
    ind, key, val = m.groups()
    k = key.split("@")[0]
    if k in ("Image", "RenderSprites") or k.endswith("Image"):
        if val.lower() in image_rename:
            return f"{ind}{key}: {image_rename[val.lower()]}"
    if k in ("Weapon", "EmptyWeapon", "MissileWeapon", "DemolishWeapon") or k.endswith("Weapon"):
        if val.lower() in weapon_rename:
            return f"{ind}{key}: {weapon_rename[val.lower()]}"
    if k == "VoiceSet" and val.lower() in voice_skip:
        return line
    return line

# ---------------------------------------------------------------- ^WW3Base_<X> private copies
base_needed = {}
def base_name(target):
    return "^WW3Base_" + target.lstrip("^").replace(".", "_")

# Inheritance graph of the existing (RA + ratc) rules
parents = {}
for pth in ra_rules + [f"{MOD}/mods/ratc/rules.yaml"]:
    for n, v, body in blocks(pth):
        for l in body:
            m = re.match(r'^\tInherits(?:@\S*)?:\s*(\S+)', l)
            if m:
                parents.setdefault(n.lower(), []).append(m.group(1))

def modified_ancestors(name, acc=None):
    """WW3-modified strict ancestors of an existing actor/template, root first."""
    acc = [] if acc is None else acc
    for p in parents.get(name.lower(), []):
        modified_ancestors(p, acc)
        if p.lower() in deltas and p.lower() not in [a.lower() for a in acc]:
            acc.append(p)
    return acc

# ---- tiny MiniYaml tree: [key, value, children]
def parse_tree(lines, depth=1):
    nodes = []
    prefix = "\t" * depth
    for line in lines:
        if line.startswith(prefix) and not line.startswith(prefix + "\t"):
            k, _, v = line[depth:].partition(":")
            nodes.append([k.strip(), v, []])
        elif nodes:
            nodes[-1][2].append(line)
    for n in nodes:
        n[2] = parse_tree(n[2], depth + 1)
    return nodes

def dump_tree(nodes, depth=1):
    out = []
    for k, v, ch in nodes:
        out.append("\t" * depth + f"{k}:{v}")
        out += dump_tree(ch, depth + 1)
    return out

def merge_tree(acc, add):
    idx = {n[0]: n for n in acc}
    for k, v, ch in add:
        if k.startswith("-") and k[1:] in idx:
            acc.remove(idx.pop(k[1:]))          # removal of something an earlier delta added
            continue
        if k in idx:
            if v.strip():
                idx[k][1] = v
            merge_tree(idx[k][2], ch)
        else:
            node = [k, v, [list(c) for c in ch]]
            acc.append(node)
            idx[k] = node
    return acc

def build(owner, delta_lines, base_of=None):
    """Return body lines for a new actor (base_of=None) or for ^WW3Base_<base_of>."""
    inherits, merged = [], []
    def add_inherit(target):
        if target.lower() not in [t.lower() for t in inherits]:
            inherits.append(target)
    def inline(delta):
        tree = parse_tree(delta)
        rest = []
        for k, v, ch in tree:
            if k.split("@")[0] == "Inherits":
                t = v.strip()
                if t.lower() in existing_rules:
                    continue            # an existing ancestor: already covered
                add_inherit(t)
            else:
                rest.append([k, v, ch])
        merge_tree(merged, rest)
    if base_of:
        add_inherit(base_of)
        for anc in modified_ancestors(base_of):
            inline(deltas[anc.lower()][1])
        inline(delta_lines)
    else:
        tree = parse_tree(delta_lines)
        for k, v, ch in tree:
            if k.split("@")[0] != "Inherits":
                continue
            t = v.strip()
            if t.lower() in existing_rules and t.lower() != owner.lower():
                if t.lower() in deltas:
                    base_needed[t.lower()] = t
                    add_inherit(base_name(t))
                else:
                    add_inherit(t)
                    for anc in modified_ancestors(t):
                        inline(deltas[anc.lower()][1])
            else:
                add_inherit(t)
        merge_tree(merged, [n for n in tree if n[0].split("@")[0] != "Inherits"])
    head = [f"\tInherits{'' if i == 0 else '@WW3I' + str(i)}: {t}" for i, t in enumerate(inherits)]
    return head + [fix_refs(l) for l in dump_tree(merged)]

for blk in new_blocks:
    blk[2] = build(blk[0], blk[2])
    if blk[0] == "RMTRAN":
        # TRAN already inherits ^CargoPips and has no GAPGEN shroud in this ruleset
        blk[2] = [l for l in blk[2] if l.strip() not in ("-RevealsShroud@GAPGEN:", "-Selectable:", "Interactable:")
                  and "^CargoPips" not in l]
    if blk[0].lower() in ("cq", "hop", "hopf") and not any("VoiceSet:" in l for l in blk[2]):
        blk[2] += ["\tVoiced:", "\t\tVoiceSet: WW3GenericVoice"]

base_out = []
done = set()
while True:
    todo = [k for k in base_needed if k not in done]
    if not todo:
        break
    for k in todo:
        done.add(k)
        orig = base_needed[k]
        base_out.append(emit(base_name(orig), "", build(orig, deltas[k][1], base_of=orig)))

# ---------------------------------------------------------------- World / Player / palettes additions
world_add = []
for n, v, body in ww_rules:
    if n in ("^BaseWorld",):
        for k, val, sub in children(body):
            if k.startswith("Locomotor@") and k.upper() != "LOCOMOTOR@NAVAL":
                world_add.append((k, val, sub))
palette_add = []
for n, v, body in ww_rules:
    if n == "^Palettes":
        for k, val, sub in children(body):
            palette_add.append((k, val, sub))
for n, v, body in ww_rules:
    if n == "World":
        for k, val, sub in children(body):
            if k.startswith("PaletteFromFile@") or k.startswith("PlayerColorPalette@") or k.startswith("PaletteFrom"):
                palette_add.append((k, val, sub))
player_add = []
for n, v, body in ww_rules:
    if n == "Player":
        for k, val, sub in children(body):
            if k == "LobbyPrerequisiteCheckbox@NAVY":
                player_add.append(("ProvidesPrerequisite@WW3NAVY", "", ["\t\tPrerequisite: techlevel.naval"]))

ra_pal_keys = set()
for pth in glob.glob(f"{RA}/rules/*.yaml"):
    for n, v, body in blocks(pth):
        if n in ("^Palettes", "World", "^BaseWorld"):
            ra_pal_keys |= {k for k, _, _ in children(body)}
dedup = {}
for k, val, sub in palette_add:
    if k not in ra_pal_keys:
        dedup[k] = (k, val, sub)
palette_add = list(dedup.values())

def child_text(items):
    txt = []
    for k, val, sub in items:
        txt.append(f"\t{k}:{val}")
        txt += sub
    return txt

# ---------------------------------------------------------------- write rules
os.makedirs(OUT, exist_ok=True)
with open(f"{OUT}/rules.yaml", "w", encoding="utf-8") as f:
    f.write("# Généré à partir de la carte « Europe: WW3 Final Edition [BI-4.8] »\n"
            "# (auteurs : Trump, H, Therapist et autres). Contenu ajouté uniquement :\n"
            "# les unités Red Alert / ratc existantes ne sont pas modifiées.\n\n")
    f.write(emit("^BaseWorld", "", child_text(world_add)))
    f.write(emit("^Palettes", "", child_text(palette_add)))
    f.write(emit("Player", "", child_text(player_add)))
    f.write("# ---- Copies privées des modèles modifiés par WW3 (utilisées seulement par les unités WW3)\n\n")
    for b in base_out:
        f.write(b)
    f.write("# ---- Nouvelles unités, bâtiments et modèles WW3\n\n")
    for n, v, body in new_blocks:
        f.write(emit(n, v, body))

# ---------------------------------------------------------------- weapons
with open(f"{OUT}/weapons.yaml", "w", encoding="utf-8") as f:
    for n, v, body in wpn_blocks:
        body = [fix_refs(l) for l in body]
        if n.lower() in weapon_rename:
            body = [re.sub(r'^\tInherits:', '\tInherits@WW3DELTA:', l) for l in body]
            f.write(emit(weapon_rename[n.lower()], "", [f"\tInherits@WW3BASE: {n}"] + body))
        else:
            f.write(emit(n, v, body))

# ---------------------------------------------------------------- sequences
def seq_children(body):
    return children(body)

with open(f"{OUT}/sequences.yaml", "w", encoding="utf-8") as f:
    merged = {}
    order = []
    for n, v, body in img_blocks:
        if n.lower() not in merged:
            order.append(n)
            merged[n.lower()] = []
        merged[n.lower()].extend(body)
    for n in order:
        body = merged[n.lower()]
        low = n.lower()
        if low in image_rename:
            f.write(emit(image_rename[low], "", body))
        elif low in existing_images:
            # Only add sequences that do not exist yet; inline the WW3 Defaults into them.
            ra_seqs = set()
            for p in glob.glob(f"{RA}/sequences/*.yaml") + [f"{MOD}/mods/ratc/sequences.yaml"]:
                for bn, _, bb in blocks(p):
                    if bn.lower() == low:
                        ra_seqs |= {k.lower() for k, _, _ in children(bb)}
            kids = children(body)
            defaults = next((sub for k, _, sub in kids if k == "Defaults"), [])
            dkeys = {l.strip().split(":")[0] for l in defaults if re.match(r'^\t\t[^\t]', l)}
            add = []
            for k, val, sub in kids:
                if k == "Defaults" or k.lower() in ra_seqs:
                    continue
                own = {l.strip().split(":")[0] for l in sub if re.match(r'^\t\t[^\t]', l)}
                extra = [l for l in defaults if re.match(r'^\t\t[^\t]', l) and l.strip().split(":")[0] not in own]
                # keep nested lines of Defaults entries that are multi-line (rare): skip for simplicity
                add.append(f"\t{k}:{val}")
                add += extra + sub
            if add:
                f.write(emit(n, "", add))
        else:
            f.write(emit(n, "", body))

# ---------------------------------------------------------------- voices / notifications
with open(f"{OUT}/voices.yaml", "w", encoding="utf-8") as f:
    for n, v, body in voice_blocks:
        if n.lower() in voice_skip:
            # WW3's version of an existing voice set, only for WW3 units that need its extra voices
            f.write(emit("WW3" + n, "", [f"\tInherits: {n}"] + body))
            continue
        f.write(emit(n, v, body))
    # Give every Red Alert voice set with per-faction variants an entry for the new factions (additive)
    for n, v, body in blocks(f"{RA}/audio/voices.yaml"):
        tree = [c for c in children(body) if c[0] == "Variants"]
        if not tree:
            continue
        var = {l.strip().split(":")[0]: l.strip().split(":", 1)[1] for l in tree[0][2]}
        add = []
        for fac, like in (("usa", "allies"), ("spain", "allies"), ("china", "soviet"), ("turkey", "soviet"), ("greece", "soviet")):
            if fac not in var and like in var:
                add.append(f"\t\t{fac}:{var[like]}")
        if add:
            f.write(emit(n, "", ["\tVariants:"] + add))

with open(f"{OUT}/notifications.yaml", "w", encoding="utf-8") as f:
    for n, v, body in blocks(f"{SRC}/notifications.yaml"):
        kids = children(body)
        out = []
        for k, val, sub in kids:
            keep = [l for l in sub if l.strip().split(":")[0].lower() not in existing_speech]
            if keep:
                out.append(f"\t{k}:{val}")
                out += keep
        if out:
            f.write(emit(n, v, out))

print("new rule blocks:", len(new_blocks), " private bases:", len(base_out),
      " renamed images:", image_rename, " renamed weapons:", weapon_rename, " skipped voices:", voice_skip)

# ---------------------------------------------------------------- post-fix: interior bibs do not exist in RA content
p = f"{OUT}/sequences.yaml"
txt = open(p, encoding="utf-8").read()
txt = re.sub(r'(\t+)TilesetFilenames:\n((?:\1\t.*\n)*?)\1\tINTERIOR: (bib\d)\.int\n',
             lambda m: f"{m.group(1)}Filename: {m.group(3)}.tem\n{m.group(1)}TilesetFilenames:\n{m.group(2)}", txt)
open(p, "w", encoding="utf-8").write(txt)
