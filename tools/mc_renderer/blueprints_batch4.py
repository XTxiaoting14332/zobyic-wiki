import os
from .rasterizer import render_scene
from .composer import compose_blueprint

OUT_DIR = "/home/nightwind/workspace/zobyic-wiki/docs/public/images/ztech"

def generate_batch4():
    print("=== Generating Blueprints Batch 4 (Starter, Power Cabling & Advanced Conveyors) ===")

    # ================= 61. 初级手摇磨粉工位 =================
    b61 = [
        (0, 0, 0, "dispenser", 0, 180),
        (-1, 0, 0, "lightning_rod", 90, 90),
        (-2, 0, 0, "lever", 0, 90),
        (0, 0, 1, "barrel")
    ]
    img61 = render_scene(b61, scale=4.2)
    l61 = [
        {
            'title': "第 1 层 (Y=1 地面机械动力装配)",
            'note': "手摇曲柄同轴连接传动轴，驱动石磨，出料端置桶",
            'grid': [
                [ None, None, ('barrel_top', '出料桶', (34, 197, 94, 255)) ],
                [ ('lever', '手摇曲柄', (234, 179, 8, 255)), ('lightning_rod', '传动轴', (249, 115, 22, 255)), ('dispenser_front', '石磨磨坊', (239, 68, 68, 255)) ]
            ]
        }
    ]
    m61 = [
        "【石磨磨坊】× 1（坚硬研磨凹槽，矿石资源利用率翻倍）",
        "【手摇曲柄】× 1（初期纯人力旋转动力源，零燃料消耗）",
        "【传动轴】× 1（将旋转动能同轴无损传递至石磨）",
        "【储物木桶】× 1（承接研磨产出的双倍矿石粉末）"
    ]
    ann61 = [
        {
            'rel_pos': (0.16, 0.58), 'card_x': 1140, 'card_y': 220, 'color': (234, 179, 8),
            'title': "【手摇曲柄动力源】", 'lines': ["持续右键摇动曲柄，输出 16 转速的旋转动能", "开荒初期无需电力与蒸汽，纯手动驱动磨坊运转"]
        },
        {
            'rel_pos': (0.42, 0.52), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【同轴直线传动轴】", 'lines': ["同向直线延伸动力，不产生转速损耗与动能衰减", "可配合大齿轮带小齿轮实现两倍快速提速"]
        },
        {
            'rel_pos': (0.76, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (239, 68, 68),
            'title': "【石磨磨坊与出料】", 'lines': ["空手右键投入生铁矿或生铜矿开始高速研磨", "单块生矿研磨产出两份矿粉，矿物利用率直接翻倍"]
        }
    ]
    compose_blueprint(img61, os.path.join(OUT_DIR, "starter-millstone-setup.png"), "初级手摇磨粉工位蓝图 (Starter Millstone & Crank)", l61, m61, ann61)

    # ================= 62. 工业电网电缆布线规范 =================
    b62 = [
        (0, 0, 0, "furnace_on", 0, 180),
        (1, 0, 0, "redstone_block"),
        (2, 0, 0, "redstone_block"),
        (3, 0, 0, "copper_block"),
        (4, 0, 0, "iron_block"),
        (2, 1, 0, "chain"),
        (2, 2, 0, "chain"),
        (2, 2, 1, "dispenser", -90, 0)
    ]
    img62 = render_scene(b62, scale=3.6)
    l62 = [
        {
            'title': "第 1 层 (Y=1 地面铺设电网与储能)",
            'note': "发电机产电，地面平铺电缆连接储能箱与传送带支架",
            'grid': [
                [ ('furnace_front_on', '发电机', (239, 68, 68, 255)), ('redstone_block', '地面电缆', (234, 179, 8, 255)), ('redstone_block', '地面电缆', (234, 179, 8, 255)), ('copper_block', '储能箱', (56, 189, 248, 255)), ('iron_block', '用电设备', (34, 197, 94, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 竖直电缆爬墙立线)",
            'note': "在地面电缆上方垂直延伸，跨越高度差",
            'grid': [
                [ None, None, ('chain', '竖直电缆', (234, 179, 8, 255)), None, None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 高位悬挂工作母机)",
            'note': "竖直电缆穿透楼板直连二层用电机台",
            'grid': [
                [ None, None, ('chain', '竖直电缆', (234, 179, 8, 255)), None, None ],
                [ None, None, ('dispenser_front', '悬挂机床', (239, 68, 68, 255)), None, None ]
            ]
        }
    ]
    m62 = [
        "【燃煤发电机】× 1（消耗煤炭产电，工业电网源泉）",
        "【地面电缆】× 2（红石线形态平铺地面，无损导电）",
        "【竖直电缆】× 2（铁链构型，垂直攀爬墙面跨楼层供电）",
        "【工业储能方块】× 1（缓冲蓄存富余电能，防断电停机）",
        "【用电设备】× 2（传送带支架、顶置机床接入即转）"
    ]
    ann62 = [
        {
            'rel_pos': (0.16, 0.65), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【发电机组发电输出】", 'lines': ["右键投入燃料持续产电，侧面紧密贴合即直连电网", "亦可通过电缆向全厂数十米外的各个车间集中输电"]
        },
        {
            'rel_pos': (0.45, 0.68), 'card_x': 1140, 'card_y': 340, 'color': (234, 179, 8),
            'title': "【地面与竖直电缆布线】", 'lines': ["地面电缆像红石粉一样平铺地表，挖掉即切断", "竖直电缆上下堆叠延伸，专用于穿透楼板与跨层攀爬"]
        },
        {
            'rel_pos': (0.75, 0.62), 'card_x': 1140, 'card_y': 480, 'color': (56, 189, 248),
            'title': "【储能缓冲与用电设备】", 'lines': ["电网全域自动均分电能，储能箱优先吸纳富余电力", "用电设备贴脸或接线即可通电，实现全厂电力自动化"]
        }
    ]
    compose_blueprint(img62, os.path.join(OUT_DIR, "power-cable-wiring-setup.png"), "工业电网电缆布线蓝图 (Power Cable Wiring Setup)", l62, m62, ann62)

    # ================= 63. 悬挂式物品分流器 =================
    b63 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "stone_slab_top"),
        (3, 0, 0, "iron_block"),
        (1, 1, 0, "observer", 0, 180),
        (1, 0, 1, "stone_slab_top"),
        (1, 0, 2, "iron_block"),
        (0, 0, -1, "redstone_block")
    ]
    img63 = render_scene(b63, scale=3.6)
    l63 = [
        {
            'title': "第 1 层 (Y=1 主干传送带与侧翼支线)",
            'note': "主干带面平整连续贯穿，交汇点引出侧翼支线带",
            'grid': [
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None, None ],
                [ ('iron_block', '主线起点', (239, 68, 68, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('iron_block', '主线终点', (34, 197, 94, 255)) ],
                [ None, ('stone', '支线带', (56, 189, 248, 255)), None, None ],
                [ None, ('iron_block', '支线终点', (34, 197, 94, 255)), None, None ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 悬挂式物品分流器)",
            'note': "分流器悬空架设于交汇半砖正上方第 1 格高度",
            'grid': [
                [ None, None, None, None ],
                [ None, ('observer_front', '分流器', (239, 68, 68, 255)), None, None ],
                [ None, None, None, None ],
                [ None, None, None, None ]
            ]
        }
    ]
    m63 = [
        "【悬挂式分流器】× 1（悬空架设于带面上方，右键配置幽灵白名单）",
        "【传送带支架】× 3（主线进出端与侧翼支线出料支架）",
        "【传送带半砖】× 3（上半砖连续铺设，形成主支交汇节点）",
        "【供电线路】× 1（接入电网提供 2 能量/秒）"
    ]
    ann63 = [
        {
            'rel_pos': (0.38, 0.36), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【悬挂式物品分流器】", 'lines': ["悬空安装在半砖上方第 1 格，玩家朝向决定分流方向", "手持物品右键设置幽灵白名单，手持扳手可旋转朝向"]
        },
        {
            'rel_pos': (0.65, 0.60), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【主干连续直通线】", 'lines': ["非白名单内的普通物料不受任何干扰", "沿着主干传送带保持原速平稳向前滑行"]
        },
        {
            'rel_pos': (0.42, 0.78), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【侧翼分选支线】", 'lines': ["符合过滤规则的目标工件被自动剥离推入支线", "直接导向特种加工车间或高阶物料仓库"]
        }
    ]
    compose_blueprint(img63, os.path.join(OUT_DIR, "conveyor-splitter-filter-setup.png"), "悬挂式物品分流器蓝图 (Conveyor Splitter Setup)", l63, m63, ann63)

    # ================= 64. 传送带隧道加速装配 =================
    b64 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "stone_slab_top"),
        (3, 0, 0, "stone_slab_top"),
        (4, 0, 0, "iron_block"),
        (1, 1, 0, "andesite"),
        (2, 1, 0, "andesite"),
        (3, 1, 0, "andesite"),
        (0, 0, 1, "redstone_block")
    ]
    img64 = render_scene(b64, scale=3.6)
    l64 = [
        {
            'title': "第 1 层 (Y=1 连续传送带跑道)",
            'note': "两端驱动支架，中间紧密平铺上半砖",
            'grid': [
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None, None, None ],
                [ ('iron_block', '起点支架', (239, 68, 68, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('iron_block', '终点支架', (34, 197, 94, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 扣盖式传送带隧道)",
            'note': "隧道直接扣盖在传送带半砖正上方",
            'grid': [
                [ None, None, None, None, None ],
                [ None, ('andesite', '隧道外壳', (56, 189, 248, 255)), ('andesite', '隧道外壳', (56, 189, 248, 255)), ('andesite', '隧道外壳', (56, 189, 248, 255)), None ]
            ]
        }
    ]
    m64 = [
        "【传送带隧道】× 3（直接扣盖在带面上方，形成全封闭气道）",
        "【传送带支架】× 2（流水线两端驱动与出料支架）",
        "【传送带半砖】× 3（两支架间紧密平铺的上半砖跑道）",
        "【供电线路】× 1（接入电网提供 2 能量/秒）"
    ]
    ann64 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【扣盖式传送带隧道】", 'lines': ["将传送带隧道直接扣盖在传送带半砖的正上方", "可连续多格拼接，自动咬合为全封闭高速输送廊道"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (34, 197, 94),
            'title': "【50% 气流加速推进】", 'lines': ["隧道内部产生聚束气流，物料滑行速度额外提升 50%", "完全不增加任何系统耗电，跨车间长途运输首选"]
        },
        {
            'rel_pos': (0.20, 0.60), 'card_x': 1140, 'card_y': 500, 'color': (239, 68, 68),
            'title': "【恶劣天气防护】", 'lines': ["全封闭防护雨雪侵蚀与强气流干扰", "杜绝带面上轻量工件弹跳散落或被玩家误捡"]
        }
    ]
    compose_blueprint(img64, os.path.join(OUT_DIR, "conveyor-tunnel-acceleration.png"), "传送带隧道加速装配蓝图 (Conveyor Tunnel Setup)", l64, m64, ann64)

    # ================= 65. 顶置在线加工流水线 =================
    b65 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "stone_slab_top"),
        (3, 0, 0, "stone_slab_top"),
        (4, 0, 0, "iron_block"),
        (1, 1, 0, "piston", -90, 0),
        (2, 1, 0, "dispenser", -90, 0),
        (3, 1, 0, "hopper", 0, 0),
        (0, 0, 1, "redstone_block"),
        (1, 1, -1, "lightning_rod", 0, 0),
        (2, 1, -1, "redstone_block"),
        (3, 1, -1, "glass")
    ]
    img65 = render_scene(b65, scale=3.5)
    l65 = [
        {
            'title': "第 1 层 (Y=1 完整连续传送带跑道)",
            'note': "传送带支架到支架完整连续，严禁在带面插入机器打断",
            'grid': [
                [ None, None, None, None, None ],
                [ ('iron_block', '入料支架', (239, 68, 68, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('iron_block', '出料支架', (34, 197, 94, 255)) ],
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None, None, None ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶置机组与动电管网)",
            'note': "冲压机、拉丝机、注液器直接架设于带面上方，后方接管网",
            'grid': [
                [ None, ('lightning_rod', '传动轴', (249, 115, 22, 255)), ('redstone_block', '电缆', (234, 179, 8, 255)), ('glass', '流体管', (56, 189, 248, 255)), None ],
                [ None, ('piston_top', '动力冲压', (239, 68, 68, 255)), ('dispenser_front', '金属拉丝', (234, 179, 8, 255)), ('hopper_top', '注液喷头', (56, 189, 248, 255)), None ],
                [ None, None, None, None, None ]
            ]
        }
    ]
    m65 = [
        "【连续传送带跑道】× 1（两端支架 + 3 格上半砖，完整贯通不中断）",
        "【顶置动力冲压机】× 1（机头朝下，将金属锭原位重压延展为板材）",
        "【顶置金属拉丝机】× 1（机头朝下，将金属板原位快速拉制为导线）",
        "【顶置注液喷头】× 1（机头朝下，为工件在线自动注入保护润滑药剂）",
        "【动力与管网线路】× 3（后侧隐蔽接入旋转应力、工业电缆与流体管道）"
    ]
    ann65 = [
        {
            'rel_pos': (0.32, 0.42), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【顶置多工序加工机】", 'lines': ["机器紧贴悬空架设于传送带半砖上方第 1 格", "工件随传送带滑至机台下方时自动暂停加工，完成后自动放行"]
        },
        {
            'rel_pos': (0.16, 0.65), 'card_x': 1140, 'card_y': 350, 'color': (148, 163, 184),
            'title': "【连续无间断传送带】", 'lines': ["传送带自起点至终点保持完整连续，严禁插块截断", "多道工序在同一条传送带上无缝贯通连续完成"]
        },
        {
            'rel_pos': (0.75, 0.50), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【无人值守流水线】", 'lines': ["锭材入线、原位冲板、在线拉丝、自动注液一气呵成", "终点直接收获高精密成品构件，实现真正现代化工厂"]
        }
    ]
    compose_blueprint(img65, os.path.join(OUT_DIR, "inline-processing-assembly-line.png"), "顶置在线加工流水线蓝图 (Inline Processing Assembly)", l65, m65, ann65)

    print("Batch 4 blueprints successfully generated!")

if __name__ == "__main__":
    generate_batch4()
