"""Mini-moteur de rendu 3D -> sprites OpenRA (palette RA, 32 orientations).

Les modèles sont décrits en pixels (24 px = 1 case), axe x vers l'avant,
y vers la gauche, z vers le haut. Chaque solide est un prisme : un polygone
bas et un polygone haut ayant le même nombre de sommets.
"""
import math
from PIL import Image, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo

SS = 4                      # suréchantillonnage
TILT = math.radians(40)     # inclinaison de la caméra (0 = vue de dessus)
LIGHT = (-0.45, 0.55, 0.70) # lumière venant du haut-gauche
SHADOW_INDEX = 4

_n = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _n for c in LIGHT)

# Rampes de la palette temperat.pal (du plus clair au plus foncé).
RAMPS = {
    "paint": list(range(80, 96)),       # couleur du joueur
    "metal": list(range(131, 144)),
    "dark": list(range(138, 144)),
    "rubber": [140, 141, 142, 143, 143],
    "glass": [133, 135, 137, 139],
    "burnt": list(range(137, 144)) + [143, 143],
    # Bâtiments
    "concrete": [104, 105, 106, 107, 108, 109, 110, 111, 120, 121],
    "white": list(range(128, 139)),
    "olive": list(range(145, 156)),
    "red": list(range(230, 240)),
    "yellow": [156, 157, 158, 159, 214, 215, 216],
    "earth": [59, 57, 51, 42, 32, 120, 121, 122],
}
MATERIALS = list(RAMPS)


def load_palette(path):
    p = open(path, "rb").read()
    return [min(255, v * 4) for v in p]


class Model:
    def __init__(self):
        self.solids = []    # (bas, haut, matériau, décalage de teinte)

    def prism(self, bottom, top, mat="paint", tint=0.0):
        self.solids.append((bottom, top, mat, tint))
        return self

    def extrude(self, poly, z0, z1, mat="paint", tint=0.0):
        return self.prism([(x, y, z0) for x, y in poly], [(x, y, z1) for x, y in poly], mat, tint)

    def box(self, x0, x1, y0, y1, z0, z1, mat="paint", tint=0.0):
        return self.extrude([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1, mat, tint)

    def tapered_box(self, x0, x1, y0, y1, z0, z1, inset_front=0, inset_back=0, inset_side=0,
                    mat="paint", tint=0.0):
        bottom = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)]
        top = [(x0 + inset_back, y0 + inset_side, z1), (x1 - inset_front, y0 + inset_side, z1),
               (x1 - inset_front, y1 - inset_side, z1), (x0 + inset_back, y1 - inset_side, z1)]
        return self.prism(bottom, top, mat, tint)

    def cylinder_x(self, x0, x1, y, z, r, mat="metal", sides=8, tint=0.0):
        """Tube le long de l'axe x (canon)."""
        ring = [(y + r * math.cos(2 * math.pi * i / sides), z + r * math.sin(2 * math.pi * i / sides))
                for i in range(sides)]
        # Un tube est un prisme orienté selon x : on le décompose en facettes.
        for i in range(sides):
            (ya, za), (yb, zb) = ring[i], ring[(i + 1) % sides]
            self.solids.append(("quad", [(x0, ya, za), (x1, ya, za), (x1, yb, zb), (x0, yb, zb)], mat, tint))
        return self

    def cylinder_y(self, x, y0, y1, z, r, mat="rubber", sides=10, tint=0.0):
        """Roue : cylindre d'axe y."""
        ring = [(x + r * math.cos(2 * math.pi * i / sides), z + r * math.sin(2 * math.pi * i / sides))
                for i in range(sides)]
        self.solids.append(("poly", [(px, y0, pz) for px, pz in ring], mat, tint))
        self.solids.append(("poly", [(px, y1, pz) for px, pz in ring[::-1]], mat, tint))
        for i in range(sides):
            (xa, za), (xb, zb) = ring[i], ring[(i + 1) % sides]
            self.solids.append(("quad", [(xa, y0, za), (xb, y0, zb), (xb, y1, zb), (xa, y1, za)], mat, tint))
        return self

    def loft_x(self, sections, mat="paint", sides=12, tint=0.0, cap=True):
        """Fuselage profilé : sections (x, demi-largeur, demi-hauteur, z du centre), x croissant."""
        rings = []
        for x, ry, rz, zc in sections:
            rings.append([(x, ry * math.cos(2 * math.pi * i / sides), zc + rz * math.sin(2 * math.pi * i / sides))
                          for i in range(sides)])
        for a, b in zip(rings, rings[1:]):
            for i in range(sides):
                j = (i + 1) % sides
                self.solids.append(("poly", [a[i], a[j], b[j], b[i]], mat, tint))
        if cap:     # sections données de l'arrière vers l'avant (x croissant)
            self.solids.append(("poly", rings[0][::-1], mat, tint))
            self.solids.append(("poly", rings[-1], mat, tint))
        return self

    def plate(self, pts, thickness=0.5, mat="paint", tint=0.0):
        """Surface fine quelconque (aile, dérive, pale) : polygone 3D épaissi selon sa normale."""
        n = _normal(pts)
        h = thickness / 2
        bottom = [(x - n[0] * h, y - n[1] * h, z - n[2] * h) for x, y, z in pts]
        top = [(x + n[0] * h, y + n[1] * h, z + n[2] * h) for x, y, z in pts]
        return self.prism(bottom, top, mat, tint)

    def cylinder_z(self, x, y, z0, z1, r, mat="metal", sides=8, tint=0.0):
        """Cylindre vertical (coupole, fût, pot)."""
        ring = [(x + r * math.cos(2 * math.pi * i / sides), y + r * math.sin(2 * math.pi * i / sides))
                for i in range(sides)]
        return self.extrude(ring, z0, z1, mat, tint)

    def tube(self, p0, p1, r, mat="metal", sides=6, tint=0.0):
        """Tube quelconque de p0 à p1 (antenne, câble, lance-pots incliné)."""
        d = _sub(p1, p0)
        ln = math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2) or 1
        d = (d[0] / ln, d[1] / ln, d[2] / ln)
        a = (0, 0, 1) if abs(d[2]) < 0.9 else (1, 0, 0)
        u = _cross(d, a)
        un = math.sqrt(sum(c * c for c in u))
        u = (u[0] / un, u[1] / un, u[2] / un)
        v = _cross(d, u)
        ring = [(u[0] * math.cos(t) + v[0] * math.sin(t), u[1] * math.cos(t) + v[1] * math.sin(t),
                 u[2] * math.cos(t) + v[2] * math.sin(t)) for t in (2 * math.pi * i / sides for i in range(sides))]
        for i in range(sides):
            a, b = ring[i], ring[(i + 1) % sides]
            self.solids.append(("quad", [tuple(p0[j] + r * a[j] for j in range(3)), tuple(p1[j] + r * a[j] for j in range(3)),
                                         tuple(p1[j] + r * b[j] for j in range(3)), tuple(p0[j] + r * b[j] for j in range(3))],
                                mat, tint))
        return self

    def transformed(self, fn):
        """Copie du modèle dont chaque sommet passe par fn (x, y, z) -> (x, y, z)."""
        m = Model()
        m.__dict__.update({k: v for k, v in vars(self).items() if k != "solids"})
        for s in self.solids:
            if s[0] in ("quad", "poly"):
                m.solids.append((s[0], [fn(*p) for p in s[1]], s[2], s[3]))
            else:
                b, t, mat, tint = s
                m.solids.append(([fn(*p) for p in b], [fn(*p) for p in t], mat, tint))
        return m

    def faces(self):
        for s in self.solids:
            if s[0] in ("quad", "poly"):
                yield s[1], s[2], s[3], s[0] == "quad"
                continue
            bottom, top, mat, tint = s
            n = len(bottom)
            yield top, mat, tint, False
            yield bottom[::-1], mat, tint, False
            for i in range(n):
                j = (i + 1) % n
                yield [bottom[i], bottom[j], top[j], top[i]], mat, tint, False


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _normal(pts):
    # Méthode de Newell : robuste pour les polygones plans.
    nx = ny = nz = 0.0
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        nx += (a[1] - b[1]) * (a[2] + b[2])
        ny += (a[2] - b[2]) * (a[0] + b[0])
        nz += (a[0] - b[0]) * (a[1] + b[1])
    ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
    return (nx / ln, ny / ln, nz / ln)


def render_frame(model, facing, size, scale=1.0, shadow=True, ground=0.0, remap=None):
    """Rend une orientation. facing en fractions de tour, sens antihoraire depuis le nord."""
    if getattr(model, "hd", False):
        import hd
        return hd.render_frame(model, facing, size, scale, shadow, ground, remap)
    th = 2 * math.pi * facing
    fwd = (-math.sin(th), math.cos(th))
    left = (-math.cos(th), -math.sin(th))
    ca, sa = math.cos(TILT), math.sin(TILT)
    W = size[0] * SS
    H = size[1] * SS
    cx, cy = W / 2, H / 2
    k = scale * SS

    def world(p):
        x, y, z = p
        return (x * fwd[0] + y * left[0], x * fwd[1] + y * left[1], z)

    def screen(w):
        X, Y, Z = w
        return (cx + X * k, cy - (Y * ca + Z * sa) * k)

    mat_img = Image.new("L", (W, H), 0)
    shd_img = Image.new("L", (W, H), 0)
    dm = ImageDraw.Draw(mat_img)
    ds = ImageDraw.Draw(shd_img)
    view = (0, -sa, ca)     # du décor vers la caméra

    polys = []
    shadow_polys = []
    for pts, mat, tint, two_sided in model.faces():
        wp = [world(p) for p in pts]
        n = _normal(wp)
        facing_cam = n[0] * view[0] + n[1] * view[1] + n[2] * view[2]
        if facing_cam <= 1e-4:
            if not two_sided:
                if shadow and n[2] < -0.5:
                    shadow_polys.append(wp)
                continue
            n = (-n[0], -n[1], -n[2])
        light = max(0.0, n[0] * LIGHT[0] + n[1] * LIGHT[1] + n[2] * LIGHT[2])
        shade = min(1.0, max(0.0, 0.18 + 0.95 * light - tint))
        if remap:
            mat = remap.get(mat, mat)
        depth = sum(w[1] * sa - w[2] * ca for w in wp) / len(wp)
        polys.append((depth, [screen(w) for w in wp], MATERIALS.index(mat) + 1, shade))

    if shadow:
        # Ombre portée : projection des faces du dessous sur le sol, décalée.
        for wp in shadow_polys:
            pts = [screen((w[0] + 2.5, w[1] - 2.5 * 0.8, ground)) for w in wp]
            ds.polygon(pts, fill=255)
    shadow_mask = shd_img.copy()
    shd_img = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(shd_img)

    polys.sort(key=lambda p: -p[0])
    for _, pts, m, shade in polys:
        dm.polygon(pts, fill=m)
        ds.polygon(pts, fill=int(shade * 255))

    # Réduction : matériau majoritaire par bloc SSxSS.
    out = Image.new("P", size, 0)
    mp, sp, hp = mat_img.load(), shd_img.load(), shadow_mask.load()
    op = out.load()
    for oy in range(size[1]):
        for ox in range(size[0]):
            counts = {}
            shades = {}
            shadow_cov = 0
            for dy in range(SS):
                for dx in range(SS):
                    px, py = ox * SS + dx, oy * SS + dy
                    m = mp[px, py]
                    if m:
                        counts[m] = counts.get(m, 0) + 1
                        shades[m] = shades.get(m, 0) + sp[px, py]
                    elif hp[px, py]:
                        shadow_cov += 1
            cov = sum(counts.values())
            if cov * 2 >= SS * SS:
                m = max(counts, key=counts.get)
                shade = shades[m] / counts[m] / 255
                ramp = RAMPS[MATERIALS[m - 1]]
                op[ox, oy] = ramp[min(len(ramp) - 1, int((1 - shade) * len(ramp)))]
            elif shadow_cov * 2 >= SS * SS:
                op[ox, oy] = SHADOW_INDEX
    return out


def outline(frame):
    """Contour sombre d'un pixel autour de la silhouette, comme les sprites RA."""
    w, h = frame.size
    src = frame.load()
    out = frame.copy()
    op = out.load()
    for y in range(h):
        for x in range(w):
            if src[x, y] in (0, SHADOW_INDEX):
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and src[nx, ny] in (0, SHADOW_INDEX):
                    break
            else:
                continue
            idx = src[x, y]
            if 80 <= idx <= 95:
                op[x, y] = min(95, idx + 5)
            elif 128 <= idx <= 143:
                op[x, y] = min(143, idx + 3)
    return out


def save_sheet(frames, path, palette):
    w, h = frames[0].size
    sheet = Image.new("P", (w * len(frames), h), 0)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * w, 0))
    sheet.putpalette(palette)
    info = PngInfo()
    info.add_text("FrameSize", f"{w},{h}")
    info.add_text("FrameAmount", str(len(frames)))
    sheet.save(path, pnginfo=info, transparency=0)


def render_rotations(model, size, facings=32, scale=1.0, shadow=True, remap=None):
    if getattr(model, "hd", False):
        import hd
        return hd.render_rotations(model, size, facings, scale, shadow, remap)
    return [outline(render_frame(model, i / facings, size, scale, shadow, remap=remap)) for i in range(facings)]


# --- Icônes de production (64x48, palette chrome = temperat sans remplacement) ---
ICON_COLORS = {
    "paint": (92, 104, 60),
    "metal": (120, 120, 116),
    "dark": (60, 60, 60),
    "rubber": (36, 36, 36),
    "glass": (150, 190, 200),
    "burnt": (40, 36, 34),
    "concrete": (176, 162, 132),
    "white": (214, 214, 214),
    "olive": (92, 112, 70),
    "red": (220, 24, 24),
    "yellow": (240, 190, 24),
    "earth": (124, 104, 76),
}


def hd_style(m, camo=None, dust=0.0, dust_height=2.4, track_period=2.0, ground_ao=True):
    """Active le rendu détaillé (hd.py) : ombres portées, camouflage, poussière, textures, liserés.
    camo : {"scale": taille des taches, "seed": graine, "tones": [(seuil, assombrissement), ...]}."""
    m.hd = True
    m.camo = camo
    m.dust = dust
    m.dust_height = dust_height
    m.track_period = track_period
    m.ground_ao = ground_ao            # assombrissement près du sol (False pour les aéronefs)
    return m


def render_icon(model, palette, scale=1.25, facing=0.84, paint=(92, 104, 60), bg=((52, 60, 44), (20, 24, 20))):
    if getattr(model, "hd", False):
        import hd
        return hd.render_icon(model, palette, scale, facing, paint, bg)
    size = (64, 48)
    colors = dict(ICON_COLORS, paint=paint)
    # On réutilise le rendu indexé pour obtenir matériau + ombrage par pixel.
    th = 2 * math.pi * facing
    fwd = (-math.sin(th), math.cos(th))
    left = (-math.cos(th), -math.sin(th))
    ca, sa = math.cos(TILT), math.sin(TILT)
    W, H = size[0] * SS, size[1] * SS
    cx, cy = W / 2 - 1 * SS, H / 2 + 3 * SS
    k = scale * SS
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(bg[0][i] * (1 - t) + bg[1][i] * t) for i in range(3)))
    view = (0, -sa, ca)
    polys = []
    for pts, mat, tint, two_sided in model.faces():
        wp = [(p[0] * fwd[0] + p[1] * left[0], p[0] * fwd[1] + p[1] * left[1], p[2]) for p in pts]
        n = _normal(wp)
        if n[0] * view[0] + n[1] * view[1] + n[2] * view[2] <= 1e-4:
            if not two_sided:
                continue
            n = (-n[0], -n[1], -n[2])
        light = max(0.0, n[0] * LIGHT[0] + n[1] * LIGHT[1] + n[2] * LIGHT[2])
        shade = min(1.2, max(0.15, 0.35 + 0.8 * light - tint))
        depth = sum(w[1] * sa - w[2] * ca for w in wp) / len(wp)
        c = colors[mat]
        polys.append((depth, [(cx + w[0] * k, cy - (w[1] * ca + w[2] * sa) * k) for w in wp],
                      tuple(min(255, int(ch * shade)) for ch in c)))
    polys.sort(key=lambda p: -p[0])
    for _, pts, col in polys:
        d.polygon(pts, fill=col)
    return quantize_icon(img.resize(size, Image.LANCZOS), palette)


def quantize_icon(img, palette):
    """Image RVB -> palette RA, sans les indices spéciaux ni la couleur du joueur."""
    size = img.size
    pal_img = Image.new("P", (1, 1))
    # On exclut les indices spéciaux (transparence, ombre) et la rampe de couleur joueur.
    usable = [i for i in range(256) if i not in (0, 3, 4) and not 80 <= i <= 95]
    pal = [0] * 768
    for i in range(256):
        src = usable[i % len(usable)]
        pal[3 * i:3 * i + 3] = palette[3 * src:3 * src + 3]
    pal_img.putpalette(pal)
    q = img.quantize(palette=pal_img, dither=Image.Dither.NONE)
    qp = q.load()
    out = Image.new("P", size)
    o = out.load()
    for y in range(size[1]):
        for x in range(size[0]):
            o[x, y] = usable[qp[x, y] % len(usable)]
    return out


def label(icon, text, fg=15, bg=142):
    """Bandeau de nom en bas de l'icône (remplace le texte anglais des icônes RA)."""
    icon = icon.copy()
    d = ImageDraw.Draw(icon)
    w, h = icon.size
    d.rectangle([0, h - 10, w - 1, h - 1], fill=bg)
    font = ImageFont.load_default()
    tw = d.textlength(text, font=font)
    d.text(((w - tw) / 2, h - 11), text, fill=fg, font=font)
    return icon
