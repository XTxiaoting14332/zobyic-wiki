"""
原版模型等轴测渲染器（无头、纯 Python）。

读取客户端 JAR 解出的 assets/minecraft/{blockstates,models,textures}，
按方块状态（如 "lightning_rod[facing=east]"）解析出模型与旋转，
在内存中拼装几何体，用 numpy 做逐像素 z-buffer 光栅化，输出透明背景 PNG。

用法见 build.py。
"""
import json
import math
import os
import re
from functools import lru_cache

import numpy as np
from PIL import Image

ASSETS = os.environ.get("MC_ASSETS", os.path.join(os.path.dirname(__file__), "mc", "assets", "minecraft"))

# ---------------------------------------------------------------- 资源读取

def _json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _strip_ns(name):
    return name.split(":", 1)[1] if ":" in name else name


@lru_cache(maxsize=None)
def load_texture(name):
    """name 形如 block/stone；动画贴图取第一帧。返回 RGBA uint8 数组。"""
    name = _strip_ns(name)
    path = os.path.join(ASSETS, "textures", name + ".png")
    if not os.path.exists(path):
        arr = np.zeros((16, 16, 4), np.uint8)
        arr[..., 0] = 255; arr[..., 2] = 255; arr[..., 3] = 255  # 缺图：品红
        return arr
    img = Image.open(path).convert("RGBA")
    if img.height > img.width:
        img = img.crop((0, 0, img.width, img.width))
    return np.asarray(img).copy()


@lru_cache(maxsize=None)
def texture_is_translucent(name):
    a = load_texture(name)[..., 3]
    return bool(((a > 8) & (a < 247)).any())


@lru_cache(maxsize=None)
def load_model(name):
    """解析继承链，返回 (elements, textures)。elements 为原始 dict 列表。"""
    name = _strip_ns(name)
    chain = []
    cur = name
    while cur:
        path = os.path.join(ASSETS, "models", cur + ".json")
        if not os.path.exists(path):
            break
        data = _json(path)
        chain.append(data)
        cur = _strip_ns(data["parent"]) if "parent" in data else None
    textures, elements = {}, None
    for d in reversed(chain):
        textures.update(d.get("textures", {}))
        if "elements" in d:
            elements = d["elements"]
    return elements or [], textures


def resolve_texture(ref, textures):
    seen = set()
    while ref and ref.startswith("#") and ref not in seen:
        seen.add(ref)
        ref = textures.get(ref[1:])
    return _strip_ns(ref) if ref else None

# ---------------------------------------------------------------- 方块状态

SPEC_RE = re.compile(r"^([a-z0-9_:]+)(?:\[(.*)\])?$")


def parse_spec(spec):
    m = SPEC_RE.match(spec.strip())
    if not m:
        raise ValueError(spec)
    bid = _strip_ns(m.group(1))
    props = {}
    if m.group(2):
        for kv in m.group(2).split(","):
            k, v = kv.split("=")
            props[k.strip()] = v.strip()
    return bid, props


def _cond_match(cond, props):
    if "OR" in cond:
        return any(_cond_match(c, props) for c in cond["OR"])
    if "AND" in cond:
        return all(_cond_match(c, props) for c in cond["AND"])
    for k, v in cond.items():
        allowed = str(v).split("|")
        have = props.get(k)
        if have is None:
            # 未指定的属性按"默认值"处理：none / false / 0 / low
            have = "none"
            if "false" in allowed or "true" in allowed:
                have = "false"
            elif "0" in allowed:
                have = "0"
        if have not in allowed:
            return False
    return True


def blockstate_models(bid, props):
    """返回 [(model_name, x, y)]"""
    path = os.path.join(ASSETS, "blockstates", bid + ".json")
    if not os.path.exists(path):
        return [("block/" + bid, 0, 0)]
    bs = _json(path)
    out = []
    if "variants" in bs:
        best, best_score = None, -1
        for key, val in bs["variants"].items():
            conds = dict(kv.split("=") for kv in key.split(",")) if key else {}
            if any(k in props and props[k] != v for k, v in conds.items()):
                continue
            score = sum(1 for k in conds if k in props)
            if score > best_score:
                best, best_score = val, score
        if best is None:
            best = next(iter(bs["variants"].values()))
        if isinstance(best, list):
            best = best[0]
        out.append((best["model"], best.get("x", 0), best.get("y", 0)))
    else:
        for part in bs.get("multipart", []):
            if "when" in part and not _cond_match(part["when"], props):
                continue
            a = part["apply"]
            if isinstance(a, list):
                a = a[0]
            out.append((a["model"], a.get("x", 0), a.get("y", 0)))
    return out

# ---------------------------------------------------------------- 染色

GRASS = (124, 189, 107)
FOLIAGE = (89, 174, 48)
WATER = (63, 118, 228)


def redstone_color(power):
    f = power / 15.0
    r = f * 0.6 + (0.4 if f > 0 else 0.3)
    g = max(0.0, f * f * 0.7 - 0.5)
    b = max(0.0, f * f * 0.6 - 0.7)
    return (int(r * 255), int(g * 255), int(b * 255))


def tint_for(bid, props):
    if bid == "redstone_wire":
        return redstone_color(int(props.get("power", "0")))
    if bid in ("grass_block", "short_grass", "tall_grass", "fern", "large_fern", "sugar_cane"):
        return GRASS
    if bid.endswith("_leaves") or bid in ("vine", "lily_pad"):
        return FOLIAGE
    if bid in ("water", "water_cauldron"):
        return WATER
    return (255, 255, 255)

# ---------------------------------------------------------------- 几何

FACE_CORNERS = {
    # 顺序：左上、右上、右下、左下（从外侧看）
    "north": lambda a, b: [(b[0], b[1], a[2]), (a[0], b[1], a[2]), (a[0], a[1], a[2]), (b[0], a[1], a[2])],
    "south": lambda a, b: [(a[0], b[1], b[2]), (b[0], b[1], b[2]), (b[0], a[1], b[2]), (a[0], a[1], b[2])],
    "west":  lambda a, b: [(a[0], b[1], a[2]), (a[0], b[1], b[2]), (a[0], a[1], b[2]), (a[0], a[1], a[2])],
    "east":  lambda a, b: [(b[0], b[1], b[2]), (b[0], b[1], a[2]), (b[0], a[1], a[2]), (b[0], a[1], b[2])],
    "up":    lambda a, b: [(a[0], b[1], a[2]), (b[0], b[1], a[2]), (b[0], b[1], b[2]), (a[0], b[1], b[2])],
    "down":  lambda a, b: [(a[0], a[1], b[2]), (b[0], a[1], b[2]), (b[0], a[1], a[2]), (a[0], a[1], a[2])],
}
FACE_NORMAL = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0),
               "east": (1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}


def default_uv(face, a, b):
    x0, y0, z0 = a
    x1, y1, z1 = b
    return {
        "up": [x0, z0, x1, z1], "down": [x0, 16 - z1, x1, 16 - z0],
        "north": [16 - x1, 16 - y1, 16 - x0, 16 - y0], "south": [x0, 16 - y1, x1, 16 - y0],
        "west": [z0, 16 - y1, z1, 16 - y0], "east": [16 - z1, 16 - y1, 16 - z0, 16 - y0],
    }[face]


def rot_axis(p, axis, deg, origin):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    x, y, z = p[0] - origin[0], p[1] - origin[1], p[2] - origin[2]
    if axis == "x":
        y, z = y * c - z * s, y * s + z * c
    elif axis == "y":
        x, z = x * c + z * s, -x * s + z * c
    else:
        x, y = x * c - y * s, x * s + y * c
    return (x + origin[0], y + origin[1], z + origin[2])


def state_rot(p, rx, ry, center=(8, 8, 8)):
    """方块状态旋转：先绕 x 再绕 y（与原版一致，y=90 把北转到东）。"""
    if rx:
        t = math.radians(-rx)
        c, s = math.cos(t), math.sin(t)
        x, y, z = p[0] - center[0], p[1] - center[1], p[2] - center[2]
        y, z = y * c - z * s, y * s + z * c
        p = (x + center[0], y + center[1], z + center[2])
    if ry:
        t = math.radians(ry)
        c, s = math.cos(t), math.sin(t)
        x, y, z = p[0] - center[0], p[1] - center[1], p[2] - center[2]
        x, z = x * c - z * s, x * s + z * c
        p = (x + center[0], y + center[1], z + center[2])
    return p


def _rotdir(d, rx, ry):
    p = state_rot(d, rx, ry, center=(0, 0, 0))
    return tuple(int(round(v)) for v in p)


DIRS = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0), "east": (1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}

TRANSLUCENT_BLOCKS = {"water", "ice"}


def fluid_elements(bid, props):
    level = int(props.get("level", "0"))
    h = 14.2 if level == 0 else max(2.0, 14.2 - level * 1.8)
    if bid == "water":
        top, side = "block/water_still", "block/water_flow"
    else:
        top, side = "block/lava_still", "block/lava_flow"
    faces = {}
    for f in ("up", "down", "north", "south", "east", "west"):
        faces[f] = {"texture": top if f in ("up", "down") else side, "tintindex": 0 if bid == "water" else None,
                    "cullface": f if f != "up" else None}
    return [{"from": [0, 0, 0], "to": [16, h, 16], "faces": faces}], {}


class Quad:
    __slots__ = ("pts", "uv", "tex", "tint", "shade", "translucent", "block")

    def __init__(self, pts, uv, tex, tint, shade, translucent, block):
        self.pts, self.uv, self.tex, self.tint = pts, uv, tex, tint
        self.shade, self.translucent, self.block = shade, translucent, block


def _is_full_opaque(spec_cache, bid, props):
    key = (bid, tuple(sorted(props.items())))
    if key in spec_cache:
        return spec_cache[key]
    full = False
    models = blockstate_models(bid, props)
    if len(models) == 1 and bid not in TRANSLUCENT_BLOCKS and bid not in ("water", "lava"):
        els, texs = load_model(models[0][0])
        if len(els) == 1 and els[0]["from"] == [0, 0, 0] and els[0]["to"] == [16, 16, 16] and "rotation" not in els[0]:
            full = True
            for fd in els[0].get("faces", {}).values():
                t = resolve_texture(fd.get("texture"), texs)
                if not t or texture_is_translucent(t) or (load_texture(t)[..., 3] < 128).any():
                    full = False
                    break
    spec_cache[key] = full
    return full


def build_quads(blocks):
    """blocks: list of (x, y, z, spec)"""
    occ = {}
    for x, y, z, spec in blocks:
        occ[(x, y, z)] = parse_spec(spec)
    full_cache = {}
    quads = []
    for (bx, by, bz), (bid, props) in occ.items():
        tint_rgb = tint_for(bid, props)
        if bid in ("water", "lava"):
            model_list = [(None, 0, 0)]
        else:
            model_list = blockstate_models(bid, props)
        for model_name, rx, ry in model_list:
            if model_name is None:
                els, texs = fluid_elements(bid, props)
            else:
                els, texs = load_model(model_name)
            for el in els:
                a, b = el["from"], el["to"]
                erot = el.get("rotation")
                for fname, fd in el.get("faces", {}).items():
                    tex = fd["texture"] if model_name is None else resolve_texture(fd.get("texture"), texs)
                    if not tex:
                        continue
                    # 面剔除：贴着完整不透明方块，或同种半透明方块相邻
                    cf = fd.get("cullface")
                    if cf:
                        d = _rotdir(DIRS[cf], rx, ry)
                        nb = occ.get((bx + d[0], by + d[1], bz + d[2]))
                        if nb:
                            if _is_full_opaque(full_cache, *nb):
                                continue
                            if nb[0] == bid and (bid in ("water", "lava") or "glass" in bid or bid == "fluid"):
                                continue
                    corners = FACE_CORNERS[fname](a, b)
                    if erot:
                        corners = [rot_axis(p, erot["axis"], erot["angle"], erot["origin"]) for p in corners]
                    corners = [state_rot(p, rx, ry) for p in corners]
                    corners = [((p[0] / 16 + bx), (p[1] / 16 + by), (p[2] / 16 + bz)) for p in corners]
                    uv = fd.get("uv") or default_uv(fname, a, b)
                    u0, v0, u1, v1 = uv
                    uvc = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
                    k = (fd.get("rotation", 0) // 90) % 4
                    uvc = [uvc[(i - k) % 4] for i in range(4)]
                    n = FACE_NORMAL[fname]
                    if erot:
                        n = rot_axis(n, erot["axis"], erot["angle"], (0, 0, 0))
                    n = state_rot(n, rx, ry, center=(0, 0, 0))
                    if el.get("shade", True) is False or bid in ("lava",):
                        shade = 1.0
                    else:
                        nx, ny, nz = n
                        shade = nx * nx * 0.6 + nz * nz * 0.8 + ny * ny * (1.0 if ny > 0 else 0.5)
                    tint = tint_rgb if fd.get("tintindex") is not None else None
                    translucent = bid in TRANSLUCENT_BLOCKS or texture_is_translucent(tex)
                    quads.append(Quad(corners, uvc, tex, tint, shade, translucent, (bx, by, bz)))
    return quads

# ---------------------------------------------------------------- 相机与光栅化

PITCH = math.radians(30)
R = np.array([1, 0, -1]) / math.sqrt(2)                              # 屏幕右
U = np.array([-math.sin(PITCH) / math.sqrt(2), math.cos(PITCH), -math.sin(PITCH) / math.sqrt(2)])  # 屏幕上
F = np.array([math.cos(PITCH) / math.sqrt(2), math.sin(PITCH), math.cos(PITCH) / math.sqrt(2)])     # 指向观察者


def project(p, scale):
    p = np.asarray(p, float)
    return float(p @ R * scale), float(-(p @ U) * scale), float(p @ F)


class Rendered:
    def __init__(self, image, scale, offset, ss):
        self.image, self.scale, self.offset, self.ss = image, scale, offset, ss

    def to_px(self, p):
        """世界坐标（方块单位）→ 最终图片像素坐标"""
        x, y, _ = project(p, self.scale)
        return ((x + self.offset[0]) / self.ss, (y + self.offset[1]) / self.ss)


def _raster_tri(P, UV, tex, tint, shade, color, depth, alpha_mode, pad_off):
    """P: 3x3 (sx, sy, depth)，UV: 3x2 (像素坐标)"""
    xs, ys = P[:, 0], P[:, 1]
    H, W = depth.shape
    x0 = max(int(math.floor(xs.min())), 0); x1 = min(int(math.ceil(xs.max())), W - 1)
    y0 = max(int(math.floor(ys.min())), 0); y1 = min(int(math.ceil(ys.max())), H - 1)
    if x1 < x0 or y1 < y0:
        return
    gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
    (ax, ay), (bx, by), (cx, cy) = P[0, :2], P[1, :2], P[2, :2]
    den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
    if abs(den) < 1e-9:
        return
    w0 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / den
    w1 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / den
    w2 = 1 - w0 - w1
    eps = -1e-4
    inside = (w0 >= eps) & (w1 >= eps) & (w2 >= eps)
    if not inside.any():
        return
    z = w0 * P[0, 2] + w1 * P[1, 2] + w2 * P[2, 2]
    th, tw = tex.shape[:2]
    u = w0 * UV[0, 0] + w1 * UV[1, 0] + w2 * UV[2, 0]
    v = w0 * UV[0, 1] + w1 * UV[1, 1] + w2 * UV[2, 1]
    ui = np.clip(np.floor(u).astype(int), 0, tw - 1)
    vi = np.clip(np.floor(v).astype(int), 0, th - 1)
    texel = tex[vi, ui].astype(np.float32)
    a = texel[..., 3] / 255.0
    rgb = texel[..., :3]
    if tint is not None:
        rgb = rgb * (np.array(tint, np.float32) / 255.0)
    rgb = rgb * shade
    zs = depth[y0:y1 + 1, x0:x1 + 1]
    cs = color[y0:y1 + 1, x0:x1 + 1]
    if alpha_mode == "cutout":
        m = inside & (a >= 0.5) & (z > zs)
        zs[m] = z[m]
        cs[m, :3] = rgb[m]
        cs[m, 3] = 1.0
    else:
        m = inside & (a > 0.02) & (z > zs)
        aa = a[m][:, None]
        cs[m, :3] = cs[m, :3] * cs[m, 3:4] * (1 - aa) + rgb[m] * aa
        newa = cs[m, 3:4] + aa * (1 - cs[m, 3:4])
        cs[m, :3] = cs[m, :3] / np.maximum(newa, 1e-6)
        cs[m, 3:4] = newa


def render(blocks, scale=56, ss=2, margin=24):
    """blocks: [(x,y,z,spec)] → Rendered"""
    quads = build_quads(blocks)
    s = scale * ss
    proj = []
    for q in quads:
        pp = [project(p, s) for p in q.pts]
        proj.append(pp)
    allx = [p[0] for pp in proj for p in pp] or [0]
    ally = [p[1] for pp in proj for p in pp] or [0]
    m = margin * ss
    offx, offy = -min(allx) + m, -min(ally) + m
    W = int(math.ceil(max(allx) - min(allx))) + 2 * m
    H = int(math.ceil(max(ally) - min(ally))) + 2 * m
    depth = np.full((H, W), -1e9, np.float32)
    color = np.zeros((H, W, 4), np.float32)

    def tri_data(q, pp):
        tex = load_texture(q.tex)
        th, tw = tex.shape[:2]
        P = np.array([[p[0] + offx, p[1] + offy, p[2]] for p in pp])
        UV = np.array([[u * tw / 16.0, v * th / 16.0] for u, v in q.uv])
        return tex, P, UV

    trans = []
    for q, pp in zip(quads, proj):
        if q.translucent:
            trans.append((q, pp))
            continue
        tex, P, UV = tri_data(q, pp)
        for idx in ((0, 1, 2), (0, 2, 3)):
            _raster_tri(P[list(idx)], UV[list(idx)], tex, q.tint, q.shade, color, depth, "cutout", None)
    # 半透明：由远到近，深度测试但不写深度
    trans.sort(key=lambda t: sum(p[2] for p in t[1]) / 4)
    for q, pp in trans:
        tex, P, UV = tri_data(q, pp)
        for idx in ((0, 1, 2), (0, 2, 3)):
            _raster_tri(P[list(idx)], UV[list(idx)], tex, q.tint, q.shade, color, depth.copy(), "blend", None)
    # color 前三通道是 0-255 线性值，alpha 0-1
    arr = np.zeros((H, W, 4), np.uint8)
    arr[..., :3] = np.clip(color[..., :3], 0, 255).astype(np.uint8)
    arr[..., 3] = np.clip(color[..., 3] * 255, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGBA")
    if ss > 1:
        img = img.resize((W // ss, H // ss), Image.LANCZOS)
    return Rendered(img, s, (offx, offy), ss)
