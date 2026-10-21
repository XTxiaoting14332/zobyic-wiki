import math
import numpy as np
from PIL import Image, ImageDraw
from .model_resolver import resolve_model, get_texture_image

def rotate_point_around_center(pt, rx, ry, center=(8, 8, 8)):
    cx, cy, cz = center
    x = pt[0] - cx
    y = pt[1] - cy
    z = pt[2] - cz

    if rx != 0:
        rad_x = math.radians(rx)
        cos_x = math.cos(rad_x)
        sin_x = math.sin(rad_x)
        y_new = y * cos_x - z * sin_x
        z_new = y * sin_x + z * cos_x
        y, z = y_new, z_new

    if ry != 0:
        rad_y = math.radians(-ry) # negative for clockwise looking down
        cos_y = math.cos(rad_y)
        sin_y = math.sin(rad_y)
        x_new = x * cos_y - z * sin_y
        z_new = x * sin_y + z * cos_y
        x, z = x_new, z_new

    return [x + cx, y + cy, z + cz]

def render_scene(blocks, scale=5.0, yaw=45, pitch=30):
    """
    blocks: list of (gx, gy, gz, model_name, rx, ry)
    """
    all_quads = []

    for item in blocks:
        if len(item) == 4:
            gx, gy, gz, model_name = item
            rx, ry = 0, 0
        else:
            gx, gy, gz, model_name, rx, ry = item

        elements = resolve_model(model_name)
        if not elements:
            continue

        for el in elements:
            x0, y0, z0 = el["from"]
            x1, y1, z1 = el["to"]

            face_defs = {
                "up": {
                    "corners": [[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]],
                    "shade": 1.0,
                    "normal": [0, 1, 0]
                },
                "down": {
                    "corners": [[x0, y0, z1], [x1, y0, z1], [x1, y0, z0], [x0, y0, z0]],
                    "shade": 0.5,
                    "normal": [0, -1, 0]
                },
                "north": {
                    "corners": [[x1, y1, z0], [x0, y1, z0], [x0, y0, z0], [x1, y0, z0]],
                    "shade": 0.8,
                    "normal": [0, 0, -1]
                },
                "south": {
                    "corners": [[x0, y1, z1], [x1, y1, z1], [x1, y0, z1], [x0, y0, z1]],
                    "shade": 0.8,
                    "normal": [0, 0, 1]
                },
                "west": {
                    "corners": [[x0, y1, z0], [x0, y1, z1], [x0, y0, z1], [x0, y0, z0]],
                    "shade": 0.65,
                    "normal": [-1, 0, 0]
                },
                "east": {
                    "corners": [[x1, y1, z1], [x1, y1, z0], [x1, y0, z0], [x1, y0, z1]],
                    "shade": 0.65,
                    "normal": [1, 0, 0]
                }
            }

            for f_name, f_data in el.get("faces", {}).items():
                if f_name not in face_defs:
                    continue
                tex_name = f_data.get("texture")
                uv = f_data.get("uv", [0, 0, 16, 16])
                rot = f_data.get("rotation", 0)

                corners_3d = face_defs[f_name]["corners"]
                rotated_corners = [rotate_point_around_center(pt, rx, ry) for pt in corners_3d]
                world_corners = [[pt[0] + gx * 16, pt[1] + gy * 16, pt[2] + gz * 16] for pt in rotated_corners]

                normal_3d = face_defs[f_name]["normal"]
                rot_norm = rotate_point_around_center(normal_3d, rx, ry, center=(0, 0, 0))

                all_quads.append({
                    "corners": world_corners,
                    "normal": rot_norm,
                    "shade": face_defs[f_name]["shade"],
                    "texture": tex_name,
                    "uv": uv,
                    "rotation": rot,
                    "is_glass": "glass" in str(tex_name)
                })

    cos30 = math.cos(math.radians(pitch))
    sin30 = math.sin(math.radians(pitch))

    def project_pt(pt):
        x, y, z = pt
        px = (x - z) * cos30 * scale
        py = (-y + (x + z) * sin30) * scale
        depth = (x + z) + y * 0.577
        return px, py, depth

    projected_quads = []
    all_px = []
    all_py = []

    for q in all_quads:
        proj_pts = [project_pt(pt) for pt in q["corners"]]
        p0, p1, p2, p3 = proj_pts
        cross = (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0])
        if cross <= 0:
            continue

        avg_depth = sum(p[2] for p in proj_pts) / 4.0
        projected_quads.append({
            "proj_pts": proj_pts,
            "depth": avg_depth,
            "quad": q
        })
        for p in proj_pts:
            all_px.append(p[0])
            all_py.append(p[1])

    if not projected_quads:
        return Image.new("RGBA", (100, 100), (0, 0, 0, 0))

    min_px = min(all_px)
    max_px = max(all_px)
    min_py = min(all_py)
    max_py = max(all_py)

    pad = 40
    cw = int(math.ceil(max_px - min_px)) + pad * 2
    ch = int(math.ceil(max_py - min_py)) + pad * 2
    offset_x = -min_px + pad
    offset_y = -min_py + pad

    canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))

    # Sort quads by depth (Painter's algorithm: smallest depth to largest)
    projected_quads.sort(key=lambda item: (1 if item["quad"]["is_glass"] else 0, item["depth"]))

    def render_textured_quad(canvas, tex_img, dst_pts):
        w, h = tex_img.size
        src_pts = np.array([[0, 0], [w, 0], [0, h]], dtype=np.float64)
        dst_tri = np.array([dst_pts[0], dst_pts[1], dst_pts[3]], dtype=np.float64)

        A = np.column_stack([dst_tri, np.ones(3)])
        try:
            M = np.linalg.solve(A, src_pts)
        except np.linalg.LinAlgError:
            return

        a, d = M[0]
        b, e = M[1]
        c, f = M[2]

        min_x = int(math.floor(min(p[0] for p in dst_pts)))
        max_x = int(math.ceil(max(p[0] for p in dst_pts)))
        min_y = int(math.floor(min(p[1] for p in dst_pts)))
        max_y = int(math.ceil(max(p[1] for p in dst_pts)))

        bw = max_x - min_x + 1
        bh = max_y - min_y + 1
        if bw <= 0 or bh <= 0:
            return

        local_c = a * min_x + b * min_y + c
        local_f = d * min_x + e * min_y + f
        local_coeffs = (a, b, local_c, d, e, local_f)

        warped = tex_img.transform((bw, bh), Image.Transform.AFFINE, local_coeffs, resample=Image.Resampling.NEAREST)

        mask = Image.new("L", (bw, bh), 0)
        draw_mask = ImageDraw.Draw(mask)
        local_pts = [(p[0] - min_x, p[1] - min_y) for p in dst_pts]
        draw_mask.polygon(local_pts, fill=255)

        warped.putalpha(Image.composite(warped.getchannel('A'), Image.new('L', (bw, bh), 0), mask))
        canvas.alpha_composite(warped, (min_x, min_y))

    for item in projected_quads:
        q = item["quad"]
        dst_pts = [(p[0] + offset_x, p[1] + offset_y) for p in item["proj_pts"]]

        tex_full = get_texture_image(q["texture"])
        uv = q["uv"]
        u0, v0, u1, v1 = uv

        tw, th = tex_full.size
        px_u0 = int(u0 * tw / 16.0)
        px_v0 = int(v0 * th / 16.0)
        px_u1 = int(u1 * tw / 16.0)
        px_v1 = int(v1 * th / 16.0)

        left = min(px_u0, px_u1)
        right = max(px_u0, px_u1)
        top = min(px_v0, px_v1)
        bottom = max(px_v0, px_v1)

        if right <= left or bottom <= top:
            continue

        cropped = tex_full.crop((left, top, right, bottom))
        if px_u1 < px_u0:
            cropped = cropped.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if px_v1 < px_v0:
            cropped = cropped.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        rot = q["rotation"]
        if rot == 90:
            cropped = cropped.transpose(Image.Transpose.ROTATE_270)
        elif rot == 180:
            cropped = cropped.transpose(Image.Transpose.ROTATE_180)
        elif rot == 270:
            cropped = cropped.transpose(Image.Transpose.ROTATE_90)

        shade = q["shade"]
        if shade < 0.99:
            shaded = Image.eval(cropped, lambda v: int(v * shade))
            shaded.putalpha(cropped.getchannel('A'))
            cropped = shaded

        render_textured_quad(canvas, cropped, dst_pts)

    # Crop excess transparency
    bbox = canvas.getbbox()
    if bbox:
        canvas = canvas.crop(bbox)

    block_rel = {}
    crop_x0, crop_y0 = (bbox[0], bbox[1]) if bbox else (0, 0)
    final_w, final_h = canvas.size

    for item in blocks:
        gx, gy, gz = item[:3]
        model = str(item[3])
        off_y = 12 if "slab_top" in model or "hopper" in model else (4 if "slab" in model else 8)
        wx = gx * 16 + 8
        wy = gy * 16 + off_y
        wz = gz * 16 + 8
        px, py, _ = project_pt((wx, wy, wz))
        rx = (px + offset_x - crop_x0) / max(1, final_w)
        ry = (py + offset_y - crop_y0) / max(1, final_h)
        block_rel[(gx, gy, gz)] = (max(0.02, min(0.98, rx)), max(0.02, min(0.98, ry)))
    canvas.block_rel = block_rel

    return canvas
