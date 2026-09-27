"""Rendu détaillé des véhicules (activé par render.hd_style sur un modèle).

Par rapport au rendu de base (render.render_frame), chaque sous-pixel connaît sa
position sur le modèle, ce qui permet :
- les ombres portées du modèle sur lui-même (canon sur la caisse, coffres...) ;
- une ombre au sol projetée depuis la lumière ;
- un camouflage en taches (nuances de la couleur du joueur) ;
- la poussière et la boue sur le bas du véhicule ;
- des textures : maillons de chenille, grilles moteur ;
- des reflets sur les vitres et le métal ;
- des liserés de relief : arête claire côté lumière, trait d'ombre sous les surplombs.
"""
import math
from PIL import Image, ImageDraw
import render as R

SS = R.SS
SHADOW_LENGTH = 0.45        # longueur de l'ombre au sol (1 = projection exacte depuis la lumière)
SHADOW_EPS = 0.35           # tolérance de l'ombre portée (évite l'auto-ombrage des faces voisines)
EDGE_DEPTH = 1.2            # écart de profondeur (px) qui marque un surplomb
SPECULAR = {"glass": (20, 1.0), "metal": (12, 0.45), "white": (8, 0.25), "paint": (6, 0.10), "dark": (10, 0.12)}
TEXTURED = ("paint", "rubber", "metal", "dark")
_f = (0.4, -0.8, 0.45)                      # lumière d'appoint côté caméra (débouche les flancs)
FILL = tuple(c / math.sqrt(sum(v * v for v in _f)) for c in _f)
FILL_STRENGTH = 0.24


# ---------------------------------------------------------------- bruit de valeur 3D
def _hash(ix, iy, iz, seed):
    h = (ix * 374761393 + iy * 668265263 + iz * 1440662683 + seed * 2654435761) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def _smooth(t):
    return t * t * (3 - 2 * t)


def noise(x, y, z, seed=0):
    ix, iy, iz = math.floor(x), math.floor(y), math.floor(z)
    fx, fy, fz = _smooth(x - ix), _smooth(y - iy), _smooth(z - iz)
    v = 0.0
    for dz in (0, 1):
        wz = fz if dz else 1 - fz
        for dy in (0, 1):
            wy = fy if dy else 1 - fy
            for dx in (0, 1):
                wx = fx if dx else 1 - fx
                v += wx * wy * wz * _hash(ix + dx, iy + dy, iz + dz, seed)
    return v


def fbm(x, y, z, seed=0):
    return 0.65 * noise(x, y, z, seed) + 0.35 * noise(2.1 * x, 2.1 * y, 2.1 * z, seed + 17)


# ---------------------------------------------------------------- géométrie
def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _affine(spts, attrs):
    """Coefficients (c0, a, b) tels que attribut = c0 + a*sx + b*sy sur le plan de la face."""
    best, bi, bj = 0.0, 1, 2
    ax, ay = spts[0]
    for i in range(1, len(spts)):
        for j in range(i + 1, len(spts)):
            d = (spts[i][0] - ax) * (spts[j][1] - ay) - (spts[j][0] - ax) * (spts[i][1] - ay)
            if abs(d) > abs(best):
                best, bi, bj = d, i, j
    out = []
    if abs(best) < 1e-6:
        return [(attrs[0][n], 0.0, 0.0) for n in range(len(attrs[0]))]
    e1x, e1y = spts[bi][0] - ax, spts[bi][1] - ay
    e2x, e2y = spts[bj][0] - ax, spts[bj][1] - ay
    for n in range(len(attrs[0])):
        qa = attrs[0][n]
        d1, d2 = attrs[bi][n] - qa, attrs[bj][n] - qa
        a = (d1 * e2y - d2 * e1y) / best
        b = (d2 * e1x - d1 * e2x) / best
        out.append((qa - a * ax - b * ay, a, b))
    return out


class _Face:
    __slots__ = ("mat", "tint", "n", "nm", "diffuse", "fill", "spec", "coef", "lcoef", "depth")


def _prepare(model, facing, W, H, cx, cy, k):
    th = 2 * math.pi * facing
    fwd = (-math.sin(th), math.cos(th))
    left = (-math.cos(th), -math.sin(th))
    ca, sa = math.cos(R.TILT), math.sin(R.TILT)
    view = (0.0, -sa, ca)
    L = R.LIGHT

    def world(p):
        x, y, z = p
        return (x * fwd[0] + y * left[0], x * fwd[1] + y * left[1], z)

    def screen(w):
        return (cx + w[0] * k, cy - (w[1] * ca + w[2] * sa) * k)

    # Repère de la lumière (pour la carte d'ombres).
    e1 = (L[1], -L[0], 0.0)
    ln = math.sqrt(e1[0] ** 2 + e1[1] ** 2)
    e1 = (e1[0] / ln, e1[1] / ln, 0.0)
    e2 = (L[1] * e1[2] - L[2] * e1[1], L[2] * e1[0] - L[0] * e1[2], L[0] * e1[1] - L[1] * e1[0])

    faces, cam, lit, ground = [], [], [], []
    for pts, mat, tint, two_sided in model.faces():
        wp = [world(p) for p in pts]
        n = R._normal(wp)
        nm = R._normal(pts)
        fc = _dot(n, view)
        f = _Face()
        f.mat, f.tint = mat, tint
        if fc <= 1e-4 and two_sided:
            n = (-n[0], -n[1], -n[2])
            nm = (-nm[0], -nm[1], -nm[2])
        f.n, f.nm = n, nm
        nl = _dot(n, L)
        f.diffuse = max(0.0, nl)
        f.fill = FILL_STRENGTH * max(0.0, _dot(n, FILL))
        p_exp, strength = SPECULAR.get(mat, (0, 0))
        if strength and nl > 0:
            r = (2 * nl * n[0] - L[0], 2 * nl * n[1] - L[1], 2 * nl * n[2] - L[2])
            f.spec = strength * max(0.0, _dot(r, view)) ** p_exp
        else:
            f.spec = 0.0
        idx = len(faces)
        faces.append(f)
        # vers la caméra
        if fc > 1e-4 or two_sided:
            sp = [screen(w) for w in wp]
            f.coef = _affine(sp, [p + w for p, w in zip(pts, wp)])
            f.depth = sum(w[1] * sa - w[2] * ca for w in wp) / len(wp)
            cam.append((f.depth, sp, idx + 1))
        # vers la lumière (ombres)
        if nl > 0.02 or two_sided:
            lp = [(_dot(w, e1), _dot(w, e2), _dot(w, L)) for w in wp]
            lit.append((sum(p[2] for p in lp) / len(lp), lp, idx + 1))
            if nl > 0.02:
                ground.append([screen((w[0] - L[0] * w[2] / L[2] * SHADOW_LENGTH,
                                       w[1] - L[1] * w[2] / L[2] * SHADOW_LENGTH, 0.0)) for w in wp])
    return faces, cam, lit, ground, (e1, e2, L), view


def raster(model, facing, W, H, cx, cy, k, cast_shadow=True):
    """Tampons par sous-pixel : identifiant de face, matériau, luminosité, profondeur ; masque d'ombre au sol."""
    faces, cam, lit, ground, (e1, e2, L), view = _prepare(model, facing, W, H, cx, cy, k)
    ca, sa = math.cos(R.TILT), math.sin(R.TILT)

    # Tampon d'identifiants vu de la caméra (peintre : du plus loin au plus proche).
    idimg = Image.new("I", (W, H), 0)
    d = ImageDraw.Draw(idimg)
    for _, sp, fid in sorted(cam, key=lambda c: -c[0]):
        d.polygon(sp, fill=fid)
    ids = list(idimg.getdata())

    # Carte d'ombres vue de la lumière (du plus loin au plus proche de la lumière).
    if lit:
        xs = [p[0] for _, lp, _ in lit for p in lp]
        ys = [p[1] for _, lp, _ in lit for p in lp]
        ox, oy = min(xs) - 2, min(ys) - 2
        LW = int((max(xs) - ox + 2) * k) + 2
        LH = int((max(ys) - oy + 2) * k) + 2
        limg = Image.new("I", (LW, LH), 0)
        ld = ImageDraw.Draw(limg)
        for _, lp, fid in sorted(lit, key=lambda c: c[0]):
            sp = [((p[0] - ox) * k, (p[1] - oy) * k) for p in lp]
            ld.polygon(sp, fill=fid)
            faces[fid - 1].lcoef = _affine(sp, [(p[2],) for p in lp])[0]
        lids = list(limg.getdata())
    else:
        lids, LW, LH, ox, oy = [], 0, 0, 0, 0

    shadow_mask = None
    if cast_shadow:
        simg = Image.new("L", (W, H), 0)
        sd = ImageDraw.Draw(simg)
        for sp in ground:
            sd.polygon(sp, fill=255)
        shadow_mask = list(simg.getdata())

    camo = getattr(model, "camo", None)
    dust = getattr(model, "dust", 0.0)
    dust_h = getattr(model, "dust_height", 2.4)
    track_period = getattr(model, "track_period", 2.0)
    cache = {}

    n = W * H
    mats = [None] * n
    shades = [0.0] * n
    depths = [0.0] * n
    for i in range(n):
        fid = ids[i]
        if not fid:
            continue
        f = faces[fid - 1]
        sx, sy = (i % W) + 0.5, (i // W) + 0.5
        c = f.coef
        mx = c[0][0] + c[0][1] * sx + c[0][2] * sy
        my = c[1][0] + c[1][1] * sx + c[1][2] * sy
        mz = c[2][0] + c[2][1] * sx + c[2][2] * sy
        wx = c[3][0] + c[3][1] * sx + c[3][2] * sy
        wy = c[4][0] + c[4][1] * sx + c[4][2] * sy
        wz = c[5][0] + c[5][1] * sx + c[5][2] * sy
        depths[i] = wy * sa - wz * ca

        # Ombre portée par le modèle sur lui-même.
        diffuse = f.diffuse
        spec = f.spec
        if diffuse > 0 and lids:
            lx = int(((wx * e1[0] + wy * e1[1]) - ox) * k)
            ly = int(((wx * e2[0] + wy * e2[1] + wz * e2[2]) - oy) * k)
            if 0 <= lx < LW and 0 <= ly < LH:
                g = lids[ly * LW + lx]
                if g and g != fid:
                    gc = faces[g - 1].lcoef
                    if gc[0] + gc[1] * lx + gc[2] * ly > wx * L[0] + wy * L[1] + wz * L[2] + SHADOW_EPS:
                        diffuse *= 0.2
                        spec = 0.0

        mat = f.mat
        dt = 0.0
        if mat in TEXTURED:
            key = (int(mx * 3), int(my * 3), int(mz * 3))
            hit = cache.get(key)
            if hit is None:
                hit = (fbm(mx / camo["scale"], my / camo["scale"], mz / camo["scale"], camo["seed"]) if camo else 0.0,
                       noise(mx * 0.8, my * 0.8, mz * 0.8, 91))
                cache[key] = hit
            camo_n, grain = hit
            if mat == "paint" and camo:
                for thr, tone in camo["tones"]:
                    if camo_n < thr:
                        dt += tone
                        break
            elif mat == "rubber" and abs(f.nm[1]) < 0.9:
                if (mx / track_period) % 1.0 < 0.45:        # maillons de chenille / sculptures de pneu
                    dt += 0.2
            elif mat == "dark" and f.nm[2] > 0.7:
                if (mx * 0.75) % 1.0 < 0.5:                 # grilles
                    dt += 0.22
            if dust and mz < dust_h:
                h = 1.0 - mz / dust_h
                if grain < h * dust:
                    mat = "earth"
                    dt = 0.0
                else:
                    dt += 0.12 * h * dust
        # Occlusion ambiante près du sol.
        ao = 0.1 * max(0.0, 1.0 - mz / 1.6)
        shade = 0.14 + 0.95 * diffuse + f.fill + spec - f.tint - dt - ao
        mats[i] = mat
        shades[i] = min(1.0, max(0.0, shade))
    return faces, ids, mats, shades, depths, shadow_mask


def render_frame(model, facing, size, scale=1.0, shadow=True, ground=0.0, remap=None):
    W, H = size[0] * SS, size[1] * SS
    faces, ids, mats, shades, depths, shadow_mask = raster(model, facing, W, H, W / 2, H / 2, scale * SS, shadow)
    if remap:
        mats = [remap.get(m, m) if m else m for m in mats]

    # Réduction SSxSS -> 1 : matériau majoritaire, face majoritaire, niveau de la rampe.
    w, h = size
    cells = [None] * (w * h)
    for oy in range(h):
        for ox in range(w):
            counts, sums, fcount, fdepth = {}, {}, {}, {}
            cov_shadow = 0
            for dy in range(SS):
                row = (oy * SS + dy) * W + ox * SS
                for dx in range(SS):
                    i = row + dx
                    m = mats[i]
                    if m:
                        counts[m] = counts.get(m, 0) + 1
                        sums[m] = sums.get(m, 0.0) + shades[i]
                        fid = ids[i]
                        fcount[fid] = fcount.get(fid, 0) + 1
                        fdepth[fid] = fdepth.get(fid, 0.0) + depths[i]
                    elif shadow_mask and shadow_mask[i]:
                        cov_shadow += 1
            cov = sum(counts.values())
            if cov * 2 >= SS * SS:
                m = max(counts, key=counts.get)
                ramp = R.RAMPS[m]
                level = min(len(ramp) - 1, int((1 - sums[m] / counts[m]) * len(ramp)))
                fid = max(fcount, key=fcount.get)
                cells[oy * w + ox] = [m, level, fid, fdepth[fid] / fcount[fid], 0, 0]
            elif cov_shadow * 2 >= SS * SS:
                cells[oy * w + ox] = "shadow"

    # Liserés de relief.
    for oy in range(h):
        for ox in range(w):
            c = cells[oy * w + ox]
            if not c or c == "shadow":
                continue
            for dx, dy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
                nx, ny = ox + dx, oy + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                q = cells[ny * w + nx]
                if not q or q == "shadow" or q[2] == c[2]:
                    continue
                toward_light = dx < 0 or dy < 0
                if q[3] < c[3] - EDGE_DEPTH and toward_light:
                    c[4] = max(c[4], 2 if q[3] < c[3] - 3 * EDGE_DEPTH else 1)   # sous un surplomb : trait d'ombre
                elif q[3] > c[3] + EDGE_DEPTH:
                    if toward_light:
                        c[5] = 1                   # arête d'une pièce en relief, côté lumière
                    else:
                        c[4] = max(c[4], 1)        # arête côté ombre

    out = Image.new("P", size, 0)
    op = out.load()
    for oy in range(h):
        for ox in range(w):
            c = cells[oy * w + ox]
            if c == "shadow":
                op[ox, oy] = R.SHADOW_INDEX
            elif c:
                ramp = R.RAMPS[c[0]]
                op[ox, oy] = ramp[max(0, min(len(ramp) - 1, c[1] + c[4] - c[5]))]
    return out


def _frame(args):
    model, facing, size, scale, shadow, remap = args
    return R.outline(render_frame(model, facing, size, scale, shadow, remap=remap))


def render_rotations(model, size, facings=32, scale=1.0, shadow=True, remap=None):
    from multiprocessing import Pool
    jobs = [(model, i / facings, size, scale, shadow, remap) for i in range(facings)]
    with Pool() as pool:
        return pool.map(_frame, jobs)


def render_icon(model, palette, scale=1.25, facing=0.84, paint=(92, 104, 60), bg=((52, 60, 44), (20, 24, 20))):
    size = (64, 48)
    colors = dict(R.ICON_COLORS, paint=paint, earth=(110, 92, 66))
    W, H = size[0] * SS, size[1] * SS
    faces, ids, mats, shades, depths, shadow_mask = raster(model, facing, W, H, W / 2 - SS, H / 2 + 3 * SS,
                                                           scale * SS, True)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(bg[0][i] * (1 - t) + bg[1][i] * t) for i in range(3)))
    px = img.load()
    for i in range(W * H):
        m = mats[i]
        x, y = i % W, i // W
        if m:
            s = 0.3 + 0.95 * shades[i]
            c = colors[m]
            px[x, y] = tuple(min(255, int(ch * s)) for ch in c)
        elif shadow_mask and shadow_mask[i]:
            r, g, b = px[x, y]
            px[x, y] = (int(r * 0.55), int(g * 0.55), int(b * 0.55))
    return R.quantize_icon(img.resize(size, Image.LANCZOS), palette)
