import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .model_resolver import get_texture_image

FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def wrap_text(d, text, font, max_width):
    """把文本按像素宽度自动拆分为多行，支持中英文字符"""
    lines = []
    cur_line = ""
    for ch in text:
        test_line = cur_line + ch
        w = d.textbbox((0, 0), test_line, font=font)[2]
        if w > max_width and cur_line:
            lines.append(cur_line)
            cur_line = ch
        else:
            cur_line = test_line
    if cur_line:
        lines.append(cur_line)
    return lines

def compose_blueprint(scene_3d_img, out_png_path, title, layers_data, materials_list, annotations_3d):
    """
    通用工业装配教程双视窗蓝图合成器：
    - 统一分辨率 1440x880
    - 左侧面板：分层解剖俯视网格（Layer by Layer）+ 必备材料清单（自适应高度，严禁溢出）
    - 右侧面板：客户端原生模型 3D 等轴测成型图 + Z-Tech 纯正构件引线说明
    - 仅保留核心标题与右下角“Z-Tech 工业装配规范”，剔除多余副标题
    """
    canvas_w = 1440
    canvas_h = 880
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (15, 23, 42, 255))
    d = ImageDraw.Draw(canvas)

    # 背景网格
    for gx in range(0, canvas_w, 32):
        for gy in range(0, canvas_h, 32):
            d.point((gx, gy), fill=(51, 65, 85, 120))

    # 字体配置
    font_title = get_font(28)
    font_foot = get_font(13)
    font_h2 = get_font(18)
    font_layer = get_font(15)
    font_desc = get_font(13)
    font_bold = get_font(14)
    font_tag = get_font(11)

    # 顶部标题栏（纯主标题，无多余副标题）
    d.text((48, 36), title, font=font_title, fill=(241, 245, 249, 255))
    d.line([(48, 86), (canvas_w - 48, 86)], fill=(51, 65, 85, 180), width=1)

    # ================= 左侧面板 =================
    panel_x = 48
    panel_y = 110
    panel_w = 540
    panel_h = 730

    d.rounded_rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
                        radius=8, outline=(71, 85, 105, 255), fill=(30, 41, 59, 180), width=1)

    # 左侧面板标题（去除冗余副标题）
    d.text((panel_x + 24, panel_y + 22), "▼ 乐高式分层剖面放置指南（俯视网格）", font=font_h2, fill=(56, 189, 248, 255))

    # ================= 必备材料清单（预先计算高度与安全位置） =================
    num_items = len(materials_list)
    line_h = 22
    box_inner_h = 36 + num_items * line_h + 16
    list_box_y = panel_y + panel_h - box_inner_h - 16

    # 自适应网格单元大小，严格杜绝网格与底部清单重叠
    num_layers = len(layers_data)
    total_rows = sum(len(l['grid']) for l in layers_data)
    max_cols = max(len(l['grid'][0]) for l in layers_data)
    avail_h = (list_box_y - 16) - (panel_y + 60) - (num_layers * 26)
    cell_h = (avail_h // max(1, total_rows)) - 4
    cell_w = (460 // max(1, max_cols)) - 4
    cell = min(44, cell_h, cell_w)
    cell = max(26, cell)
    gap = 4

    cur_y = panel_y + 60
    for l_info in layers_data:
        l_title = l_info['title']
        l_note = l_info.get('note', '')
        l_grid = l_info['grid']

        d.text((panel_x + 32, cur_y), l_title, font=font_layer, fill=(248, 250, 252, 255))
        if l_note:
            tw = d.textbbox((0, 0), l_title, font=font_layer)[2]
            d.text((panel_x + 32 + tw + 14, cur_y + 2), l_note, font=font_desc, fill=(203, 213, 225, 255))

        rows = len(l_grid)
        cols = len(l_grid[0])
        for r in range(rows):
            for c in range(cols):
                cx = panel_x + 32 + c * (cell + gap)
                cy = cur_y + 22 + r * (cell + gap)
                item = l_grid[r][c]

                d.rounded_rectangle([cx, cy, cx + cell - 1, cy + cell - 1], radius=4,
                                    outline=(100, 116, 139, 255), fill=(15, 23, 42, 220), width=1)
                if item:
                    tex_name, name_txt, col_tag = item
                    tex_pad = 12 if cell >= 38 else 8
                    tex_size = max(14, cell - tex_pad)
                    tex = get_texture_image(tex_name).resize((tex_size, tex_size), Image.Resampling.NEAREST)
                    canvas.paste(tex, (cx + (cell - tex_size) // 2, cy + 3), tex)
                    f_tag = font_tag if cell >= 36 else get_font(9)
                    d_c_w = d.textbbox((0, 0), name_txt, font=f_tag)[2]
                    d.text((cx + (cell - d_c_w) // 2, cy + cell - (13 if cell >= 36 else 11)), name_txt, font=f_tag, fill=col_tag)
                else:
                    d.text((cx + cell // 2 - 4, cy + cell // 2 - 8), "·", font=font_desc, fill=(71, 85, 105, 255))

        cur_y += 24 + rows * (cell + gap) + 12

    # 绘制必备材料清单面板
    d.rounded_rectangle([panel_x + 20, list_box_y, panel_x + panel_w - 20, list_box_y + box_inner_h],
                        radius=6, outline=(249, 115, 22, 180), fill=(15, 23, 42, 240), width=1)
    d.text((panel_x + 34, list_box_y + 12), "必备材料清单", font=font_bold, fill=(249, 115, 22, 255))
    for m_idx, m_txt in enumerate(materials_list):
        d.text((panel_x + 34, list_box_y + 38 + m_idx * line_h), f"• {m_txt}", font=font_desc, fill=(241, 245, 249, 255))

    # ================= 右侧面板：3D 模型 =================
    d.text((630, 110), "▼ 完整装配成型效果", font=font_h2, fill=(248, 250, 252, 255))

    target_max_w = 640
    target_max_h = 460
    w_scale = target_max_w / scene_3d_img.width
    h_scale = target_max_h / scene_3d_img.height
    fit_scale = min(w_scale, h_scale, 1.8)

    scaled_w = int(scene_3d_img.width * fit_scale)
    scaled_h = int(scene_3d_img.height * fit_scale)
    scaled_3d = scene_3d_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

    model_x = 640 + (target_max_w - scaled_w) // 2
    model_y = 190 + (target_max_h - scaled_h) // 2

    # 底部阴影
    sh_w = int(scaled_w * 0.85)
    sh_h = 90
    sh_img = Image.new("RGBA", (sh_w, sh_h), (0, 0, 0, 0))
    d_sh = ImageDraw.Draw(sh_img)
    d_sh.ellipse([10, 10, sh_w - 10, sh_h - 10], fill=(5, 10, 20, 140))
    sh_img = sh_img.filter(ImageFilter.GaussianBlur(16))
    canvas.paste(sh_img, (model_x + (scaled_w - sh_w) // 2, model_y + scaled_h - 45), sh_img)

    canvas.paste(scaled_3d, (model_x, model_y), scaled_3d)

    # 构件引线与说明卡片（仅 Z-Tech 纯正名称，自适应折行防溢出）
    for ann in annotations_3d:
        # 1. 优先使用 target_block 精确匹配三维方块投影中心
        if 'target_block' in ann and hasattr(scene_3d_img, 'block_rel'):
            tb = ann['target_block']
            if tb in scene_3d_img.block_rel:
                rx, ry = scene_3d_img.block_rel[tb]
            else:
                rx, ry = ann.get('rel_pos', (0.5, 0.5))
        else:
            rx, ry = ann.get('rel_pos', (0.5, 0.5))

        # 2. 若指针落在透明空气区域，就近自动吸附至最近的不透明方块中心，杜绝指空
        orig_px = int(scene_3d_img.width * rx)
        orig_py = int(scene_3d_img.height * ry)
        cx = max(0, min(scene_3d_img.width - 1, orig_px))
        cy = max(0, min(scene_3d_img.height - 1, orig_py))
        if scene_3d_img.getpixel((cx, cy))[3] < 30 and hasattr(scene_3d_img, 'block_rel') and scene_3d_img.block_rel:
            best_dist = 999999.0
            best_pos = (rx, ry)
            for (bgx, bgy, bgz), (brx, bry) in scene_3d_img.block_rel.items():
                bpx = int(scene_3d_img.width * brx)
                bpy = int(scene_3d_img.height * bry)
                bcx = max(0, min(scene_3d_img.width - 1, bpx))
                bcy = max(0, min(scene_3d_img.height - 1, bpy))
                if scene_3d_img.getpixel((bcx, bcy))[3] >= 30:
                    dist_sq = (brx - rx)**2 + (bry - ry)**2
                    if dist_sq < best_dist:
                        best_dist = dist_sq
                        best_pos = (brx, bry)
            rx, ry = best_pos

        target_pt_x = model_x + int(scaled_w * rx)
        target_pt_y = model_y + int(scaled_h * ry)

        col = ann.get('color', (56, 189, 248))
        ann_title = ann['title']
        raw_lines = ann['lines']

        # 最大文本宽度限制在 240px 内，超长文字自动折行
        max_text_w = 240
        wrapped_lines = []
        for l_txt in raw_lines:
            wrapped_lines.extend(wrap_text(d, l_txt, font_desc, max_text_w))

        # 计算卡片尺寸
        title_w = d.textbbox((0, 0), ann_title, font=font_bold)[2]
        content_max_w = max([title_w] + [d.textbbox((0, 0), wl, font=font_desc)[2] for wl in wrapped_lines]) if wrapped_lines else title_w
        card_w = max(250, content_max_w + 32)
        card_w = min(card_w, 290)

        # 确保卡片完全收纳在右侧画布内，绝不超出右边界（canvas_w = 1440）
        card_x = ann['card_x']
        if card_x + card_w > canvas_w - 24:
            card_x = canvas_w - 24 - card_w

        line_h = 18
        card_h = 12 + 18 + 8 + len(wrapped_lines) * line_h + 10
        card_y = ann['card_y']

        # 绘制指示点与引线
        d.ellipse([target_pt_x - 4, target_pt_y - 4, target_pt_x + 4, target_pt_y + 4], fill=col + (255,))
        conn_x = card_x if card_x >= target_pt_x else card_x + card_w
        conn_y = card_y + min(28, card_h // 2)
        d.line([(target_pt_x, target_pt_y), (conn_x, conn_y)], fill=col + (255,), width=2)

        # 绘制卡片背景框与文字
        d.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h],
                            radius=6, outline=col + (220,), fill=(30, 41, 59, 240), width=1)
        d.text((card_x + 16, card_y + 10), ann_title, font=font_bold, fill=col + (255,))
        for l_idx, l_txt in enumerate(wrapped_lines):
            d.text((card_x + 16, card_y + 34 + l_idx * line_h), l_txt, font=font_desc, fill=(203, 213, 225, 255))

    # 右下角水印：严格只保留“Z-Tech 工业装配规范”
    d.text((canvas_w - 200, canvas_h - 36), "Z-Tech 工业装配规范", font=font_foot, fill=(100, 116, 139, 220))

    os.makedirs(os.path.dirname(out_png_path), exist_ok=True)
    canvas.save(out_png_path)
    print(f"Blueprint successfully written to {out_png_path}")
