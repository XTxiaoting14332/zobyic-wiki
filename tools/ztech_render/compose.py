"""
场景 → 成图：自动铺底板、渲染、叠加编号标注与流向箭头。
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

from .render import render

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BADGE_FILL = (245, 158, 11, 255)
BADGE_EDGE = (31, 41, 55, 255)
ARROW = (14, 165, 233, 255)
HALO = (255, 255, 255, 235)


class Scene:
    def __init__(self, name, blocks, labels=None, arrows=None, floor="smooth_stone_slab[type=top]", scale=64, pad=1, legend=None, title=""):
        """
        blocks: [(x, y, z, spec)]，y=0 为地面层
        labels: {编号: (x, y, z)}，标注指向该格中心
        arrows: [((x,y,z), (x,y,z))]，世界坐标（方块中心用 .5）
        floor:  底板方块，None 不铺
        """
        self.name, self.blocks = name, list(blocks)
        self.labels, self.arrows = labels or {}, arrows or []
        self.floor, self.scale, self.pad = floor, scale, pad
        self.legend, self.title = legend or {}, title

    def all_blocks(self):
        bl = list(self.blocks)
        if self.floor:
            occupied = {(x, y, z) for x, y, z, _ in bl}
            xs = [b[0] for b in bl]; zs = [b[2] for b in bl]
            miny = min(b[1] for b in bl)
            fy = miny - 1
            for x in range(min(xs) - self.pad, max(xs) + self.pad + 1):
                for z in range(min(zs) - self.pad, max(zs) + self.pad + 1):
                    if (x, fy, z) not in occupied:
                        bl.append((x, fy, z, self.floor))
        return bl


def _font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def _arrow(d, p0, p1, width=6):
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    head = 16
    tip = p1
    base = (p1[0] - head * math.cos(ang), p1[1] - head * math.sin(ang))
    left = (base[0] + head * 0.55 * math.sin(ang), base[1] - head * 0.55 * math.cos(ang))
    right = (base[0] - head * 0.55 * math.sin(ang), base[1] + head * 0.55 * math.cos(ang))
    for col, w, grow in ((HALO, width + 5, 3), (ARROW, width, 0)):
        d.line([p0, base], fill=col, width=w)
        if grow:
            d.polygon([(tip[0] + grow * math.cos(ang), tip[1] + grow * math.sin(ang)),
                       (left[0] - grow * math.cos(ang) + grow * math.sin(ang), left[1] - grow * math.sin(ang) - grow * math.cos(ang)),
                       (right[0] - grow * math.cos(ang) - grow * math.sin(ang), right[1] - grow * math.sin(ang) + grow * math.cos(ang))], fill=col)
        else:
            d.polygon([tip, left, right], fill=col)


def build(scene, out_dir, max_width=1000):
    scale = scene.scale
    for _ in range(4):
        r = render(scene.all_blocks(), scale=scale, margin=90)
        if r.image.width <= max_width:
            break
        scale = int(scale * max_width / r.image.width)
    img = r.image
    d = ImageDraw.Draw(img)

    for a, b in scene.arrows:
        _arrow(d, r.to_px(a), r.to_px(b))

    font = _font(17)
    rad = 14
    targets = {n: r.to_px((p[0] + 0.5, p[1] + 0.5, p[2] + 0.5)) for n, p in scene.labels.items()}
    if targets:
        cx = sum(t[0] for t in targets.values()) / len(targets)
        cy = sum(t[1] for t in targets.values()) / len(targets) + 40
    placed = []
    for num in sorted(targets):
        tx, ty = targets[num]
        if abs(tx - cx) < 16:
            right = (sorted(targets).index(num) % 2 == 0)
        else:
            right = tx > cx
        base = -0.55 if right else math.pi + 0.55
        best = None
        for k in range(0, 19):
            ang = base + (k + 1) // 2 * (0.3 if k % 2 else -0.3)
            for dist in (52, 70, 90):
                bx, by = tx + dist * math.cos(ang), ty + dist * math.sin(ang)
                if bx < rad + 4 or bx > img.width - rad - 4 or by < rad + 4:
                    continue
                if all((bx - px) ** 2 + (by - py) ** 2 > (2 * rad + 8) ** 2 for px, py in placed) and \
                        all((bx - ox) ** 2 + (by - oy) ** 2 > (rad + 6) ** 2 for ox, oy in targets.values()):
                    best = (bx, by)
                    break
            if best:
                break
        bx, by = best or (tx, ty - 52)
        placed.append((bx, by))
        d.line([(tx, ty), (bx, by)], fill=HALO, width=5)
        d.line([(tx, ty), (bx, by)], fill=BADGE_EDGE, width=2)
        d.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=BADGE_EDGE, outline=HALO, width=1)
    for (bx, by), num in zip(placed, sorted(targets)):
        d.ellipse([bx - rad - 2, by - rad - 2, bx + rad + 2, by + rad + 2], fill=HALO)
        d.ellipse([bx - rad, by - rad, bx + rad, by + rad], fill=BADGE_FILL, outline=BADGE_EDGE, width=2)
        txt = str(num)
        w = d.textlength(txt, font=font)
        d.text((bx - w / 2, by - 11), txt, font=font, fill=(17, 24, 39, 255))

    bbox = img.getbbox()
    if bbox:
        img = img.crop((max(0, bbox[0] - 8), max(0, bbox[1] - 8), min(img.width, bbox[2] + 8), min(img.height, bbox[3] + 8)))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, scene.name + ".png")
    img.save(path, optimize=True)
    return path, img.size
