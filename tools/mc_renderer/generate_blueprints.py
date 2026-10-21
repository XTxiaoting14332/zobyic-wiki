import os, sys
from .rasterizer import render_scene
from .composer import compose_blueprint

OUT_DIR = "/home/nightwind/workspace/zobyic-wiki/docs/public/images/ztech"

def generate_batch1():
    print("=== Generating Blueprints Batch 1 (Scenes 1-20) ===")

    # ================= 1. 多方块锻造炉 =================
    smeltery_blocks = [
        (0, 0, 0, "stone_brick_slab"), (1, 0, 0, "stone_brick_slab"), (2, 0, 0, "stone_brick_slab"),
        (0, 0, 1, "stone_brick_slab"), (1, 0, 1, "stone_brick_slab"), (2, 0, 1, "stone_brick_slab"),
        (0, 0, 2, "stone_brick_slab"), (1, 0, 2, "stone_brick_slab"), (2, 0, 2, "stone_brick_slab"),
        (1, 1, 1, "furnace_on", 0, 180),
        (0, 1, 1, "blast_furnace", 0, 90),
        (2, 1, 1, "blast_furnace", 0, 270),
        (1, 1, 0, "blast_furnace", 0, 180),
        (1, 1, 2, "redstone_block", 0, 0),
        (1, 2, 1, "blast_furnace", 0, 180)
    ]
    img_3d_1 = render_scene(smeltery_blocks, scale=4.2)
    l1 = [
        {
            'title': "第 1 层 (Y=1 底层地基)",
            'note': "3×3 平铺石砖半砖",
            'grid': [
                [ ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)) ],
                [ ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)) ],
                [ ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 核心冶炼层)",
            'note': "中心放熔炉，四周贴高炉",
            'grid': [
                [ None, ('blast_furnace_side', '高炉', (249, 115, 22, 255)), None ],
                [ ('blast_furnace_side', '高炉', (249, 115, 22, 255)), ('furnace_front_on', '熔炉核心', (239, 68, 68, 255)), ('blast_furnace_side', '高炉', (249, 115, 22, 255)) ],
                [ None, ('redstone_block', '电网', (234, 179, 8, 255)), None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 顶部加热层)",
            'note': "熔炉正上方压放 1 个高炉",
            'grid': [
                [ None, None, None ],
                [ None, ('blast_furnace_side', '高炉', (249, 115, 22, 255)), None ],
                [ None, None, None ]
            ]
        }
    ]
    m1 = [
        "【锻造炉核心】× 1（正面朝向通道，投入矿石）",
        "【加热模块】× 4（贴紧核心后、左、右、顶，各加速50%）",
        "【供电线路】× 1（接入工业电网供电）",
        "【地基基座】× 9（平铺 3×3 地面）"
    ]
    ann1 = [
        {
            'rel_pos': (0.48, 0.52),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【锻造炉核心】",
            'lines': ["位于 3×3 正中心，正面朝前", "右键打开界面投入金属矿石"]
        },
        {
            'rel_pos': (0.50, 0.22),
            'card_x': 1140, 'card_y': 340,
            'color': (249, 115, 22),
            'title': "【加热模块】",
            'lines': ["紧贴核心后、左、右、顶四面", "每块提速 50%，全包覆达 4 倍速"]
        },
        {
            'rel_pos': (0.48, 0.72),
            'card_x': 1140, 'card_y': 460,
            'color': (234, 179, 8),
            'title': "【供电接口】",
            'lines': ["紧邻核心底座连接输电线缆", "保证持续供电维持高温炉膛"]
        }
    ]
    compose_blueprint(img_3d_1, os.path.join(OUT_DIR, "smeltery-multiblock.png"),
                      "多方块锻造炉搭建蓝图 (Smeltery Assembly)",
                      l1, m1, ann1)

    # ================= 2. 多方块合金炉 =================
    alloy_blocks = [
        (0, 0, 0, "stone_brick_slab"), (1, 0, 0, "stone_brick_slab"), (2, 0, 0, "stone_brick_slab"),
        (0, 0, 1, "stone_brick_slab"), (1, 0, 1, "stone_brick_slab"), (2, 0, 1, "stone_brick_slab"),
        (0, 0, 2, "stone_brick_slab"), (1, 0, 2, "stone_brick_slab"), (2, 0, 2, "stone_brick_slab"),
        (1, 1, 1, "furnace_on", 0, 180),
        (0, 1, 1, "blast_furnace_on", 0, 90),
        (2, 1, 1, "blast_furnace_on", 0, 270),
        (1, 1, 0, "blast_furnace_on", 0, 180),
        (1, 1, 2, "redstone_block", 0, 0),
        (1, 2, 1, "blast_furnace_on", 0, 180)
    ]
    img_3d_2 = render_scene(alloy_blocks, scale=4.2)
    l2 = [
        {
            'title': "第 1 层 (Y=1 底层地基)",
            'note': "3×3 平铺石砖半砖",
            'grid': [
                [ ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)) ],
                [ ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)) ],
                [ ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)), ('stone_bricks', '石砖', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 双料反应层)",
            'note': "中心放合金炉，外围包覆高炉",
            'grid': [
                [ None, ('blast_furnace_front_on', '高炉', (249, 115, 22, 255)), None ],
                [ ('blast_furnace_front_on', '高炉', (249, 115, 22, 255)), ('furnace_front_on', '合金核心', (239, 68, 68, 255)), ('blast_furnace_front_on', '高炉', (249, 115, 22, 255)) ],
                [ None, ('redstone_block', '电网', (234, 179, 8, 255)), None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 顶部高压密闭层)",
            'note': "正上方加装 1 个高炉",
            'grid': [
                [ None, None, None ],
                [ None, ('blast_furnace_front_on', '高炉', (249, 115, 22, 255)), None ],
                [ None, None, None ]
            ]
        }
    ]
    m2 = [
        "【合金炉核心】× 1（支持双原料同时置入，高效熔铸）",
        "【高温加热模块】× 4（环绕提供极端高温反应环境）",
        "【供电线路】× 1（大功率工业电力接入）",
        "【地基基座】× 9（平铺 3×3 地面）"
    ]
    ann2 = [
        {
            'rel_pos': (0.48, 0.52),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【合金炉核心】",
            'lines': ["支持同时置入两种不同金属粉末", "在高温高压下固相烧结成特种合金"]
        },
        {
            'rel_pos': (0.50, 0.22),
            'card_x': 1140, 'card_y': 340,
            'color': (249, 115, 22),
            'title': "【高温加热模块】",
            'lines': ["多面包覆维持炉膛极端高温", "双份原料转化产出三份合金粉"]
        },
        {
            'rel_pos': (0.48, 0.72),
            'card_x': 1140, 'card_y': 460,
            'color': (234, 179, 8),
            'title': "【高压供电线路】",
            'lines': ["接入工业电网，保障充沛电能供应"]
        }
    ]
    compose_blueprint(img_3d_2, os.path.join(OUT_DIR, "alloy-furnace-multiblock.png"),
                      "多方块合金炉搭建蓝图 (Alloy Furnace Assembly)",
                      l2, m2, ann2)

    # ================= 3. 原位冲压工作站 =================
    press_blocks = [
        (0, 0, 0, "iron_block"), (1, 0, 0, "polished_andesite_slab_top"), (2, 0, 0, "iron_block"),
        (1, 1, -1, "andesite"), (1, 2, -1, "andesite"),
        (1, 2, 0, "piston", -90, 0),
        (1, 3, 0, "lightning_rod", 0, 0)
    ]
    img_3d_3 = render_scene(press_blocks, scale=4.0)
    l3 = [
        {
            'title': "第 1 层 (Y=1 传送带与置物台)",
            'note': "两端传送带支架，中置物料承托台",
            'grid': [
                [ None, ('andesite', '立柱', (148, 163, 184, 255)), None ],
                [ ('iron_block', '入料支架', (148, 163, 184, 255)), ('polished_andesite', '置物台', (56, 189, 248, 255)), ('iron_block', '出料支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 加工空腔与立柱)",
            'note': "预留 1 格空间供物料进出与冲压头下砸",
            'grid': [
                [ None, ('andesite', '立柱', (148, 163, 184, 255)), None ],
                [ None, None, None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 动力冲压机与立柱)",
            'note': "机头朝下，顶部接入旋转应力",
            'grid': [
                [ None, ('andesite', '立柱', (148, 163, 184, 255)), None ],
                [ None, ('piston_top', '冲压机', (249, 115, 22, 255)), None ]
            ]
        },
        {
            'title': "第 4 层 (Y=4 垂直动力传动轴)",
            'note': "动力轴由顶部垂直接入冲压机",
            'grid': [
                [ None, None, None ],
                [ None, ('lightning_rod', '传动轴', (234, 179, 8, 255)), None ]
            ]
        }
    ]
    m3 = [
        "【安山岩置物台】× 1（承托物料，防弹跳吸附）",
        "【动力冲压机】× 1（悬空安装在上方第 2 格，机头垂直向下）",
        "【动力传动轴】× 1（顶部垂直接入旋转动力）",
        "【传送带支架】× 2（两端进出料流水线驱动端）"
    ]
    ann3 = [
        {
            'rel_pos': (0.50, 0.32),
            'card_x': 1140, 'card_y': 220,
            'color': (249, 115, 22),
            'title': "【动力冲压机】",
            'lines': ["悬空安装，机头垂直朝下对准物料", "接入旋转动力后向下往复重压成板"]
        },
        {
            'rel_pos': (0.50, 0.68),
            'card_x': 1140, 'card_y': 360,
            'color': (56, 189, 248),
            'title': "【安山岩置物台】",
            'lines': ["原料平稳静置于台面上方", "冲压完成瞬间自动变为延展成品板材"]
        },
        {
            'rel_pos': (0.50, 0.12),
            'card_x': 1140, 'card_y': 500,
            'color': (234, 179, 8),
            'title': "【垂直动力轴】",
            'lines': ["顶部立式接入旋转传动轴", "转速越高，重锤下砸节拍越快"]
        }
    ]
    compose_blueprint(img_3d_3, os.path.join(OUT_DIR, "depot-press-station.png"),
                      "原位冲压工作站搭建蓝图 (Depot Press Station)",
                      l3, m3, ann3)

    # ================= 4. 原位注液流水线 =================
    spout_blocks = [
        (0, 0, 0, "iron_block"), (1, 0, 0, "stone_slab_top"), (2, 0, 0, "iron_block"),
        (1, 0, -1, "barrel"),
        (1, 1, -1, "barrel"),
        (1, 2, -1, "glass"),
        (1, 2, 0, "glass"),
        (1, 1, 0, "hopper", 0, 0)
    ]
    img_3d_4 = render_scene(spout_blocks, scale=4.4)
    l4 = [
        {
            'title': "第 1 层 (Y=1 物流传动基座)",
            'note': "传送带通向前方，侧面立储水罐",
            'grid': [
                [ None, ('barrel_top', '储液罐', (249, 115, 22, 255)), None ],
                [ ('stone_bricks', '传送带', (148, 163, 184, 255)), ('stone_bricks', '输送位', (56, 189, 248, 255)), ('stone_bricks', '传送带', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 注液喷嘴层)",
            'note': "传送带上方空 1 格供物料通行",
            'grid': [
                [ None, ('barrel_side', '储液罐', (249, 115, 22, 255)), None ],
                [ None, ('hopper_outside', '注液喷嘴', (239, 68, 68, 255)), None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 供液管道网络)",
            'note': "注液器喷嘴朝下，顶接流体管",
            'grid': [
                [ None, ('glass', '流体管', (56, 189, 248, 255)), None ],
                [ None, ('glass', '输液弯头', (56, 189, 248, 255)), None ]
            ]
        }
    ]
    m4 = [
        "【注液喷嘴】× 1（悬空朝下，检测下方物料自动滴注）",
        "【流体储液罐】× 2（储存水、熔融熔岩或化学溶液）",
        "【流体管道】× 2（严格整格密封连接）",
        "【物流传送带】× 3（匀速输送待加工工件）"
    ]
    ann4 = [
        {
            'target_block': (1, 1, 0),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【注液喷嘴】",
            'lines': ["悬空对准传送带工件上方", "当工件到位时精准滴灌流体"]
        },
        {
            'target_block': (1, 2, 0),
            'card_x': 1140, 'card_y': 340,
            'color': (56, 189, 248),
            'title': "【流体管道】",
            'lines': ["密封走线，实时目视观察流向", "无任何液体泄漏损耗"]
        },
        {
            'target_block': (1, 1, -1),
            'card_x': 1140, 'card_y': 460,
            'color': (249, 115, 22),
            'title': "【储液罐】",
            'lines': ["提供持续稳定的供液水压", "支持直接用桶右键注入补给"]
        }
    ]
    compose_blueprint(img_3d_4, os.path.join(OUT_DIR, "spout-conveyor-line.png"),
                      "原位注液流水线搭建蓝图 (Spout Conveyor Line)",
                      l4, m4, ann4)

    # ================= 5. 机械动力传动与转向 =================
    stress_blocks = [
        (0, 0, 0, "tinted_glass"),
        (0, 0, 1, "spruce_log", 90, 0),
        (1, 0, 1, "lightning_rod", 90, 90),
        (2, 0, 1, "carved_pumpkin", 0, 180),
        (3, 0, 1, "pumpkin", 0, 180),
        (4, 0, 1, "barrel", 0, 0),
        (4, 1, 1, "lightning_rod", 0, 0)
    ]
    img_3d_5 = render_scene(stress_blocks, scale=4.0)
    l5 = [
        {
            'title': "整格直线传动与换向流程 (Y=1)",
            'note': "全部方块严格位于整数网格",
            'grid': [
                [ ('tinted_glass', '流水', (56, 189, 248, 255)), ('spruce_log', '水车', (34, 197, 94, 255)), ('lightning_rod', '传动轴', (249, 115, 22, 255)), ('carved_pumpkin', '大齿轮', (234, 179, 8, 255)), ('pumpkin', '小齿轮', (249, 115, 22, 255)), ('barrel_top', '齿轮箱', (168, 85, 247, 255)) ]
            ]
        }
    ]
    m5 = [
        "【水车动力源】× 1 + 流水（提供稳定 16 转/分应力）",
        "【直线传动轴】× 2（沿直线无损传递转速）",
        "【提速齿轮组】× 1（大齿轮啮合小齿轮实现 2:1 提速）",
        "【垂直齿轮箱】× 1（90° 直角转换为向上纵向输出）"
    ]
    ann5 = [
        {
            'rel_pos': (0.16, 0.48),
            'card_x': 1140, 'card_y': 220,
            'color': (34, 197, 94),
            'title': "【水车】",
            'lines': ["流水驱动，零燃料平稳输出 16 转/分"]
        },
        {
            'rel_pos': (0.52, 0.52),
            'card_x': 1140, 'card_y': 340,
            'color': (249, 115, 22),
            'title': "【提速齿轮组】",
            'lines': ["大齿轮驱动小齿轮，转速翻倍至 32 转/分"]
        },
        {
            'rel_pos': (0.75, 0.45),
            'card_x': 1140, 'card_y': 460,
            'color': (168, 85, 247),
            'title': "【垂直齿轮箱】",
            'lines': ["内部伞齿轮将水平旋转 90° 垂直向上导出"]
        }
    ]
    compose_blueprint(img_3d_5, os.path.join(OUT_DIR, "stress-transmission-setup.png"),
                      "机械动力传动与转向蓝图 (Stress Transmission)",
                      l5, m5, ann5)

    # ================= 6. 多方块物品保险库 =================
    vault_blocks = [
        (0, 0, 0, "barrel"), (1, 0, 0, "barrel"),
        (0, 0, 1, "barrel"), (1, 0, 1, "barrel"),
        (0, 1, 0, "barrel"), (1, 1, 0, "barrel"),
        (0, 1, 1, "barrel"), (1, 1, 1, "barrel"),
        (1, 2, 1, "hopper", 0, 0)
    ]
    img_3d_6 = render_scene(vault_blocks, scale=4.4)
    l6 = [
        {
            'title': "第 1 层 (Y=1 保险库基座层)",
            'note': "2×2 平铺容器",
            'grid': [
                [ ('barrel_top', '木桶', (249, 115, 22, 255)), ('barrel_top', '木桶', (249, 115, 22, 255)) ],
                [ ('barrel_top', '木桶', (249, 115, 22, 255)), ('barrel_top', '木桶', (249, 115, 22, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 保险库中扩层)",
            'note': "2×2 向上堆叠扩展容量",
            'grid': [
                [ ('barrel_top', '木桶', (249, 115, 22, 255)), ('barrel_top', '木桶', (249, 115, 22, 255)) ],
                [ ('barrel_top', '木桶', (249, 115, 22, 255)), ('barrel_top', '木桶', (249, 115, 22, 255)) ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 智能物料溜槽)",
            'note': "溜槽严格整格对齐单块顶面！",
            'grid': [
                [ None, None ],
                [ None, ('hopper_outside', '溜槽', (56, 189, 248, 255)) ]
            ]
        }
    ]
    m6 = [
        "【保险库存储矩阵】× 8（上下 2 层，各 2×2 共面堆叠）",
        "【智能物料溜槽】× 1（严格整格对齐顶面，支持自动注入）"
    ]
    ann6 = [
        {
            'rel_pos': (0.50, 0.22),
            'card_x': 1140, 'card_y': 220,
            'color': (56, 189, 248),
            'title': "【智能溜槽】",
            'lines': ["严格整格放置于单块顶面", "绝无悬空跨接缝，支持物料自动注入"]
        },
        {
            'rel_pos': (0.45, 0.55),
            'card_x': 1140, 'card_y': 360,
            'color': (249, 115, 22),
            'title': "【物品保险库】",
            'lines': ["2×2×2 立方体矩阵式紧密共面相连", "空间自动连通共享超大容量"]
        }
    ]
    compose_blueprint(img_3d_6, os.path.join(OUT_DIR, "item-vault-multiblock.png"),
                      "多方块物品保险库搭建蓝图 (Item Vault Assembly)",
                      l6, m6, ann6)

    # ================= 7. 高压蒸汽动力与锅炉机组 =================
    steam_blocks = [
        (0, 0, 0, "tinted_glass"),
        (1, 0, 0, "stone_bricks"),
        (2, 0, 0, "furnace_on", 0, 180),
        (3, 0, 0, "blast_furnace_on", 0, 180),
        (4, 0, 0, "lightning_rod", 90, 90),
        (1, 1, 0, "glass"),
        (2, 1, 0, "glass")
    ]
    img_3d_7 = render_scene(steam_blocks, scale=4.4)
    l7 = [
        {
            'title': "第 1 层 (Y=1 基座与动力层)",
            'note': "水源、水泵、锅炉、引擎与动力轴沿直线串联",
            'grid': [
                [ ('tinted_glass', '水源', (56, 189, 248, 255)), ('stone_bricks', '水泵', (148, 163, 184, 255)), ('furnace_front_on', '锅炉', (239, 68, 68, 255)), ('blast_furnace_front_on', '引擎', (234, 179, 8, 255)), ('lightning_rod', '动力轴', (249, 115, 22, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 严格整格管道层)",
            'note': "管道整格对齐连接",
            'grid': [
                [ None, ('glass', '供水管', (56, 189, 248, 255)), ('glass', '蒸汽管', (239, 68, 68, 255)), None, None ]
            ]
        }
    ]
    m7 = [
        "【高压蒸汽锅炉】× 1（燃烧煤炭产出膨胀高压蒸汽）",
        "【工业抽水泵】× 1（贴紧水源抽取冷凝水）",
        "【流体管道】× 2（密封连接抽水泵与锅炉）",
        "【蒸汽引擎】× 1（高压蒸汽驱动输出 64 转/分）",
        "【动力传动轴】× 1（横向连接引擎输出旋转动力）"
    ]
    ann7 = [
        {
            'rel_pos': (0.46, 0.62),
            'card_x': 1140, 'card_y': 200,
            'color': (239, 68, 68),
            'title': "【高压蒸汽锅炉】",
            'lines': ["燃烧固体煤炭，产出膨胀高压蒸汽"]
        },
        {
            'rel_pos': (0.34, 0.45),
            'card_x': 1140, 'card_y': 320,
            'color': (56, 189, 248),
            'title': "【流体管道】",
            'lines': ["密封走线，实时目视观察流向", "无任何液体或蒸汽泄漏损耗"]
        },
        {
            'rel_pos': (0.62, 0.62),
            'card_x': 1140, 'card_y': 440,
            'color': (234, 179, 8),
            'title': "【蒸汽引擎】",
            'lines': ["蒸汽驱动输出高达 64 转/分强劲机械应力"]
        },
        {
            'rel_pos': (0.86, 0.72),
            'card_x': 1140, 'card_y': 560,
            'color': (249, 115, 22),
            'title': "【传动轴】",
            'lines': ["横向贴紧引擎侧面输出轴", "纯正原味传递旋转动力"]
        }
    ]
    compose_blueprint(img_3d_7, os.path.join(OUT_DIR, "steam-power-setup.png"),
                      "高压蒸汽动力与锅炉机组蓝图 (Steam Power Setup)",
                      l7, m7, ann7)

    # ================= 8. 传送带直角拐弯与分流装配 =================
    corner_blocks = [
        (0, 0, 0, "iron_block"), (1, 0, 0, "stone_slab_top"), (2, 0, 0, "stone_slab_top"), (3, 0, 0, "iron_block"),
        (4, 0, -1, "iron_block"), (4, 0, 0, "stone_slab_top"), (4, 0, 1, "stone_slab_top"), (4, 0, 2, "iron_block"),
        (1, 1, 0, "observer", 0, 180),
        (1, 0, 1, "stone_slab_top")
    ]
    img_3d_8 = render_scene(corner_blocks, scale=3.4)
    l8 = [
        {
            'title': "第 1 层 (Y=1 地面传送带与转角接驳)",
            'note': "主线末端正对转角线带面",
            'grid': [
                [ None, None, None, None, ('iron_block', '支架', (148, 163, 184, 255)) ],
                [ ('iron_block', '支架', (148, 163, 184, 255)), ('stone_bricks', '分流位', (56, 189, 248, 255)), ('stone_bricks', '传送带', (148, 163, 184, 255)), ('iron_block', '主线端', (239, 68, 68, 255)), ('stone_bricks', '转角位', (34, 197, 94, 255)) ],
                [ None, ('stone_bricks', '支线带', (56, 189, 248, 255)), None, None, ('stone_bricks', '传送带', (148, 163, 184, 255)) ],
                [ None, None, None, None, ('iron_block', '支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 悬挂式分流器)",
            'note': "悬空对准主线分流点上方",
            'grid': [
                [ None, None, None, None, None ],
                [ None, ('observer_front', '分流器', (249, 115, 22, 255)), None, None, None ],
                [ None, None, None, None, None ],
                [ None, None, None, None, None ]
            ]
        }
    ]
    m8 = [
        "【传送带支架】× 5（主线与转角线端点驱动）",
        "【传送带半砖】× 6（无缝拼接平整输送跑道）",
        "【悬挂分流器】× 1（架设于带面上方，幽灵白名单分流）",
        "【供电线路】× 1（接入电网驱动带面流转）"
    ]
    ann8 = [
        {
            'rel_pos': (0.68, 0.45),
            'card_x': 1140, 'card_y': 220,
            'color': (34, 197, 94),
            'title': "【末端转交接驳口】",
            'lines': ["主线终点支架正对转角带面", "物料滑出自动 90° 顺畅换向"]
        },
        {
            'rel_pos': (0.35, 0.38),
            'card_x': 1140, 'card_y': 360,
            'color': (249, 115, 22),
            'title': "【悬挂式分流器】",
            'lines': ["悬空架设于带面上方第 1 格", "白名单匹配项推向侧翼支线"]
        },
        {
            'rel_pos': (0.35, 0.65),
            'card_x': 1140, 'card_y': 500,
            'color': (56, 189, 248),
            'title': "【分流支线传送带】",
            'lines': ["侧向承接分流推出的工件", "平稳导向独立分支加工车间"]
        }
    ]
    compose_blueprint(img_3d_8, os.path.join(OUT_DIR, "conveyor-corner-and-splitter.png"),
                      "传送带直角拐弯与分流装配蓝图 (Conveyor Corner & Splitter)",
                      l8, m8, ann8)

    # ================= 9. 垂直传送带提升井 =================
    vert_blocks = [
        (0, 0, 0, "iron_block"), (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "polished_basalt"),
        (2, 1, 0, "polished_basalt"),
        (2, 2, 0, "polished_basalt"),
        (3, 2, 0, "stone_slab_top"), (4, 2, 0, "iron_block")
    ]
    img_3d_9 = render_scene(vert_blocks, scale=3.6)
    l9 = [
        {
            'title': "第 1 层 (Y=1 底层入料接驳)",
            'note': "水平传送带对接提升管底座",
            'grid': [
                [ ('iron_block', '入料支架', (148, 163, 184, 255)), ('stone_bricks', '传送带', (148, 163, 184, 255)), ('polished_basalt_top', '提升基座', (239, 68, 68, 255)), None, None ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 垂直立式井道)",
            'note': "垂直同轴向上堆叠闭锁",
            'grid': [
                [ None, None, ('polished_basalt_side', '提升管', (249, 115, 22, 255)), None, None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 高层出料分发)",
            'note': "顶端出料口直连高层传送带",
            'grid': [
                [ None, None, ('polished_basalt_top', '出料端', (34, 197, 94, 255)), ('stone_bricks', '传送带', (148, 163, 184, 255)), ('iron_block', '出料支架', (148, 163, 184, 255)) ]
            ]
        }
    ]
    m9 = [
        "【垂直传送带】× 3（立式同轴堆叠提升井）",
        "【水平传送带支架】× 2（底层供料与高层接驳）",
        "【传送带半砖】× 2（水平衔接提升井）",
        "【供电线路】× 1（底层驱动端接入电网）"
    ]
    ann9 = [
        {
            'rel_pos': (0.48, 0.45),
            'card_x': 1140, 'card_y': 220,
            'color': (249, 115, 22),
            'title': "【垂直提升管】",
            'lines': ["同轴垂直堆叠闭锁成直立提升井", "底部接电驱动向上极速提升物料"]
        },
        {
            'rel_pos': (0.24, 0.72),
            'card_x': 1140, 'card_y': 360,
            'color': (239, 68, 68),
            'title': "【底层入料口】",
            'lines': ["水平传送带直抵立柱侧面入料口", "地面货物平稳滑入垂直提升仓"]
        },
        {
            'rel_pos': (0.76, 0.32),
            'card_x': 1140, 'card_y': 500,
            'color': (34, 197, 94),
            'title': "【高层出料口】",
            'lines': ["顶端侧向对接二楼水平传送带", "实现多层厂房立体货物调度"]
        }
    ]
    compose_blueprint(img_3d_9, os.path.join(OUT_DIR, "vertical-belt-setup.png"),
                      "垂直传送带提升井搭建蓝图 (Vertical Belt Elevator)",
                      l9, m9, ann9)

    # ================= 10. 智能长臂机械臂 =================
    arm_blocks = [
        (0, 0, 0, "stone_slab_top"), (1, 0, 0, "stone_slab_top"), (2, 0, 0, "stone_slab_top"),
        (1, 0, 1, "lightning_rod", 0, 0),
        (1, 0, 2, "barrel")
    ]
    img_3d_10 = render_scene(arm_blocks, scale=4.2)
    l10 = [
        {
            'title': "第 1 层 (Y=1 机械臂工位布局)",
            'note': "正面来料，中枢抓取，后方投放",
            'grid': [
                [ ('stone', '传送带', (148, 163, 184, 255)), ('stone', '抓取位', (56, 189, 248, 255)), ('stone', '传送带', (148, 163, 184, 255)) ],
                [ None, ('lightning_rod', '机械臂', (249, 115, 22, 255)), None ],
                [ None, ('barrel_top', '储物箱', (34, 197, 94, 255)), None ]
            ]
        }
    ]
    m10 = [
        "【智能长臂机械臂】× 1（中枢基座，180° 旋转摆渡）",
        "【传送带】× 3（正面来料通道，上半砖铺设）",
        "【物料料箱】× 1（后方接收或供料容器）"
    ]
    ann10 = [
        {
            'target_block': (1, 0, 1),
            'card_x': 1140, 'card_y': 220,
            'color': (249, 115, 22),
            'title': "【智能长臂机械臂】",
            'lines': ["自动扫描正面来料通道", "敏捷抓取并旋转 180° 投递"]
        },
        {
            'target_block': (1, 0, 0),
            'card_x': 1140, 'card_y': 360,
            'color': (56, 189, 248),
            'title': "【进料传送带】",
            'lines': ["待转运工件平稳流经扫描范围", "无需停顿即可被即时锁定抓取"]
        },
        {
            'target_block': (1, 0, 2),
            'card_x': 1140, 'card_y': 500,
            'color': (34, 197, 94),
            'title': "【目标储物箱】",
            'lines': ["后方紧邻料箱或二次加工机台", "机械臂精准投递归仓"]
        }
    ]
    compose_blueprint(img_3d_10, os.path.join(OUT_DIR, "mechanical-arm-transfer.png"),
                      "智能长臂机械臂转运蓝图 (Mechanical Arm Transfer)",
                      l10, m10, ann10)

    # ================= 11. 工业自动合成器 =================
    crafter_blocks = [
        (1, 0, -1, "barrel"),
        (1, 0, 0, "crafter", 0, 180),
        (0, 0, 1, "iron_block"),
        (1, 0, 1, "stone_slab_top"),
        (2, 0, 1, "iron_block"),
        (0, 0, 2, "redstone_block")
    ]
    img_3d_11 = render_scene(crafter_blocks, scale=3.8)
    l11 = [
        {
            'title': "第 1 层 (Y=1 自动合成工位与成品流水线)",
            'note': "后置大容量原料仓，中置合成器，前置完整贯通成品流水线",
            'grid': [
                [ None, ('barrel_top', '原料箱', (34, 197, 94, 255)), None ],
                [ None, ('crafter_top', '合成器', (239, 68, 68, 255)), None ],
                [ ('iron_block', '入料支架', (148, 163, 184, 255)), ('stone', '接料带面', (56, 189, 248, 255)), ('iron_block', '出料支架', (34, 197, 94, 255)) ],
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None ]
            ]
        }
    ]
    m11 = [
        "【工业自动合成器】× 1（预设九宫格配方模板，正面喷射成品）",
        "【原料储物箱】× 1（紧贴背侧持续供料，自动提取配方材料）",
        "【成品传送带】× 1（前置完整流水线，包含两端支架与接料带面）",
        "【供电线路】× 1（接入电网驱动瞬时装配）"
    ]
    ann11 = [
        {
            'target_block': (1, 0, 0),
            'card_x': 1140, 'card_y': 200,
            'color': (239, 68, 68),
            'title': "【工业自动合成器】",
            'lines': ["独立落地装配工位，预设九宫格模板，每隔两秒装配一次", "正面吐出成品，绝不破坏或截断主干传送带"]
        },
        {
            'target_block': (1, 0, -1),
            'card_x': 1140, 'card_y': 350,
            'color': (34, 197, 94),
            'title': "【后置原料仓储】",
            'lines': ["紧贴背部 1~3 格放置箱子或保险库，持续自动抽料", "模板槽位被锁闭保护，避免带面杂物混入污染"]
        },
        {
            'target_block': (1, 0, 1),
            'card_x': 1140, 'card_y': 500,
            'color': (56, 189, 248),
            'title': "【成品接料流水线】",
            'lines': ["正前方铺设完整成品传送带（两端支架贯通闭合）", "合成器成品从正面精准吐出至带面上，顺畅运往成品总库"]
        }
    ]
    compose_blueprint(img_3d_11, os.path.join(OUT_DIR, "auto-crafter-setup.png"),
                      "工业自动合成流水线蓝图 (Auto Crafter Assembly)",
                      l11, m11, ann11)

    # ================= 12. 自动农林收割机 =================
    harvester_blocks = [
        (0, 0, 0, "farmland"), (1, 0, 0, "farmland"), (2, 0, 0, "farmland"),
        (0, 0, 1, "farmland"), (1, 0, 1, "dispenser", 0, 180), (2, 0, 1, "farmland"),
        (0, 0, 2, "farmland"), (1, 0, 2, "farmland"), (2, 0, 2, "farmland"),
        (0, 1, 0, "wheat_stage7"), (1, 1, 0, "wheat_stage7"), (2, 1, 0, "wheat_stage7"),
        (0, 1, 1, "wheat_stage7"), (2, 1, 1, "wheat_stage7"),
        (0, 1, 2, "wheat_stage7"), (1, 1, 2, "wheat_stage7"), (2, 1, 2, "wheat_stage7")
    ]
    img_3d_12 = render_scene(harvester_blocks, scale=3.8)
    l12 = [
        {
            'title': "第 1 层 (Y=1 农田基座与收割机核心)",
            'note': "中心放置收割机，四周耕地环绕",
            'grid': [
                [ ('farmland_moist', '耕地', (148, 163, 184, 255)), ('farmland_moist', '耕地', (148, 163, 184, 255)), ('farmland_moist', '耕地', (148, 163, 184, 255)) ],
                [ ('farmland_moist', '耕地', (148, 163, 184, 255)), ('dispenser_front', '收割机', (239, 68, 68, 255)), ('farmland_moist', '耕地', (148, 163, 184, 255)) ],
                [ ('farmland_moist', '耕地', (148, 163, 184, 255)), ('farmland_moist', '耕地', (148, 163, 184, 255)), ('farmland_moist', '耕地', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 作物生长与收获范围)",
            'note': "成熟作物被检测收割并自动补种",
            'grid': [
                [ ('wheat_stage7', '作物', (34, 197, 94, 255)), ('wheat_stage7', '作物', (34, 197, 94, 255)), ('wheat_stage7', '作物', (34, 197, 94, 255)) ],
                [ ('wheat_stage7', '作物', (34, 197, 94, 255)), None, ('wheat_stage7', '作物', (34, 197, 94, 255)) ],
                [ ('wheat_stage7', '作物', (34, 197, 94, 255)), ('wheat_stage7', '作物', (34, 197, 94, 255)), ('wheat_stage7', '作物', (34, 197, 94, 255)) ]
            ]
        }
    ]
    m12 = [
        "【自动农林收割机】× 1（覆盖周围 9×9 农田）",
        "【耕地与作物】× 8（成熟瞬间自动收割并就地补种）",
        "【供电线路】× 1（通电激活自动化巡检）"
    ]
    ann12 = [
        {
            'rel_pos': (0.50, 0.48),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【自动农林收割机】",
            'lines': ["雷达巡检成熟作物，瞬时采收掉落", "收割后自动在原位补种幼苗"]
        },
        {
            'rel_pos': (0.28, 0.45),
            'card_x': 1140, 'card_y': 360,
            'color': (34, 197, 94),
            'title': "【成熟农作物】",
            'lines': ["支持小麦、胡萝卜、马铃薯等作物", "成熟即收，彻底消除自然枯萎损耗"]
        },
        {
            'rel_pos': (0.50, 0.72),
            'card_x': 1140, 'card_y': 500,
            'color': (148, 163, 184),
            'title': "【湿润耕地】",
            'lines': ["周围环绕湿润土壤提供长效肥力", "全自动免人工翻耕施肥"]
        }
    ]
    compose_blueprint(img_3d_12, os.path.join(OUT_DIR, "harvester-farming-setup.png"),
                      "自动农林收割机工作站蓝图 (Harvester Farming Setup)",
                      l12, m12, ann12)

    # ================= 13. 动力锯在线切削 =================
    saw_blocks = [
        (0, 0, 0, "iron_block"), (1, 0, 0, "stone_slab_top"), (2, 0, 0, "stone_slab_top"), (3, 0, 0, "iron_block"),
        (1, 1, 0, "stonecutter"),
        (1, 1, 1, "lightning_rod", 90, 0)
    ]
    img_3d_13 = render_scene(saw_blocks, scale=3.8)
    l13 = [
        {
            'title': "第 1 层 (Y=1 连续传送带跑道)",
            'note': "传送带平整贯穿底部，两端支架驱动",
            'grid': [
                [ ('iron_block', '起点支架', (148, 163, 184, 255)), ('stone_bricks', '传送带', (148, 163, 184, 255)), ('stone_bricks', '传送带', (148, 163, 184, 255)), ('iron_block', '终点支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶置动力锯与传动轴)",
            'note': "动力锯架设于带面上方，侧接传动轴",
            'grid': [
                [ None, ('stonecutter_top', '动力锯', (239, 68, 68, 255)), None, None ],
                [ None, ('lightning_rod', '传动轴', (249, 115, 22, 255)), None, None ]
            ]
        }
    ]
    m13 = [
        "【动力锯】× 1（架设于传送带半砖上方，顶置在线切削）",
        "【传送带支架】× 2（流水线两端驱动支架）",
        "【传送带半砖】× 2（带面平整连续穿过锯刃下方）",
        "【动力传动轴】× 1（侧面注入高速旋转动能）"
    ]
    ann13 = [
        {
            'rel_pos': (0.42, 0.40),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【顶置动力锯】",
            'lines': ["架设于带面上方，原木随传送带穿过瞬间切削", "就地剖切为四块木板与副产物木屑，传送带不中断"]
        },
        {
            'rel_pos': (0.24, 0.65),
            'card_x': 1140, 'card_y': 360,
            'color': (148, 163, 184),
            'title': "【连续输送带】",
            'lines': ["传送带自起点至终点平整贯通", "原木进料与板材出料一体化连续流转"]
        },
        {
            'rel_pos': (0.62, 0.42),
            'card_x': 1140, 'card_y': 500,
            'color': (249, 115, 22),
            'title': "【动力输入轴】",
            'lines': ["侧面直连传动轴注入旋转动力", "转速越高，切削节拍越快"]
        }
    ]
    compose_blueprint(img_3d_13, os.path.join(OUT_DIR, "mechanical-saw-station.png"),
                      "动力锯在线切削蓝图 (Mechanical Saw Station)",
                      l13, m13, ann13)

    # ================= 14. 顶置粉碎机工作站 =================
    crush_blocks = [
        (-1, 0, 0, "iron_block"),
        (0, 0, 0, "stone_slab_top"),
        (1, 0, 0, "iron_block"),
        (0, 1, 0, "dispenser", 0, 180),
        (0, 1, -1, "redstone_block")
    ]
    img_3d_14 = render_scene(crush_blocks, scale=3.8)
    l14 = [
        {
            'title': "第 1 层 (Y=1 连续物流传送带)",
            'note': "两端放置支架，中间平铺传送带半砖",
            'grid': [
                [ ('iron_block', '支架', (148, 163, 184, 255)), ('stone_slab_top', '带面', (249, 115, 22, 255)), ('iron_block', '支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶置粉碎机与供电线路)",
            'note': "粉碎机架设在带面上方，后接工业电网",
            'grid': [
                [ None, ('redstone_block', '电网', (234, 179, 8, 255)), None ],
                [ None, ('dispenser_front', '粉碎机', (239, 68, 68, 255)), None ]
            ]
        }
    ]
    m14 = [
        "【粉碎机】× 1（架设于传送带半砖上方，顶置在线粉碎）",
        "【传送带支架】× 2（流水线两端驱动支架）",
        "【传送带半砖】× 1（带面平整连续贯穿机台正下方）",
        "【供电线路】× 1（接入电网提供 4 能量/秒）"
    ]
    ann14 = [
        {
            'rel_pos': (0.50, 0.35),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【顶置粉碎机】",
            'lines': ["架设于带面上方，需安装研磨头耗材", "原矿随传送带经过时在线粉碎为 2 份精细矿粉"]
        },
        {
            'rel_pos': (0.50, 0.65),
            'card_x': 1140, 'card_y': 360,
            'color': (249, 115, 22),
            'title': "【连续传送带跑道】",
            'lines': ["传送带全程贯通不中断，无需打断流水线", "粉碎后的矿粉继续沿带向下游输送"]
        },
        {
            'rel_pos': (0.65, 0.28),
            'card_x': 1140, 'card_y': 500,
            'color': (234, 179, 8),
            'title': "【工业供电接口】",
            'lines': ["后方接入电网提供 4 能量/秒电力", "支持安装超频芯片进一步加快粉碎节拍"]
        }
    ]
    compose_blueprint(img_3d_14, os.path.join(OUT_DIR, "crushing-wheels-setup.png"),
                      "顶置粉碎机工作站蓝图 (Crusher Station)",
                      l14, m14, ann14)

    # ================= 15. 工业鼓风机洗矿与吹炼 =================
    blower_blocks = [
        (0, 0, 0, "dispenser", 0, 180),
        (0, 0, 1, "campfire"),
        (0, 0, 2, "stone_slab_top"), (-1, 0, 2, "stone_slab_top"), (1, 0, 2, "stone_slab_top")
    ]
    img_3d_15 = render_scene(blower_blocks, scale=3.6)
    l15 = [
        {
            'title': "第 1 层 (Y=1 鼓风机、介质区与流水线)",
            'note': "鼓风机正对烈火/流水，气流笼罩前方传送带",
            'grid': [
                [ None, ('dispenser_front', '鼓风机', (239, 68, 68, 255)), None ],
                [ None, ('furnace_front_on', '热源介质', (249, 115, 22, 255)), None ],
                [ ('stone_bricks', '传送带', (148, 163, 184, 255)), ('stone_bricks', '反应区', (56, 189, 248, 255)), ('stone_bricks', '传送带', (148, 163, 184, 255)) ]
            ]
        }
    ]
    m15 = [
        "【定向工业鼓风机】× 1（后接旋转动力向前吹风）",
        "【转化反应介质】× 1（烈火转化为热风退火，清水转化为洗涤水雾）",
        "【物流传送带】× 3（横向穿过气流区域，带面原位反应）"
    ]
    ann15 = [
        {
            'rel_pos': (0.35, 0.35),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【定向工业鼓风机】",
            'lines': ["强劲气流穿过介质，形成长程原位反应区", "接入应力即刻连续运转"]
        },
        {
            'rel_pos': (0.50, 0.48),
            'card_x': 1140, 'card_y': 360,
            'color': (249, 115, 22),
            'title': "【转化反应介质】",
            'lines': ["热源使气流转化为热风退火吹炼", "水流使气流化为细密洗矿水雾"]
        },
        {
            'rel_pos': (0.62, 0.65),
            'card_x': 1140, 'card_y': 500,
            'color': (56, 189, 248),
            'title': "【原位加工流水线】",
            'lines': ["待处理工件在带面上穿流", "无需进炉，带面上瞬间完成烧炼与洗选"]
        }
    ]
    compose_blueprint(img_3d_15, os.path.join(OUT_DIR, "industrial-blower-setup.png"),
                      "工业鼓风机洗矿与吹炼蓝图 (Industrial Blower Setup)",
                      l15, m15, ann15)

    # ================= 16. 机械手序列装配流水线 =================
    deployer_blocks = [
        (0, 0, 0, "iron_block"), (1, 0, 0, "stone_slab_top"), (2, 0, 0, "stone_slab_top"), (3, 0, 0, "iron_block"),
        (1, 1, 0, "piston", -90, 0),
        (2, 1, 0, "piston", -90, 0)
    ]
    img_3d_16 = render_scene(deployer_blocks, scale=3.8)
    l16 = [
        {
            'title': "第 1 层 (Y=1 连续传送带导轨)",
            'note': "两端支架驱动，带面平直穿过多工位",
            'grid': [
                [ ('iron_block', '起点支架', (148, 163, 184, 255)), ('stone_bricks', '工位1', (56, 189, 248, 255)), ('stone_bricks', '工位2', (56, 189, 248, 255)), ('iron_block', '终点支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 悬空多工位装配机械手)",
            'note': "机械手垂直朝下对准流水线带面",
            'grid': [
                [ None, ('piston_top', '装配手1', (249, 115, 22, 255)), ('piston_top', '装配手2', (234, 179, 8, 255)), None ]
            ]
        }
    ]
    m16 = [
        "【序列装配机械手】× 2（悬挂安装，内置零件向下扣压）",
        "【物流传送带】× 4（贯穿各工位输送半成品）",
        "【动力传动网络】× 1（驱动机械指爪往复精确扣合）"
    ]
    ann16 = [
        {
            'rel_pos': (0.42, 0.42),
            'card_x': 1140, 'card_y': 220,
            'color': (249, 115, 22),
            'title': "【第 1 工位机械手】",
            'lines': ["工件底座经过时前伸扣压安装基础齿轮", "内置弹夹自动补件"]
        },
        {
            'rel_pos': (0.60, 0.45),
            'card_x': 1140, 'card_y': 360,
            'color': (234, 179, 8),
            'title': "【第 2 工位机械手】",
            'lines': ["紧随其后扣压精密微控芯片", "完成连续多道复杂组装工序"]
        },
        {
            'rel_pos': (0.35, 0.65),
            'card_x': 1140, 'card_y': 500,
            'color': (56, 189, 248),
            'title': "【流水装配传送带】",
            'lines': ["半成品沿线匀速滑行", "彻底取代繁琐手工作业"]
        }
    ]
    compose_blueprint(img_3d_16, os.path.join(OUT_DIR, "deployer-assembly-line.png"),
                      "机械手序列装配流水线蓝图 (Deployer Assembly Line)",
                      l16, m16, ann16)

    # ================= 17. 大型风车动力站 =================
    windmill_blocks = [
        (0, 0, 0, "spruce_log"),
        (0, 1, 0, "spruce_log"),
        (0, 2, 0, "white_wool"),
        (0, 2, -1, "lightning_rod", 90, 0)
    ]
    img_3d_17 = render_scene(windmill_blocks, scale=3.8)
    l17 = [
        {
            'title': "第 1~2 层 (Y=1~2 木质立柱塔架)",
            'note': "高耸立柱抬升安装海拔，获取更强风力",
            'grid': [
                [ ('spruce_log', '塔柱', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 单方块风车与输出传动轴)",
            'note': "架设风车，后侧直连传动轴导出旋转动力",
            'grid': [
                [ ('lightning_rod', '传动轴', (249, 115, 22, 255)) ],
                [ ('white_wool', '风车', (56, 189, 248, 255)) ]
            ]
        }
    ]
    m17 = [
        "【风车】× 1（单方块风力发电机具，头顶露天或 Y≥100）",
        "【传动轴】× 1（后置直连，输出 16~48 转/分与 4096 应力）",
        "【支撑立柱】× 2（原木或立柱，提升安装海拔）"
    ]
    ann17 = [
        {
            'rel_pos': (0.50, 0.45),
            'card_x': 1140, 'card_y': 220,
            'color': (56, 189, 248),
            'title': "【风车动力机】",
            'lines': ["单方块风力发电机，头顶露天或海拔 Y≥100 即可运转", "无需复杂拼装，自身即可输出 4096 应力单位"]
        },
        {
            'rel_pos': (0.50, 0.28),
            'card_x': 1140, 'card_y': 360,
            'color': (249, 115, 22),
            'title': "【后置传动轴】",
            'lines': ["紧贴风车背面同轴水平接入", "将 16~48 转/分无损引向车间工作母机"]
        },
        {
            'rel_pos': (0.50, 0.68),
            'card_x': 1140, 'card_y': 500,
            'color': (148, 163, 184),
            'title': "【立柱高空架设】",
            'lines': ["风车所处海拔越高、周围越开阔，转速越疾", "建议高空立柱架设以最大化机械输出"]
        }
    ]
    compose_blueprint(img_3d_17, os.path.join(OUT_DIR, "windmill-power-station.png"),
                      "大型风车动力站装配蓝图 (Windmill Power Station)",
                      l17, m17, ann17)

    # ================= 18. 机械抽水泵与储液储罐管网 =================
    tank_blocks = [
        (0, 0, 0, "tinted_glass"),
        (1, 0, 0, "stone_bricks"),
        (1, 1, 0, "glass"), (2, 1, 0, "glass"),
        (2, 0, 0, "barrel"), (3, 0, 0, "barrel"),
        (2, 0, 1, "barrel"), (3, 0, 1, "barrel")
    ]
    img_3d_18 = render_scene(tank_blocks, scale=3.6)
    l18 = [
        {
            'title': "第 1 层 (Y=1 水源、抽水泵与储液罐基座)",
            'note': "水泵紧贴水源，侧接 2×2 大型储罐群",
            'grid': [
                [ ('tinted_glass', '水源', (56, 189, 248, 255)), ('stone_bricks', '水泵', (148, 163, 184, 255)), ('barrel_top', '储液罐', (249, 115, 22, 255)), ('barrel_top', '储液罐', (249, 115, 22, 255)) ],
                [ None, None, ('barrel_top', '储液罐', (249, 115, 22, 255)), ('barrel_top', '储液罐', (249, 115, 22, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 密封流体管道与高架管网)",
            'note': "管道密封横跨连通水泵与储水罐",
            'grid': [
                [ None, ('glass', '引流管', (56, 189, 248, 255)), ('glass', '注液管', (56, 189, 248, 255)), None ],
                [ None, None, None, None ]
            ]
        }
    ]
    m18 = [
        "【工业抽水泵】× 1（贴紧水源抽取加压送入管网）",
        "【一体化储液罐】× 4（自融合大型储水塔）",
        "【流体管道】× 2（透明密封走线，实时目视观察）",
        "【供电网络】× 1（接入电能驱动水泵运转）"
    ]
    ann18 = [
        {
            'rel_pos': (0.34, 0.65),
            'card_x': 1140, 'card_y': 220,
            'color': (148, 163, 184),
            'title': "【工业抽水泵】",
            'lines': ["紧贴无限水源高效抽取，加压注入管道", "支持全自动连续不断补水"]
        },
        {
            'rel_pos': (0.38, 0.42),
            'card_x': 1140, 'card_y': 360,
            'color': (56, 189, 248),
            'title': "【流体管道】",
            'lines': ["密封走线无滴漏损耗，透明管身清晰可见流向", "支持远距离水压输送"]
        },
        {
            'rel_pos': (0.65, 0.58),
            'card_x': 1140, 'card_y': 500,
            'color': (249, 115, 22),
            'title': "【一体化储液罐】",
            'lines': ["多块紧密共面放置，自动融合成大型水塔", "塔身自带实时刻度监控全厂储量"]
        }
    ]
    compose_blueprint(img_3d_18, os.path.join(OUT_DIR, "fluid-pump-and-tank-setup.png"),
                      "机械抽水泵与储液储罐管网蓝图 (Fluid Pump & Tank Setup)",
                      l18, m18, ann18)

    # ================= 19. 蒸汽发电机组与工业电网 =================
    gen_blocks = [
        (0, 0, 0, "furnace_on", 0, 180),
        (1, 0, 0, "blast_furnace_on", 0, 180),
        (2, 0, 0, "copper_block"),
        (2, 1, 0, "lightning_rod", 0, 0),
        (3, 0, 0, "redstone_block"),
        (1, 1, 0, "glass")
    ]
    img_3d_19 = render_scene(gen_blocks, scale=3.8)
    l19 = [
        {
            'title': "第 1 层 (Y=1 热力机组、发电机与配电箱)",
            'note': "锅炉、透平轮机、发电机与配电储能箱直连",
            'grid': [
                [ ('furnace_front_on', '锅炉', (239, 68, 68, 255)), ('blast_furnace_front_on', '透平轮机', (249, 115, 22, 255)), ('copper_block', '发电机', (56, 189, 248, 255)), ('redstone_block', '储能箱', (234, 179, 8, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 蒸汽引管与高压导电柱)",
            'note': "管路密封与高压线缆引出",
            'grid': [
                [ None, ('glass', '蒸汽管', (239, 68, 68, 255)), ('lightning_rod', '导电柱', (234, 179, 8, 255)), None ]
            ]
        }
    ]
    m19 = [
        "【高压蒸汽锅炉】× 1（燃料燃烧产出高压蒸汽）",
        "【蒸汽轮机】× 1（高速热力透平转化为旋转应力）",
        "【应力发电机】× 1（机械应力高转化率发电）",
        "【变压配电储能箱】× 1（稳压输出，接入全厂高压电网）",
        "【流体管道】× 1（密闭输送高压蒸汽）"
    ]
    ann19 = [
        {
            'rel_pos': (0.35, 0.62),
            'card_x': 1140, 'card_y': 220,
            'color': (249, 115, 22),
            'title': "【高压蒸汽轮机】",
            'lines': ["高压蒸汽驱动高速旋转，提供强力转速", "热机效率极高，输出平稳澎湃"]
        },
        {
            'rel_pos': (0.58, 0.45),
            'card_x': 1140, 'card_y': 360,
            'color': (56, 189, 248),
            'title': "【应力发电机】",
            'lines': ["吸收轮机转速瞬间转化为高压工业电力", "实现动力到电力的高效跨界转化"]
        },
        {
            'rel_pos': (0.78, 0.65),
            'card_x': 1140, 'card_y': 500,
            'color': (234, 179, 8),
            'title': "【配电储能箱】",
            'lines': ["稳压整流缓冲负荷波动", "通过高压电缆输送全厂各车间"]
        }
    ]
    compose_blueprint(img_3d_19, os.path.join(OUT_DIR, "power-generation-station.png"),
                      "蒸汽发电机组与工业电网蓝图 (Power Generation Station)",
                      l19, m19, ann19)

    # ================= 20. 重型地脉开采钻探平台 =================
    rig_blocks = [
        # 中心开采平台
        (0, 0, 0, "crafter", 0, 180),
        # 电力接入
        (0, 0, 1, "redstone_block")
    ]
    # 外围 5x5 铁栏杆闭合圈 (16 根)
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) == 2 or abs(dz) == 2:
                rig_blocks.append((dx, 0, dz, "iron_bars_post"))
    
    img_3d_20 = render_scene(rig_blocks, scale=2.8)
    l20 = [
        {
            'title': "5×5 平面布局 (Y=1 中心平台与外围防护铁栏杆)",
            'note': "中心放置开采机，外围必须由 16 根铁栏杆完全闭合",
            'grid': [
                [ ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)) ],
                [ ('iron_bars', '铁栏杆', (148, 163, 184, 255)), None, None, None, ('iron_bars', '铁栏杆', (148, 163, 184, 255)) ],
                [ ('iron_bars', '铁栏杆', (148, 163, 184, 255)), None, ('crafter_top', '开采核心', (239, 68, 68, 255)), None, ('iron_bars', '铁栏杆', (148, 163, 184, 255)) ],
                [ ('iron_bars', '铁栏杆', (148, 163, 184, 255)), None, ('redstone_block', '电网', (234, 179, 8, 255)), None, ('iron_bars', '铁栏杆', (148, 163, 184, 255)) ],
                [ ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)), ('iron_bars', '铁栏杆', (148, 163, 184, 255)) ]
            ]
        }
    ]
    m20 = [
        "【重型地脉勘探开采平台】× 1（安放于 5×5 区域正中心）",
        "【安全防护铁栏杆】× 16（外围 5×5 边界完整闭合，缺一不可）",
        "【工业供电线路】× 1（持续输入 100 能量/秒高压电力）"
    ]
    ann20 = [
        {
            'rel_pos': (0.50, 0.48),
            'card_x': 1140, 'card_y': 220,
            'color': (239, 68, 68),
            'title': "【重型地脉开采平台】",
            'lines': ["微观引力共振富集深层矿脉，无损生态采矿", "无需向下挖掘大坑，原位持续产出珍稀矿藏"]
        },
        {
            'rel_pos': (0.28, 0.65),
            'card_x': 1140, 'card_y': 360,
            'color': (148, 163, 184),
            'title': "【安全防护铁栏杆】",
            'lines': ["外围 5×5 边界必须由 16 根铁栏杆完全闭合", "闭合形成安全力场；若有缺失系统将停机报警"]
        },
        {
            'rel_pos': (0.50, 0.62),
            'card_x': 1140, 'card_y': 500,
            'color': (234, 179, 8),
            'title': "【高压工业供电】",
            'lines': ["持续消耗 100 能量/秒驱动深层引力场", "需接入主干电网保障充足高压电能"]
        }
    ]
    compose_blueprint(img_3d_20, os.path.join(OUT_DIR, "geothermal-rig-multiblock.png"),
                      "重型地脉开采平台蓝图 (Geothermal Rig Assembly)",
                      l20, m20, ann20)

    print("Batch 1 (20 blueprints) generated successfully!")

def generate_all():
    from .blueprints_batch2 import generate_batch2
    from .blueprints_batch3 import generate_batch3
    from .blueprints_batch4 import generate_batch4
    from .blueprints_batch5 import generate_batch5
    generate_batch1()
    generate_batch2()
    generate_batch3()
    generate_batch4()
    generate_batch5()
    print("All 75 blueprints generated successfully!")

if __name__ == "__main__":
    generate_all()
