import os
from .rasterizer import render_scene
from .composer import compose_blueprint

OUT_DIR = "/home/nightwind/workspace/zobyic-wiki/docs/public/images/ztech"

def generate_batch2():
    print("=== Generating Blueprints Batch 2 (Scenes 21-40) ===")

    # 21. 金属拉丝机工作站
    b21 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "stone_slab_top"),
        (3, 0, 0, "iron_block"),
        (1, 1, 0, "dispenser", -90, 0),
        (1, 1, -1, "redstone_block")
    ]
    img21 = render_scene(b21, scale=3.8)
    l21 = [
        {
            'title': "第 1 层 (Y=1 连续传送带跑道)",
            'note': "两端驱动支架，上半砖带面平整连续穿过机台下方",
            'grid': [
                [ ('iron_block', '起点支架', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('iron_block', '终点支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶置拉丝机与电网)",
            'note': "拉丝机架设在传送带半砖上方，后方接电网",
            'grid': [
                [ None, ('redstone_block', '电网', (234, 179, 8, 255)), None, None ],
                [ None, ('dispenser_front', '拉丝机', (239, 68, 68, 255)), None, None ]
            ]
        }
    ]
    m21 = [
        "【金属拉丝机】× 1（架设于传送带半砖上方，顶置在线拉丝）",
        "【传送带支架】× 2（流水线两端驱动支架）",
        "【传送带半砖】× 2（带面平整连续贯穿机台正下方）",
        "【供电线路】× 1（接入电网提供 2 能量/秒）"
    ]
    ann21 = [
        {
            'rel_pos': (0.42, 0.40), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【顶置金属拉丝机】", 'lines': ["直接贴合架设于传送带半砖上方", "铜板在带面上经过时在线拉丝为铜线，传送带不中断"]
        },
        {
            'rel_pos': (0.24, 0.65), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【连续传送带跑道】", 'lines': ["传送带自起点至终点平整贯通", "原料与成品在线流转，无需破坏输送线"]
        },
        {
            'rel_pos': (0.65, 0.35), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【供电接口】", 'lines': ["接入工业电网，仅消耗 2 能量/秒", "全天候无人值守连续运转"]
        }
    ]
    compose_blueprint(img21, os.path.join(OUT_DIR, "wiremill-station.png"), "金属拉丝机工作站蓝图 (Wiremill Station)", l21, m21, ann21)

    # 22. 工业搅拌机与搅拌盆
    b22 = [
        (1, 0, 1, "dispenser", 0, 0),
        (0, 0, 1, "glass"),
        (1, 1, 0, "andesite"), (1, 2, 0, "andesite"),
        (1, 2, 1, "dispenser", -90, 0),
        (1, 3, 1, "lightning_rod", 0, 0)
    ]
    img22 = render_scene(b22, scale=3.8)
    l22 = [
        {
            'title': "第 1 层 (Y=1 搅拌盆与注液管网)",
            'note': "中心放置耐腐蚀搅拌盆，侧面接入流体管道",
            'grid': [
                [ ('glass', '注液管', (56, 189, 248, 255)), ('dispenser_front', '搅拌盆', (249, 115, 22, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 反应空腔与机架立柱)",
            'note': "预留 1 格空间供物料反应与叶片旋转，后方立柱支撑",
            'grid': [
                [ None, ('andesite', '机架立柱', (148, 163, 184, 255)) ],
                [ None, None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 动力搅拌机与机架)",
            'note': "动力搅拌机机头垂直朝下，后方机架固定",
            'grid': [
                [ None, ('andesite', '机架立柱', (148, 163, 184, 255)) ],
                [ None, ('dispenser_front', '搅拌机', (239, 68, 68, 255)) ]
            ]
        },
        {
            'title': "第 4 层 (Y=4 垂直动力传动轴)",
            'note': "传动轴由顶部垂直接入搅拌机",
            'grid': [
                [ None, None ],
                [ None, ('lightning_rod', '传动轴', (234, 179, 8, 255)) ]
            ]
        }
    ]
    m22 = [
        "【动力搅拌机】× 1（悬空安装在搅拌盆上方，机头垂直向下）",
        "【耐腐蚀搅拌盆】× 1（底层承载干湿混合物料的深盆）",
        "【动力传动轴】× 1（顶部垂直接入旋转应力驱动叶片）",
        "【流体管道】× 1（侧面注液管网，支持湿法混合）"
    ]
    ann22 = [
        {
            'rel_pos': (0.50, 0.32), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【动力搅拌机】", 'lines': ["悬空安装于搅拌盆正上方，机头垂直朝下", "带动十字搅拌叶片飞速回转"]
        },
        {
            'rel_pos': (0.50, 0.68), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【耐腐蚀搅拌盆】", 'lines': ["承载干湿混合物料，快速均匀干混", "铁粉混合调制产出双倍高活性合金粉"]
        },
        {
            'rel_pos': (0.50, 0.12), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【垂直动力轴】", 'lines': ["传动轴由顶部立式接入搅拌机", "转速越高，混料反应越迅速"]
        }
    ]
    compose_blueprint(img22, os.path.join(OUT_DIR, "mixer-station.png"), "动力搅拌机与搅拌盆蓝图 (Mechanical Mixer Setup)", l22, m22, ann22)

    # 23. 工业离心机提纯台
    b23 = [
        (0, 0, 0, "hopper", 0, 0),
        (0, 1, 0, "dispenser", 0, 180),
        (0, 1, -1, "redstone_block"),
        (1, 1, 0, "barrel")
    ]
    img23 = render_scene(b23, scale=4.0)
    l23 = [
        {
            'title': "第 1 层 (Y=1 离心机台与出料料箱)",
            'note': "中置离心机，侧面放料箱，后方接电网",
            'grid': [
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None ],
                [ ('dispenser_front', '离心机', (239, 68, 68, 255)), ('barrel_top', '成品箱', (34, 197, 94, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶部进料漏斗)",
            'note': "漏斗对准离心仓顶盖",
            'grid': [
                [ None, None ],
                [ ('hopper_outside', '进料斗', (56, 189, 248, 255)), None ]
            ]
        }
    ]
    m23 = [
        "【工业离心机】× 1（高速离心提纯核心机）",
        "【进料漏斗】× 1（顶部注入待提纯矿粉）",
        "【成品收集箱】× 1（暂存提纯出的高纯金属锭）",
        "【供电线路】× 1（接入工业电网提供 6 能量/秒）"
    ]
    ann23 = [
        {
            'rel_pos': (0.42, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【工业离心机】", 'lines': ["高速旋转分离仓，利用离心力提纯", "将矿粉直接精炼为金属锭并分离副产物"]
        },
        {
            'rel_pos': (0.42, 0.18), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【进料漏斗】", 'lines': ["顶部连续下料，将粗矿粉送入离心仓", "支持与自动化流水线无缝对接"]
        },
        {
            'rel_pos': (0.75, 0.58), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【成品料箱】", 'lines': ["侧面自动导出高纯金属锭", "离心分离产物即时归仓"]
        }
    ]
    compose_blueprint(img23, os.path.join(OUT_DIR, "centrifuge-station.png"), "工业离心机提纯台蓝图 (Centrifuge Station)", l23, m23, ann23)

    # 24. 工业洗矿机供水工作台
    b24 = [
        (0, 0, 0, "barrel"),
        (0, 1, 0, "dispenser", 0, 180),
        (-1, 1, 0, "glass"),
        (0, 1, -1, "redstone_block"),
        (0, 2, 0, "hopper", 0, 0)
    ]
    img24 = render_scene(b24, scale=3.8)
    l24 = [
        {
            'title': "第 1 层 (Y=1 底部收集料箱)",
            'note': "暂存洗净矿粉与微量贵金属",
            'grid': [
                [ None, ('barrel_top', '收集箱', (34, 197, 94, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 洗矿机台、管网与电网)",
            'note': "中置洗矿机，左接供水管，后接电缆",
            'grid': [
                [ None, ('redstone_block', '电网', (234, 179, 8, 255)) ],
                [ ('glass', '供水管', (56, 189, 248, 255)), ('dispenser_front', '洗矿机', (239, 68, 68, 255)) ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 顶部投入漏斗)",
            'note': "漏斗对准进矿口连续喂料",
            'grid': [
                [ None, None ],
                [ None, ('hopper_outside', '进料斗', (148, 163, 184, 255)) ]
            ]
        }
    ]
    m24 = [
        "【工业洗矿机】× 1（表面洗选脱泥核心机台）",
        "【流体管道】× 1（侧面直供加压清洁水源）",
        "【进料漏斗】× 1（顶部投入待清洗粗矿粉）",
        "【供电线路】× 1（接入电网提供 4 能量/秒）"
    ]
    ann24 = [
        {
            'rel_pos': (0.50, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【工业洗矿机】", 'lines': ["高压水流冲刷脱泥，消除矿粉杂质", "显著提升后续冶炼纯度与金属产率"]
        },
        {
            'rel_pos': (0.28, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【加压供水管】", 'lines': ["侧向通入持续水压，杜绝断水干洗", "清洁水幕彻底冲刷原矿表面泥垢"]
        },
        {
            'rel_pos': (0.50, 0.78), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【底部收集箱】", 'lines': ["承接洗净矿粉与微量贵金属副产物", "出矿率提高 50% 以上"]
        }
    ]
    compose_blueprint(img24, os.path.join(OUT_DIR, "ore-washer-station.png"), "工业洗矿机工作台蓝图 (Ore Washer Station)", l24, m24, ann24)

    # 25. 自动打包机工作站
    b25 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "stone_slab_top"),
        (3, 0, 0, "iron_block"),
        (1, 1, 0, "dispenser", -90, 0),
        (1, 1, -1, "redstone_block")
    ]
    img25 = render_scene(b25, scale=3.8)
    l25 = [
        {
            'title': "第 1 层 (Y=1 连续传送带跑道)",
            'note': "两端驱动支架，上半砖传送带平整连续穿过机台正下方",
            'grid': [
                [ ('iron_block', '起点支架', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('iron_block', '终点支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶置打包机与电网)",
            'note': "打包机架设在传送带半砖上方，后方接电网",
            'grid': [
                [ None, ('redstone_block', '电网', (234, 179, 8, 255)), None, None ],
                [ None, ('dispenser_front', '打包机', (239, 68, 68, 255)), None, None ]
            ]
        }
    ]
    m25 = [
        "【自动打包机】× 1（架设于传送带半砖上方，顶置在线压缩打包）",
        "【传送带支架】× 2（流水线两端驱动支架）",
        "【传送带半砖】× 2（带面平整连续贯穿机台正下方）",
        "【供电线路】× 1（接入工业电网提供 2 能量/秒）"
    ]
    ann25 = [
        {
            'rel_pos': (0.42, 0.40), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【顶置自动打包机】", 'lines': ["直接贴合架设于传送带半砖上方", "将 9 块金属锭在线压制为包装块，传送带不中断"]
        },
        {
            'rel_pos': (0.24, 0.65), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【连续传送带】", 'lines': ["传送带自起点至终点平整贯通", "零散矿锭进料与大宗包装块出料无缝衔接"]
        },
        {
            'rel_pos': (0.65, 0.35), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【供电接口】", 'lines': ["接入工业电网，仅消耗 2 能量/秒", "全自动免人工打捆装箱"]
        }
    ]
    compose_blueprint(img25, os.path.join(OUT_DIR, "packager-station.png"), "自动打包机工作站蓝图 (Packager Station)", l25, m25, ann25)

    # 26. 工业结晶器长晶槽
    b26 = [
        (0, 0, 0, "dispenser", 0, 180),
        (1, 0, 0, "barrel"),
        (0, 0, -1, "glass"),
        (0, 1, 0, "redstone_block")
    ]
    img26 = render_scene(b26, scale=4.0)
    l26 = [
        {
            'title': "第 1 层 (Y=1 结晶槽、供液管与料箱)",
            'note': "中置结晶槽，后接母液管，侧放料箱",
            'grid': [
                [ ('glass', '母液管', (56, 189, 248, 255)), None ],
                [ ('dispenser_front', '结晶槽', (239, 68, 68, 255)), ('barrel_top', '成品箱', (34, 197, 94, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 控温供电层)",
            'note': "上方接入工业电网维持恒温",
            'grid': [
                [ None, None ],
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None ]
            ]
        }
    ]
    m26 = [
        "【工业结晶器】× 1（恒温结晶反应生长槽）",
        "【流体管道】× 1（注入饱和金属母液）",
        "【成品收集箱】× 1（暂存长成的高纯单晶晶体）",
        "【供电线路】× 1（接入电网提供 4 能量/秒精密控温）"
    ]
    ann26 = [
        {
            'rel_pos': (0.42, 0.55), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【工业结晶器】", 'lines': ["精密控温缓慢析出，培养单晶体", "将洗净矿粉长成高级电路必备的高纯晶体"]
        },
        {
            'rel_pos': (0.35, 0.32), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【饱和母液管】", 'lines': ["后方管道直连化学溶池供给母液", "维持结晶槽内高浓度饱和状态"]
        },
        {
            'rel_pos': (0.75, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【单晶料箱】", 'lines': ["自动收集长成的高纯金属晶体", "供精密微件与传感器制造"]
        }
    ]
    compose_blueprint(img26, os.path.join(OUT_DIR, "crystallizer-station.png"), "工业结晶器长晶槽蓝图 (Crystallizer Station)", l26, m26, ann26)

    # 27. 自动灌装机工作站
    b27 = [
        (0, 0, 0, "brewing_stand"),
        (-1, 0, 0, "glass"),
        (1, 0, 0, "barrel"),
        (0, 0, -1, "hopper", 0, 0)
    ]
    img27 = render_scene(b27, scale=4.0)
    l27 = [{
        'title': "第 1 层 (Y=1 灌装机台与容器进出线)",
        'note': "中置灌装机，后方进空桶，左侧通水，右侧出成品",
        'grid': [
            [ None, ('hopper_outside', '空容器斗', (148, 163, 184, 255)), None ],
            [ ('glass', '供水管', (56, 189, 248, 255)), ('brewing_stand', '灌装机', (239, 68, 68, 255)), ('barrel_top', '成品箱', (34, 197, 94, 255)) ]
        ]
    }]
    m27 = [
        "【自动灌装机】× 1（容器自动注水与药剂灌装）",
        "【流体管道】× 1（后置直连蓄水池供水）",
        "【原料漏斗】× 1（投入待灌装空桶或空玻璃瓶）",
        "【成品料箱】× 1（承接灌装完成的水桶或水瓶）"
    ]
    ann27 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【自动灌装机】", 'lines': ["空瓶进水瓶出，空桶进水桶出", "自动定量灌注液体，彻底免除手动挥桶"]
        },
        {
            'rel_pos': (0.24, 0.65), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【直供水管道】", 'lines': ["管道直连水泵或多方块液体储罐", "充沛水压保障灌装作业零卡顿"]
        },
        {
            'rel_pos': (0.75, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【灌装成品箱】", 'lines': ["灌装完成的容器自动推进收集箱", "直接供应车间注液或蒸汽补水"]
        }
    ]
    compose_blueprint(img27, os.path.join(OUT_DIR, "bottling-machine-station.png"), "自动灌装机工作站蓝图 (Bottling Station)", l27, m27, ann27)

    # 28. 石磨磨坊工作站
    b28 = [
        (0, 0, 0, "dispenser", 0, 180),
        (0, 1, 0, "lightning_rod", 0, 0),
        (1, 0, 0, "hopper", 0, 0)
    ]
    img28 = render_scene(b28, scale=4.0)
    l28 = [
        {
            'title': "第 1 层 (Y=1 磨坊基座与出料漏斗)",
            'note': "中置石磨，侧面接出料漏斗",
            'grid': [
                [ ('dispenser_front', '石磨磨坊', (239, 68, 68, 255)), ('hopper_outside', '出料斗', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 垂直动力轴)",
            'note': "顶部接入旋转机械动力",
            'grid': [
                [ ('lightning_rod', '垂直轴', (249, 115, 22, 255)), None ]
            ]
        }
    ]
    m28 = [
        "【石磨磨坊】× 1（小型旋转磨坊，接入应力运转）",
        "【垂直传动轴】× 1（顶面垂直输入 16~32 转/分动能）",
        "【出料漏斗】× 1（导出碾磨后的精细石料或骨粉）"
    ]
    ann28 = [
        {
            'rel_pos': (0.42, 0.58), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【石磨磨坊】", 'lines': ["上下研磨盘相向摩擦粉碎物料", "圆石碾为砂砾再碾为燧石，骨头磨成4倍骨粉"]
        },
        {
            'rel_pos': (0.42, 0.28), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【垂直动力轴】", 'lines': ["顶部插接垂直转轴直通水车或齿轮箱", "仅需 32 应力单位即可驱动运转"]
        },
        {
            'rel_pos': (0.75, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【出料漏斗】", 'lines': ["研磨碎屑自动由底部或侧面滑出", "开荒期实现稳定矿物初级增产"]
        }
    ]
    compose_blueprint(img28, os.path.join(OUT_DIR, "millstone-station.png"), "石磨磨坊工作站蓝图 (Millstone Station)", l28, m28, ann28)

    # 29. 机械压榨机工位
    b29 = [
        (0, 0, 0, "polished_andesite"),
        (0, 1, 0, "polished_andesite_slab"),
        (0, 3, 0, "dispenser", 180, 0),
        (0, 3, 1, "lightning_rod", 90, 0)
    ]
    img29 = render_scene(b29, scale=3.6)
    l29 = [
        {
            'title': "第 1 层 (Y=1 地基基座)",
            'note': "安山岩稳固承重地面",
            'grid': [ [ ('polished_andesite', '基座', (148, 163, 184, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 置物工位)",
            'note': "平放置物台承托工件",
            'grid': [ [ ('polished_andesite', '置物台', (56, 189, 248, 255)) ] ]
        },
        {
            'title': "第 3 层 (Y=3 空腔层)",
            'note': "预留 1 格空间供冲头下砸",
            'grid': [ [ None ] ]
        },
        {
            'title': "第 4 层 (Y=4 机械压榨机头)",
            'note': "压榨机机头朝下，侧接动力轴",
            'grid': [ [ ('dispenser_front', '压榨机', (239, 68, 68, 255)) ] ]
        }
    ]
    m29 = [
        "【机械压榨机】× 1（悬空安装在上方第 2 格，机头朝下）",
        "【安山岩置物台】× 1（底层承托工件，防弹跳吸附）",
        "【动力传动轴】× 1（侧面注入旋转应力）"
    ]
    ann29 = [
        {
            'rel_pos': (0.50, 0.22), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【机械压榨机】", 'lines': ["纯机械凸轮带动重锤往复下砸", "金属锭放置于下方台面时凌空重砸压延成板"]
        },
        {
            'rel_pos': (0.50, 0.65), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【安山置物台】", 'lines': ["原料平稳静置于台面正中央", "重锤砸下瞬间成型为金属板材"]
        },
        {
            'rel_pos': (0.65, 0.18), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【动力输入轴】", 'lines': ["消耗 64 应力单位旋转动能", "转速越高，重锤下砸节拍越快"]
        }
    ]
    compose_blueprint(img29, os.path.join(OUT_DIR, "stress-press-station.png"), "机械压榨机工位蓝图 (Mechanical Press Setup)", l29, m29, ann29)

    # 30. 动力耕地犁工作站
    b30 = [
        (0, 0, 0, "farmland"), (1, 0, 0, "farmland"), (-1, 0, 0, "farmland"),
        (0, 0, 1, "polished_andesite"),
        (0, 0, 2, "lightning_rod", 90, 0)
    ]
    img30 = render_scene(b30, scale=3.6)
    l30 = [{
        'title': "第 1 层 (Y=1 动力犁与翻松农田)",
        'note': "刀刃向前平推，后方接入推进传动轴",
        'grid': [
            [ ('farmland_moist', '耕地', (34, 197, 94, 255)), ('farmland_moist', '耕地', (34, 197, 94, 255)), ('farmland_moist', '耕地', (34, 197, 94, 255)) ],
            [ None, ('polished_andesite', '动力犁', (239, 68, 68, 255)), None ],
            [ None, ('lightning_rod', '传动轴', (249, 115, 22, 255)), None ]
        ]
    }]
    m30 = [
        "【动力犁】× 1（合金刀刃朝前，应力驱动自动翻土）",
        "【推进传动轴】× 1（输入旋转应力驱动刀刃持续平推）",
        "【平整耕地】× 3（面前草地或泥土自动翻松为肥沃耕地）"
    ]
    ann30 = [
        {
            'rel_pos': (0.50, 0.48), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【动力犁】", 'lines': ["合金犁刃持续向前平推翻耕", "面前 5×5 范围草地/泥土瞬间翻松为肥沃耕地"]
        },
        {
            'rel_pos': (0.50, 0.72), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【推进传动轴】", 'lines': ["直连机械转轴，仅消耗 64 应力单位", "免除人工挥锄的大量体力消耗"]
        },
        {
            'rel_pos': (0.28, 0.35), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【翻松耕地】", 'lines': ["土壤均匀松软保水", "随时可补种小麦、胡萝卜等各类农作物"]
        }
    ]
    compose_blueprint(img30, os.path.join(OUT_DIR, "plough-farming-setup.png"), "动力耕地犁工作站蓝图 (Plough Farming Setup)", l30, m30, ann30)

    # 31. 动力活塞推移机构
    b31 = [
        (0, 0, 0, "stone_bricks"), (1, 0, 0, "stone_bricks"), (2, 0, 0, "stone_bricks"), (3, 0, 0, "stone_bricks"),
        (0, 1, 0, "piston", 0, -90),
        (1, 1, 0, "iron_ore"), (2, 1, 0, "iron_ore"),
        (-1, 1, 0, "lightning_rod", 0, 90),
        (0, 1, 1, "redstone_block")
    ]
    img31 = render_scene(b31, scale=3.8)
    l31 = [
        {
            'title': "第 1 层 (Y=1 平整滑轨地基)",
            'note': "平整铺设 4 格石砖作为推移滑轨承重面",
            'grid': [
                [ ('stone_bricks', '滑轨基座', (148, 163, 184, 255)), ('stone_bricks', '滑轨基座', (148, 163, 184, 255)), ('stone_bricks', '滑轨基座', (148, 163, 184, 255)), ('stone_bricks', '滑轨基座', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 活塞、推移方块与传动网络)",
            'note': "活塞面朝前，后接动力轴，侧接红石源",
            'grid': [
                [ None, ('redstone_block', '红石', (234, 179, 8, 255)), None, None ],
                [ ('lightning_rod', '传动轴', (249, 115, 22, 255)), ('piston_top', '动力活塞', (239, 68, 68, 255)), ('iron_ore', '待推矿石', (148, 163, 184, 255)), ('iron_ore', '待推矿石', (148, 163, 184, 255)) ]
            ]
        }
    ]
    m31 = [
        "【动力活塞】× 1（应力驱动，红石脉冲触发平推方块）",
        "【动力传动轴】× 1（后方同轴注入 64 应力单位旋转动能）",
        "【红石信号源】× 1（侧面输入红石信号触发推拉周期）",
        "【平整滑轨】× 4（承托方块整列平稳推移）"
    ]
    ann31 = [
        {
            'rel_pos': (0.35, 0.42), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【动力活塞】", 'lines': ["木质推头朝向前方矿石列，推力强劲平稳", "红石信号触发将面前方块列向外推出 1 格"]
        },
        {
            'rel_pos': (0.18, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【动力传动轴】", 'lines': ["后方直连轴系接入 64 应力单位旋转动能", "为往复机械伸缩提供持续机械源"]
        },
        {
            'rel_pos': (0.42, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【红石触发端】", 'lines': ["连接时钟脉冲或传感器", "黏性动力活塞交替信号可自动推拉往复"]
        }
    ]
    compose_blueprint(img31, os.path.join(OUT_DIR, "piston-pusher-setup.png"), "动力活塞推移机构蓝图 (Mechanical Piston Pusher)", l31, m31, ann31)

    # 32. 土制燃煤发电机房
    b32 = [
        (0, 0, 0, "furnace_on", 0, 180),
        (-1, 0, 0, "hopper", 0, 0),
        (1, 0, 0, "iron_block"),
        (0, 0, 1, "lightning_rod", 0, 0)
    ]
    img32 = render_scene(b32, scale=3.8)
    l32 = [{
        'title': "第 1 层 (Y=1 燃煤发电机、供煤斗与储能电网)",
        'note': "中置发电机，左侧自动供煤，右侧接储能方块，前方出电缆",
        'grid': [
            [ ('hopper_outside', '供煤斗', (148, 163, 184, 255)), ('furnace_front_on', '燃煤机', (239, 68, 68, 255)), ('iron_block', '储能方块', (56, 189, 248, 255)) ],
            [ None, ('lightning_rod', '输电导线', (234, 179, 8, 255)), None ]
        ]
    }]
    m32 = [
        "【土制燃煤发电机】× 1（燃烧固体燃料产出 3 能量/秒）",
        "【进料漏斗】× 1（侧面自动注入固体煤炭或木炭）",
        "【基础储能方块】× 1（蓄存平抑发电机电能波动）",
        "【输电电缆】× 1（向车间工作机无损输送电力）"
    ]
    ann32 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【土制燃煤发电机】", 'lines': ["开荒期主力发电机，仅需燃烧煤炭或木炭", "持续稳定输出 3 能量/秒纯净电能"]
        },
        {
            'rel_pos': (0.24, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【自动供煤漏斗】", 'lines': ["侧面直连漏斗与煤仓", "实现长期免人工值守的自动添煤"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【基础储能方块】", 'lines': ["紧邻发电机并联储能", "储存 100,000 能量单位电力缓冲区"]
        }
    ]
    compose_blueprint(img32, os.path.join(OUT_DIR, "coal-generator-setup.png"), "土制燃煤发电机房蓝图 (Coal Generator Setup)", l32, m32, ann32)

    # 33. 简易蒸汽机工位
    b33 = [
        (0, 0, 0, "furnace_on", 0, 180),
        (-1, 0, 0, "glass"),
        (1, 0, 0, "lightning_rod", 0, 0)
    ]
    img33 = render_scene(b33, scale=4.0)
    l33 = [{
        'title': "第 1 层 (Y=1 简易蒸汽机布局)",
        'note': "左侧通水管，中置蒸汽机，右侧引出电缆",
        'grid': [
            [ ('glass', '补水管', (56, 189, 248, 255)), ('furnace_front_on', '简易蒸汽机', (239, 68, 68, 255)), ('lightning_rod', '电缆', (234, 179, 8, 255)) ]
        ]
    }]
    m33 = [
        "【简易蒸汽机】× 1（消耗燃料与冷水沸腾发电）",
        "【流体管道】× 1（侧面注入冷凝水源）",
        "【输电电缆】× 1（输出 4 能量/秒电力至电网）"
    ]
    ann33 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【简易蒸汽机】", 'lines': ["初级小型热机发电机，内置 8000 能量容量", "消耗燃料与水，蒸汽受热沸腾输出 4 能量/秒"]
        },
        {
            'rel_pos': (0.24, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【冷水补水管】", 'lines': ["侧向通入流体管道供给水源", "确保水汽充足，防止机体干烧停机"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【电网导线】", 'lines': ["将发出的电能导入工厂输电干线", "为初期机床提供稳定电力"]
        }
    ]
    compose_blueprint(img33, os.path.join(OUT_DIR, "simple-steam-setup.png"), "简易蒸汽机工位蓝图 (Simple Steam Engine Setup)", l33, m33, ann33)

    # 34. 生物燃油发电站
    b34 = [
        (0, 0, 0, "furnace_on", 0, 180),
        (0, 1, 0, "hopper", 0, 0),
        (1, 0, 0, "lightning_rod", 0, 0)
    ]
    img34 = render_scene(b34, scale=4.0)
    l34 = [
        {
            'title': "第 1 层 (Y=1 发电机与出电导线)",
            'note': "中置发电机，右侧接电缆",
            'grid': [
                [ ('furnace_front_on', '生物发电机', (239, 68, 68, 255)), ('lightning_rod', '电缆', (234, 179, 8, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶部有机料仓)",
            'note': "漏斗对准燃料口投入海带/树苗",
            'grid': [
                [ ('hopper_outside', '有机进料斗', (34, 197, 94, 255)), None ]
            ]
        }
    ]
    m34 = [
        "【生物燃油发电机】× 1（消耗植物残渣清洁发电 5 能量/秒）",
        "【进料漏斗】× 1（顶部投入干燥海带、种子或树苗）",
        "【输电电缆】× 1（并入车间工业电网）"
    ]
    ann34 = [
        {
            'rel_pos': (0.42, 0.58), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【生物燃油发电机】", 'lines': ["绿色循环电站，不消耗不可再生矿物", "将有机废料催化裂解清洁供电 5 能量/秒"]
        },
        {
            'rel_pos': (0.42, 0.28), 'card_x': 1140, 'card_y': 360, 'color': (34, 197, 94),
            'title': "【有机料仓】", 'lines': ["顶部自动注入海带块、树苗或小麦残渣", "实现农林副产物全量能源化复用"]
        },
        {
            'rel_pos': (0.75, 0.58), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【主网电缆】", 'lines': ["并入厂区电网，形成零碳自循环工区", "夜间亦可持续稳定产电"]
        }
    ]
    compose_blueprint(img34, os.path.join(OUT_DIR, "biofuel-generator-setup.png"), "生物燃油发电站蓝图 (Biofuel Generator Setup)", l34, m34, ann34)

    # 35. 地热温差发电机位
    b35 = [
        (0, 0, 0, "crying_obsidian"),
        (-1, 0, 0, "tinted_glass"),
        (1, 0, 0, "lightning_rod", 0, 0)
    ]
    img35 = render_scene(b35, scale=4.0)
    l35 = [{
        'title': "第 1 层 (Y=1 熔岩热源、发电机与输电线)",
        'note': "紧邻熔岩放置，右侧引出电缆",
        'grid': [
            [ ('tinted_glass', '熔岩热源', (249, 115, 22, 255)), ('crying_obsidian', '地热发电机', (168, 85, 247, 255)), ('lightning_rod', '电缆', (234, 179, 8, 255)) ]
        ]
    }]
    m35 = [
        "【地热温差发电机】× 1（依靠熔岩温差发电 6 能量/秒）",
        "【高温熔岩源】× 1（侧面紧邻天然岩浆池或下界熔岩海）",
        "【输电电缆】× 1（向矿区无损输送工业电力）"
    ]
    ann35 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (168, 85, 247),
            'title': "【地热发电机】", 'lines': ["耐热合金机壳，内部激发热电温差效应", "持续输出 6 能量/秒纯净电能，零燃料消耗"]
        },
        {
            'rel_pos': (0.24, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【高温熔岩源】", 'lines': ["紧贴静止岩浆方块即可长效激活", "深层矿井与下界基地的绝佳能源方案"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【输电电缆】", 'lines': ["将地底热能发出的电力导出矿坑", "照亮深层自动化采矿流水线"]
        }
    ]
    compose_blueprint(img35, os.path.join(OUT_DIR, "thermal-generator-setup.png"), "地热温差发电机位蓝图 (Thermal Generator Setup)", l35, m35, ann35)

    # 36. 露天太阳能矩阵
    b36 = [
        (0, 0, 0, "daylight_detector"), (1, 0, 0, "daylight_detector"),
        (0, 0, 1, "daylight_detector"), (1, 0, 1, "daylight_detector"),
        (2, 0, 0, "iron_block"),
        (0, 0, -1, "lightning_rod", 90, 0)
    ]
    img36 = render_scene(b36, scale=3.6)
    l36 = [{
        'title': "第 1 层 (Y=1 太阳能板矩阵与储能柜)",
        'note': "2×2 平铺太阳能板，侧接储能柜与电缆",
        'grid': [
            [ None, ('lightning_rod', '主电缆', (234, 179, 8, 255)), None ],
            [ ('daylight_detector_top', '太阳能板', (56, 189, 248, 255)), ('daylight_detector_top', '太阳能板', (56, 189, 248, 255)), ('iron_block', '储能柜', (148, 163, 184, 255)) ],
            [ ('daylight_detector_top', '太阳能板', (56, 189, 248, 255)), ('daylight_detector_top', '太阳能板', (56, 189, 248, 255)), None ]
        ]
    }]
    m36 = [
        "【太阳能板】× 4（每块日照发电 4 能量/秒）",
        "【工业储能方块】× 1（白昼蓄电，供夜间不间断供电）",
        "【输电电缆】× 1（汇流引出高压电力）"
    ]
    ann36 = [
        {
            'rel_pos': (0.42, 0.48), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【太阳能板矩阵】", 'lines': ["露天平铺放置，头顶必须无遮挡方块", "白天晴空每块平稳输出 4 能量/秒清洁电力"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【工业储能柜】", 'lines': ["白昼高效储能，将多余电力充入电池", "夜间无日照时平稳放电维持工厂运转"]
        },
        {
            'rel_pos': (0.42, 0.18), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【主网电缆】", 'lines': ["多路并联汇入输电干线", "实现大面积屋顶绿电自给自足"]
        }
    ]
    compose_blueprint(img36, os.path.join(OUT_DIR, "solar-panel-array.png"), "露天太阳能矩阵蓝图 (Solar Panel Array)", l36, m36, ann36)

    # 37. 立柱高空风力发电塔
    b37 = [
        (0, 0, 0, "iron_block"),
        (0, 1, 0, "lightning_rod", 0, 0),
        (0, 2, 0, "lightning_rod", 0, 0),
        (1, 0, 0, "lightning_rod", 90, 0)
    ]
    img37 = render_scene(b37, scale=3.8)
    l37 = [
        {
            'title': "第 1 层 (Y=1 铁质地面基座与引出线)",
            'note': "中置稳固铁块，侧面引出电网线缆",
            'grid': [
                [ ('iron_block', '铁基座', (148, 163, 184, 255)), ('lightning_rod', '下引线', (234, 179, 8, 255)) ]
            ]
        },
        {
            'title': "第 2~3 层 (Y=2~3 立式高空风电机组)",
            'note': "垂直同轴向上堆叠抬升海拔",
            'grid': [
                [ ('lightning_rod', '立柱发电机', (56, 189, 248, 255)), None ]
            ]
        }
    ]
    m37 = [
        "【高空风力发电机】× 2（搭建海拔越高发电功率越强，2~8 能量/秒）",
        "【稳固承重基座】× 1（平整地面铁块基座）",
        "【输电电缆】× 1（向地面车间无损引下清洁电能）"
    ]
    ann37 = [
        {
            'rel_pos': (0.45, 0.22), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【风力发电机】", 'lines': ["避雷针式立柱气流发电机", "海平面以上每升高一定海拔，发电功率稳步提升"]
        },
        {
            'rel_pos': (0.45, 0.65), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【地面铁基座】", 'lines': ["底层坚固承托高耸塔柱", "抗强风震动，稳固地基"]
        },
        {
            'rel_pos': (0.75, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【下引电缆】", 'lines': ["高空清洁电力顺塔引下", "全天候昼夜发电，不受阴雨限制"]
        }
    ]
    compose_blueprint(img37, os.path.join(OUT_DIR, "wind-turbine-tower.png"), "立柱高空风力发电塔蓝图 (Wind Turbine Tower)", l37, m37, ann37)

    # 38. 工业快速充电站
    b38 = [
        (0, 0, 0, "crafter", 0, 180),
        (0, 0, -1, "redstone_block"),
        (0, 1, 0, "redstone_lamp")
    ]
    img38 = render_scene(b38, scale=4.0)
    l38 = [
        {
            'title': "第 1 层 (Y=1 充电站基座与电网输入)",
            'note': "中置充电站，后方接入工业电网",
            'grid': [
                [ ('redstone_block', '工业电网', (234, 179, 8, 255)) ],
                [ ('crafter_top', '充电站', (239, 68, 68, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 充电状态指示灯)",
            'note': "充电中常亮，空载或缺电熄灭",
            'grid': [
                [ None ],
                [ ('redstone_lamp', '状态灯', (249, 115, 22, 255)) ]
            ]
        }
    ]
    m38 = [
        "【工业充电站】× 1（高压快充，500 能量/秒/槽）",
        "【工业状态灯】× 1（充放电状态实时目视反馈）",
        "【高压供电线路】× 1（接入电网提供充足电能）"
    ]
    ann38 = [
        {
            'rel_pos': (0.50, 0.58), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【工业充电站】", 'lines': ["右键打开放置电池、充电棒或电动工具", "以 500 能量/秒极速满电，彻底告别能量焦虑"]
        },
        {
            'rel_pos': (0.50, 0.28), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【状态指示灯】", 'lines': ["顶置状态指示灯，通电充电时长亮", "直观掌握车间充能工位工作状态"]
        },
        {
            'rel_pos': (0.50, 0.78), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【高压供电线路】", 'lines': ["连接主电网大容量输电线路", "确保大功率突发快充不造成电网跳闸"]
        }
    ]
    compose_blueprint(img38, os.path.join(OUT_DIR, "charging-station-setup.png"), "工业快速充电站蓝图 (Charging Station Setup)", l38, m38, ann38)

    # 39. 工业储能方块矩阵
    b39 = [
        (0, 0, 0, "iron_block"), (1, 0, 0, "iron_block"),
        (0, 0, 1, "iron_block"), (1, 0, 1, "iron_block"),
        (0, 1, 0, "redstone_lamp"),
        (1, 0, -1, "lightning_rod", 0, 0)
    ]
    img39 = render_scene(b39, scale=3.6)
    l39 = [
        {
            'title': "第 1 层 (Y=1 2×2 储能方块矩阵与干线)",
            'note': "4 块储能方块紧密并排，侧接输电主干线",
            'grid': [
                [ None, ('lightning_rod', '主干电缆', (234, 179, 8, 255)) ],
                [ ('iron_block', '储能方块', (56, 189, 248, 255)), ('iron_block', '储能方块', (56, 189, 248, 255)) ],
                [ ('iron_block', '储能方块', (56, 189, 248, 255)), ('iron_block', '储能方块', (56, 189, 248, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 矩阵状态指示灯)",
            'note': "监控储能矩阵电量状态",
            'grid': [
                [ None, None ],
                [ ('redstone_lamp', '状态灯', (249, 115, 22, 255)), None ],
                [ None, None ]
            ]
        }
    ]
    m39 = [
        "【工业储能方块】× 4（单格 100,000 ~ 2,000,000 能量单位）",
        "【工业状态灯】× 1（电网供电正常时长亮）",
        "【输电干线电缆】× 1（联通发电机群与用电车间）"
    ]
    ann39 = [
        {
            'rel_pos': (0.45, 0.58), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【储能方块矩阵】", 'lines': ["基础/中型/终极储能方块集群布局", "构建数百万级容量的全厂战略电力蓄水池"]
        },
        {
            'rel_pos': (0.35, 0.28), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【状态指示灯】", 'lines': ["直观监控全网存电状态", "缺电时高频闪烁发出警示"]
        },
        {
            'rel_pos': (0.75, 0.35), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【输电主干电缆】", 'lines': ["双向大电流无损吞吐", "平抑发电机组波动与大功率母机启停脉冲"]
        }
    ]
    compose_blueprint(img39, os.path.join(OUT_DIR, "energy-cube-matrix.png"), "工业储能方块矩阵蓝图 (Energy Cube Matrix)", l39, m39, ann39)

    # 40. 飞轮动量蓄能站
    b40 = [
        (0, 0, 0, "lightning_rod", 90, 90),
        (1, 0, 0, "grindstone"),
        (2, 0, 0, "lightning_rod", 90, 90)
    ]
    img40 = render_scene(b40, scale=4.0)
    l40 = [{
        'title': "第 1 层 (Y=1 飞轮串接轴系流程)",
        'note': "输入轴、大惯量飞轮与输出轴同轴串联",
        'grid': [
            [ ('lightning_rod', '输入轴', (249, 115, 22, 255)), ('grindstone_side', '大飞轮', (239, 68, 68, 255)), ('lightning_rod', '输出轴', (249, 115, 22, 255)) ]
        ]
    }]
    m40 = [
        "【大惯量飞轮】× 1（转速 16 转/分，蓄存 512 应力单位）",
        "【直线传动轴】× 2（贯通输入端与输出端）"
    ]
    ann40 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【大惯量飞轮】", 'lines': ["旋转动量蓄能核心轮，动力源运转时充能", "动力源中断后可持续释放旋转能量约 5 秒"]
        },
        {
            'rel_pos': (0.24, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【输入传动轴】", 'lines': ["同轴接入水车、风车或蒸汽机动力", "平滑动力源带来的脉动冲击"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【输出传动轴】", 'lines': ["为下游重型机床输出平稳转速", "杜绝瞬时负荷突变导致的机械抱死停机"]
        }
    ]
    compose_blueprint(img40, os.path.join(OUT_DIR, "flywheel-buffer-setup.png"), "飞轮动量蓄能站蓝图 (Flywheel Buffer Setup)", l40, m40, ann40)

    # 40_extra. 传送带标准搭法
    b_conv = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "stone_slab_top"),
        (3, 0, 0, "stone_slab_top"),
        (4, 0, 0, "iron_block"),
        (0, 0, 1, "redstone_block")
    ]
    img_conv = render_scene(b_conv, scale=3.8)
    l_conv = [
        {
            'title': "第 1 层 (Y=1 传送带流水线与供电)",
            'note': "两端放置支架，中间紧密铺满上半砖，起点支架接入电网",
            'grid': [
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None, None, None ],
                [ ('iron_block', '起点支架', (239, 68, 68, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('stone', '传送带', (148, 163, 184, 255)), ('iron_block', '终点支架', (34, 197, 94, 255)) ]
            ]
        }
    ]
    m_conv = [
        "【传送带支架】× 2（流水线两端驱动与出料支架）",
        "【传送带半砖】× 3（两支架间紧密平铺的上半砖跑道）",
        "【供电线路】× 1（接入工业电网提供 2 能量/秒）"
    ]
    ann_conv = [
        {
            'rel_pos': (0.18, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【起点驱动支架】", 'lines': ["传送带动力核心，必须接入电网（2 能量/秒）", "放置时的视线朝向即为物料输送方向，空手右键看朝向"]
        },
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【传送带半砖】", 'lines': ["强制放置于方块上半部分（上半砖），带面与支架顶面平齐", "手持物品右键放上带面，空手右键可取回物品"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【终点支架与接驳】", 'lines': ["流水线末端，可直连下一段传送带、料箱或加工机", "手持工业扳手右键支架可一键反转整条线路方向"]
        }
    ]
    compose_blueprint(img_conv, os.path.join(OUT_DIR, "conveyor-standard-setup.png"), "传送带标准搭法蓝图 (Conveyor Belt Standard Setup)", l_conv, m_conv, ann_conv)

    print("Batch 2 blueprints successfully generated!")

if __name__ == "__main__":
    generate_batch2()
