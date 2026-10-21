import os
from .rasterizer import render_scene
from .composer import compose_blueprint

OUT_DIR = "/home/nightwind/workspace/zobyic-wiki/docs/public/images/ztech"

def generate_batch3():
    print("=== Generating Blueprints Batch 3 (Scenes 41-60) ===")

    # 41. 离合器控制台
    b41 = [
        (0, 0, 0, "lightning_rod", 90, 90),
        (1, 0, 0, "repeater_1tick"),
        (2, 0, 0, "lightning_rod", 90, 90),
        (1, 0, 1, "lever")
    ]
    img41 = render_scene(b41, scale=4.0)
    l41 = [{
        'title': "第 1 层 (Y=1 离合器与控制拉杆)",
        'note': "轴系中段嵌入离合器，侧接红石拉杆",
        'grid': [
            [ ('lightning_rod', '输入轴', (249, 115, 22, 255)), ('repeater', '离合器', (239, 68, 68, 255)), ('lightning_rod', '输出轴', (249, 115, 22, 255)) ],
            [ None, ('repeater', '拉杆', (234, 179, 8, 255)), None ]
        ]
    }]
    m41 = [
        "【离合器】× 1（串联在传动轴中段，切换接合与分离）",
        "【直线传动轴】× 2（输入轴与输出轴）",
        "【红石拉杆】× 1（侧面输入控制信号）"
    ]
    ann41 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【离合器】", 'lines': ["串插在动力传动链中段，无需拆除转轴", "右键或红石信号切换接合与分离状态"]
        },
        {
            'rel_pos': (0.48, 0.72), 'card_x': 1140, 'card_y': 360, 'color': (234, 179, 8),
            'title': "【控制拉杆】", 'lines': ["拉杆激活时离合器分离，下游设备瞬间停转", "常用于过载紧急断开或分段检修"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【下游输出轴】", 'lines': ["接合时 1:1 无损传递转速", "分离时平稳停摆，上游动力网不受影响"]
        }
    ]
    compose_blueprint(img41, os.path.join(OUT_DIR, "clutch-control-setup.png"), "离合器传动控制台蓝图 (Clutch Control Setup)", l41, m41, ann41)

    # 42. 穿墙轴承隔断密封
    b42 = [
        (0, 0, 0, "lightning_rod", 90, 90),
        (1, 0, 0, "iron_bars_post"),
        (2, 0, 0, "lightning_rod", 90, 90),
        (1, 1, 0, "stone_bricks"),
        (1, -1, 0, "stone_bricks")
    ]
    img42 = render_scene(b42, scale=3.8)
    l42 = [{
        'title': "第 1 层 (Y=1 隔离墙孔与轴承密封)",
        'note': "墙孔中嵌入穿墙轴承，两侧贯通转轴",
        'grid': [
            [ ('lightning_rod', '室内轴', (249, 115, 22, 255)), ('iron_bars', '穿墙轴承', (56, 189, 248, 255)), ('lightning_rod', '室外轴', (249, 115, 22, 255)) ]
        ]
    }]
    m42 = [
        "【穿墙轴承】× 1（嵌入墙体孔洞，1:1 传递转速）",
        "【石砖隔离墙】× 2（上下完全封闭形成气密隔断）",
        "【直线传动轴】× 2（墙体内外无损对接）"
    ]
    ann42 = [
        {
            'rel_pos': (0.48, 0.48), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【穿墙轴承】", 'lines': ["紧密嵌入墙体或楼板预留孔洞", "维持厂房密封隔绝，杜绝开洞漏气"]
        },
        {
            'rel_pos': (0.48, 0.22), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【隔音隔离墙】", 'lines': ["上下四周由实心建材完全包覆", "将室外嘈杂水车动力安全导入室内"]
        },
        {
            'rel_pos': (0.75, 0.48), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【轴向传动】", 'lines': ["转速 1:1 零摩擦损耗跨墙传输", "工厂多车间动力网标准化穿墙规范"]
        }
    ]
    compose_blueprint(img42, os.path.join(OUT_DIR, "wall-bearing-setup.png"), "穿墙轴承隔断密封蓝图 (Wall Bearing Setup)", l42, m42, ann42)

    # 43. 动力曲柄箱逆变站
    b43 = [
        (0, 0, 0, "redstone_block"),
        (1, 0, 0, "copper_block"),
        (2, 0, 0, "lightning_rod", 90, 90)
    ]
    img43 = render_scene(b43, scale=4.0)
    l43 = [{
        'title': "第 1 层 (Y=1 电网输入、曲柄箱与输出轴)",
        'note': "左接电缆，中置曲柄箱，右接输出转轴",
        'grid': [
            [ ('redstone_block', '电网', (234, 179, 8, 255)), ('copper_block', '曲柄箱', (239, 68, 68, 255)), ('lightning_rod', '输出轴', (249, 115, 22, 255)) ]
        ]
    }]
    m43 = [
        "【动力曲柄箱】× 1（电能转机械能逆变机）",
        "【工业电网电缆】× 1（耗电 10 能量/秒）",
        "【动力传动轴】× 1（输出 32 转/分 · 2048 应力单位）"
    ]
    ann43 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【动力曲柄箱】", 'lines': ["动电互通枢纽：瞬间将工业电力转化为旋转动能", "输出高达 32 转/分与 2048 应力容量"]
        },
        {
            'rel_pos': (0.24, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (234, 179, 8),
            'title': "【工业电网输入】", 'lines': ["接入全厂工业电网供电", "远距离电缆引电，终结超长传动轴困局"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【机械输出轴】", 'lines': ["直驱车床、冲压机与粉碎轮", "实现车间设备电气化改造"]
        }
    ]
    compose_blueprint(img43, os.path.join(OUT_DIR, "power-motor-setup.png"), "动力曲柄箱逆变站蓝图 (Power Motor Setup)", l43, m43, ann43)

    # 44. 仪表监控面板墙
    b44 = [
        (0, 0, 0, "lightning_rod", 90, 90), (1, 0, 0, "lightning_rod", 90, 90), (2, 0, 0, "lightning_rod", 90, 90),
        (0, 1, 0, "quartz_block"),
        (1, 1, 0, "quartz_block"),
        (2, 1, 0, "redstone_lamp")
    ]
    img44 = render_scene(b44, scale=3.8)
    l44 = [
        {
            'title': "第 1 层 (Y=1 底层动力贯通轴)",
            'note': "轴系水平贯通仪表工位",
            'grid': [
                [ ('lightning_rod', '传动轴', (249, 115, 22, 255)), ('lightning_rod', '传动轴', (249, 115, 22, 255)), ('lightning_rod', '传动轴', (249, 115, 22, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 监控仪表与指示灯排)",
            'note': "贴紧转轴安装转速表、应力表与状态灯",
            'grid': [
                [ ('quartz_block_side', '转速表', (56, 189, 248, 255)), ('quartz_block_side', '应力表', (34, 197, 94, 255)), ('redstone_lamp', '状态灯', (234, 179, 8, 255)) ]
            ]
        }
    ]
    m44 = [
        "【转速表】× 1（上方实时悬浮显示每分钟转速）",
        "【应力表】× 1（上方实时悬浮显示应力供需）",
        "【工业状态灯】× 1（机器运转常亮，异常高频闪烁）",
        "【动力传动轴】× 3（主轴贯通承载仪表监测）"
    ]
    ann44 = [
        {
            'rel_pos': (0.32, 0.35), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【转速表】", 'lines': ["贴紧动力轴安装，数字悬浮实时显示", "清晰洞悉当前传动分支每分钟转速"]
        },
        {
            'rel_pos': (0.50, 0.35), 'card_x': 1140, 'card_y': 360, 'color': (34, 197, 94),
            'title': "【应力表】", 'lines': ["显示全网供给总容量与已用负荷", "超载预警一目了然，排查过载必备"]
        },
        {
            'rel_pos': (0.68, 0.35), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【工业状态灯】", 'lines': ["直观反映设备运转工况", "常亮表示健康，闪烁提示供能不足"]
        }
    ]
    compose_blueprint(img44, os.path.join(OUT_DIR, "instrument-panel-wall.png"), "仪表监控面板墙蓝图 (Instrument Panel Setup)", l44, m44, ann44)

    # 45. 大型水车动力站
    b45 = [
        (0, 0, 0, "tinted_glass"), (1, 0, 0, "tinted_glass"), (2, 0, 0, "tinted_glass"),
        (1, 1, 0, "spruce_log", 90, 0),
        (1, 1, -1, "lightning_rod", 90, 0)
    ]
    img45 = render_scene(b45, scale=3.8)
    l45 = [
        {
            'title': "第 1 层 (Y=1 宽广驱动水渠)",
            'note': "平铺连续流水冲击叶轮切线",
            'grid': [
                [ ('tinted_glass', '流水', (56, 189, 248, 255)), ('tinted_glass', '流水', (56, 189, 248, 255)), ('tinted_glass', '流水', (56, 189, 248, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 巨型木轮与后置转轴)",
            'note': "半径 2.5 巨型叶轮，背侧接出输出轴",
            'grid': [
                [ None, ('lightning_rod', '传动轴', (249, 115, 22, 255)), None ],
                [ None, ('spruce_log', '大水车', (239, 68, 68, 255)), None ]
            ]
        }
    ]
    m45 = [
        "【大型水车】× 1（半径 2.5 巨型叶轮，需 5×5 水域驱动）",
        "【宽广流水水渠】× 3（稳定水流冲击轮叶）",
        "【输出传动轴】× 1（稳定输出 32 转/分 · 4096 应力单位）"
    ]
    ann45 = [
        {
            'rel_pos': (0.50, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【大型水车】", 'lines': ["多方块结构大木轮，半径 2.5 格", "宽广水域冲刷即转，输出高达 4096 应力容量"]
        },
        {
            'rel_pos': (0.35, 0.72), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【驱动水渠】", 'lines': ["周围水流顺切线持续冲刷", "零燃料零电耗，大厂基底澎湃动力"]
        },
        {
            'rel_pos': (0.65, 0.28), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【输出传动轴】", 'lines': ["后置中心轴直接引入机房主电网", "双倍于普通水车的充沛转速"]
        }
    ]
    compose_blueprint(img45, os.path.join(OUT_DIR, "big-water-wheel-station.png"), "大型水车动力站蓝图 (Big Water Wheel Station)", l45, m45, ann45)

    # 46. 工业高炉独立冶炼站
    b46 = [
        (0, 0, 0, "barrel"),
        (0, 1, 0, "blast_furnace", 0, 180),
        (0, 2, 0, "hopper", 0, 0),
        (-1, 1, 0, "hopper", 0, 90)
    ]
    img46 = render_scene(b46, scale=3.8)
    l46 = [
        {
            'title': "第 1 层 (Y=1 底部成品出料箱)",
            'note': "暂存烧结完成的金属锭",
            'grid': [ [ ('barrel_top', '成品箱', (34, 197, 94, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 工业高炉与侧面燃料仓)",
            'note': "中置高炉，左接燃料漏斗",
            'grid': [ [ ('hopper_outside', '燃料斗', (249, 115, 22, 255)), ('blast_furnace_front', '工业高炉', (239, 68, 68, 255)) ] ]
        },
        {
            'title': "第 3 层 (Y=3 顶部原矿进料斗)",
            'note': "漏斗对准顶部投入粗矿",
            'grid': [ [ None, ('hopper_outside', '进矿斗', (148, 163, 184, 255)) ] ]
        }
    ]
    m46 = [
        "【工业高炉】× 1（燃料冶炼，速度 2 倍 + 25% 额外产出）",
        "【进料漏斗】× 2（顶部进原矿，侧面进煤炭燃料）",
        "【成品料箱】× 1（底部自动收集金属锭）"
    ]
    ann46 = [
        {
            'rel_pos': (0.50, 0.48), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【工业高炉】", 'lines': ["独立燃料驱动，完全免除外部电网", "冶炼速度翻倍，且有 25% 概率产出双倍矿锭"]
        },
        {
            'rel_pos': (0.28, 0.48), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【双漏斗供料】", 'lines': ["顶部投矿、侧面加煤，全自动连续烧炼", "早期无电矿场的高效粗炼核心"]
        },
        {
            'rel_pos': (0.50, 0.78), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【成品收集箱】", 'lines': ["金属锭自动沉降归仓", "支持后续对接传送带发运"]
        }
    ]
    compose_blueprint(img46, os.path.join(OUT_DIR, "blast-furnace-setup.png"), "工业高炉独立冶炼站蓝图 (Blast Furnace Setup)", l46, m46, ann46)

    # 47. 土制耐火窑炉
    b47 = [
        (0, 0, 0, "smoker", 0, 180),
        (1, 0, 0, "barrel"),
        (0, 1, 0, "hopper", 0, 0)
    ]
    img47 = render_scene(b47, scale=4.0)
    l47 = [
        {
            'title': "第 1 层 (Y=1 窑炉与耐火材料箱)",
            'note': "中置耐火窑，侧接成品箱",
            'grid': [ [ ('smoker_front', '耐火窑', (239, 68, 68, 255)), ('barrel_top', '耐火砖箱', (34, 197, 94, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 顶部原料进料漏斗)",
            'note': "投入黏土坯料慢速焙烧",
            'grid': [ [ ('hopper_outside', '坯料斗', (148, 163, 184, 255)), None ] ]
        }
    ]
    m47 = [
        "【土制耐火窑】× 1（低温慢速焙烧耐火建材）",
        "【进料漏斗】× 1（顶部投入黏土球与坯料）",
        "【成品料箱】× 1（收集耐火砖与坩埚构件）"
    ]
    ann47 = [
        {
            'rel_pos': (0.42, 0.58), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【土制耐火窑】", 'lines': ["慢火均匀焙烧黏土与生坯", "产出耐高温耐火砖，为搭建重型锻造炉备料"]
        },
        {
            'rel_pos': (0.42, 0.28), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【进料漏斗】", 'lines': ["顶部自动注入黏土生料", "连续闷烧杜绝坯体受热不均开裂"]
        },
        {
            'rel_pos': (0.75, 0.58), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【耐火砖料箱】", 'lines': ["焙烧成品自动导出归仓", "热工重工基石原料集散地"]
        }
    ]
    compose_blueprint(img47, os.path.join(OUT_DIR, "kiln-setup.png"), "土制耐火窑炉蓝图 (Kiln Setup)", l47, m47, ann47)

    # 48. 木炭闷烧窑
    b48 = [
        (0, 0, 0, "campfire"),
        (1, 0, 0, "barrel"),
        (-1, 0, 0, "spruce_log")
    ]
    img48 = render_scene(b48, scale=4.0)
    l48 = [{
        'title': "第 1 层 (Y=1 原木堆放、木炭窑与收集箱)",
        'note': "左放原木，中置营火闷烧结构，右接木炭箱",
        'grid': [
            [ ('spruce_log', '原木堆', (148, 163, 184, 255)), ('campfire_log', '木炭窑', (239, 68, 68, 255)), ('barrel_top', '木炭箱', (34, 197, 94, 255)) ]
        ]
    }]
    m48 = [
        "【木炭窑】× 1（营火闷烧构造，原木以 1.5 倍产出慢速制炭）",
        "【储木备料堆】× 1（持续提供纯净原木）",
        "【木炭收集箱】× 1（收集高转化率纯净木炭）"
    ]
    ann48 = [
        {
            'rel_pos': (0.48, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【木炭窑】", 'lines': ["开放式营火闷烧构造，低温缺氧热解原木", "木炭产出率高达普通熔炉的 1.5 倍，完全免电"]
        },
        {
            'rel_pos': (0.24, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【原木备料堆】", 'lines': ["支持各种原木投入", "林场副产物转为高热值固体燃料"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【木炭收集箱】", 'lines': ["收集优质木炭", "稳定供给高炉与蒸汽机组燃料仓"]
        }
    ]
    compose_blueprint(img48, os.path.join(OUT_DIR, "charcoal-kiln-setup.png"), "木炭闷烧窑蓝图 (Charcoal Kiln Setup)", l48, m48, ann48)

    # 49. 工业冷却塔散热机组
    b49 = [
        (0, 0, 0, "furnace_on", 0, 180),
        (1, 0, 0, "snow_block"),
        (1, 1, 0, "glass")
    ]
    img49 = render_scene(b49, scale=4.0)
    l49 = [
        {
            'title': "第 1 层 (Y=1 高热机器与贴紧冷却塔)",
            'note': "冷却塔紧贴在超频发热机器侧面",
            'grid': [ [ ('furnace_front_on', '高热机器', (239, 68, 68, 255)), ('snow', '冷却塔', (56, 189, 248, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 循环冷水进水管)",
            'note': "顶接密封管道注入冷却水流",
            'grid': [ [ None, ('glass', '冷水管', (56, 189, 248, 255)) ] ]
        }
    ]
    m49 = [
        "【工业冷却塔】× 1（贴紧发热机台，供水后散热速度大增）",
        "【循环冷水管道】× 1（注入冷凝水循环降温）",
        "【超频机台】× 1（高负荷作业机器）"
    ]
    ann49 = [
        {
            'rel_pos': (0.65, 0.58), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【工业冷却塔】", 'lines': ["紧贴超频机台侧面放置，内部强效热交换", "通入冷水后散热速度成倍提升，防止过热跳闸"]
        },
        {
            'rel_pos': (0.65, 0.28), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【循环冷水管】", 'lines': ["直连抽水泵或液体储罐持续注水", "冷水循环带走热量，维持设备峰值转速"]
        },
        {
            'rel_pos': (0.35, 0.58), 'card_x': 1140, 'card_y': 500, 'color': (239, 68, 68),
            'title': "【高热发电机台】", 'lines': ["支持粉碎机、冲压机等多款超频机台", "在冷却塔保护下全天候极限超频运转"]
        }
    ]
    compose_blueprint(img49, os.path.join(OUT_DIR, "cooling-tower-setup.png"), "工业冷却塔散热机组蓝图 (Cooling Tower Setup)", l49, m49, ann49)

    # 50. 工业岩浆抽取站
    b50 = [
        (0, 0, 0, "tinted_glass"),
        (1, 0, 0, "nether_bricks"),
        (1, 1, 0, "tinted_glass"),
        (2, 1, 0, "tinted_glass")
    ]
    img50 = render_scene(b50, scale=3.8)
    l50 = [
        {
            'title': "第 1 层 (Y=1 岩浆池与加固耐腐蚀岩浆泵)",
            'note': "岩浆泵紧贴熔岩源，底部接电",
            'grid': [ [ ('tinted_glass', '岩浆池', (249, 115, 22, 255)), ('nether_bricks', '岩浆泵', (239, 68, 68, 255)), None ] ]
        },
        {
            'title': "第 2 层 (Y=2 加强耐火流体管网)",
            'note': "墨色耐火玻璃密封管道安全输送高热流体",
            'grid': [ [ None, ('tinted_glass', '加强管', (168, 85, 247, 255)), ('tinted_glass', '加强管', (168, 85, 247, 255)) ] ]
        }
    ]
    m50 = [
        "【工业岩浆泵】× 1（下界耐火合金加固，抽取熔岩耗电 4 能量/秒）",
        "【加强流体管道】× 2（墨色耐火玻璃，耐极端高温防爆）",
        "【高温熔岩源】× 1（天然岩浆池或下界熔岩海）"
    ]
    ann50 = [
        {
            'rel_pos': (0.45, 0.65), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【工业岩浆泵】", 'lines': ["下界合金防爆外壳，专门抽取千度高热熔岩", "电网供电，自动加压注入高温输送管网"]
        },
        {
            'rel_pos': (0.65, 0.35), 'card_x': 1140, 'card_y': 360, 'color': (168, 85, 247),
            'title': "【加强流体管】", 'lines': ["墨色耐高温钢化玻璃管，绝无融毁风险", "安全横跨长距离将熔岩送入车间"]
        },
        {
            'rel_pos': (0.24, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【高温岩浆源】", 'lines': ["直接抽取地下岩浆海", "为地热发电、高温注液与特种合金提供高热工质"]
        }
    ]
    compose_blueprint(img50, os.path.join(OUT_DIR, "lava-pump-setup.png"), "工业岩浆抽取站蓝图 (Lava Pump Setup)", l50, m50, ann50)

    # 51. 多方块大型储水塔
    b51 = [
        (0, 0, 0, "blue_stained_glass"), (1, 0, 0, "blue_stained_glass"),
        (0, 1, 0, "blue_stained_glass"), (1, 1, 0, "blue_stained_glass"),
        (2, 0, 0, "glass")
    ]
    img51 = render_scene(b51, scale=3.6)
    l51 = [
        {
            'title': "第 1 层 (Y=1 储水罐底层与出水管)",
            'note': "2×1 储罐贴合并接出水管",
            'grid': [ [ ('blue_stained_glass', '储液罐', (56, 189, 248, 255)), ('blue_stained_glass', '储液罐', (56, 189, 248, 255)), ('glass', '出水管', (56, 189, 248, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 向上堆叠自融合)",
            'note': "自融合扩容为一体化透明水塔",
            'grid': [ [ ('blue_stained_glass', '储液罐', (56, 189, 248, 255)), ('blue_stained_glass', '储液罐', (56, 189, 248, 255)), None ] ]
        }
    ]
    m51 = [
        "【液体储罐】× 4（每格容量 8000 毫桶，相邻共面自动融合）",
        "【流体管道】× 1（底部引出供水主管）"
    ]
    ann51 = [
        {
            'rel_pos': (0.45, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【自融合储液塔】", 'lines': ["深蓝色防爆玻璃方块，多个并排自动消除内壁", "融合成大型透明水塔，塔身自带实时液位刻度"]
        },
        {
            'rel_pos': (0.75, 0.65), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【出水总管】", 'lines': ["底部直连水管，利用重力与水压自流供水", "支持为全厂锅炉、洗矿机与注液流水线持续保压"]
        },
        {
            'rel_pos': (0.45, 0.18), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【模块化扩容】", 'lines': ["支持横向铺开或纵向加高", "每增加一个方块即扩展 8000 毫桶储液量"]
        }
    ]
    compose_blueprint(img51, os.path.join(OUT_DIR, "fluid-tank-multiblock.png"), "多方块大型储水塔蓝图 (Fluid Tank Multiblock)", l51, m51, ann51)

    # 52. 流体阀门与分液池分配网
    b52 = [
        (-1, 0, 0, "stone_bricks"), (0, 0, 0, "stone_bricks"), (1, 0, 0, "stone_bricks"),
        (2, 0, 0, "stone_bricks"), (2, 0, -1, "stone_bricks"), (2, 0, 1, "stone_bricks"), (3, 0, 0, "stone_bricks"),
        (-1, 1, 0, "glass"),
        (0, 1, 0, "iron_door_bottom_left"),
        (0, 2, 0, "iron_door_top_left"),
        (1, 1, 0, "glass"),
        (2, 1, 0, "cauldron"),
        (2, 1, -1, "glass"),
        (2, 1, 1, "glass"),
        (3, 1, 0, "glass")
    ]
    img52 = render_scene(b52, scale=3.6)
    l52 = [
        {
            'title': "第 1 层 (Y=1 铺设平整管道地基)",
            'note': "在平地铺设稳固石砖，承托截流闸阀与分液池",
            'grid': [
                [ None, None, None, ('stone_bricks', '基座', (148, 163, 184, 255)), None ],
                [ ('stone_bricks', '基座', (148, 163, 184, 255)), ('stone_bricks', '基座', (148, 163, 184, 255)), ('stone_bricks', '基座', (148, 163, 184, 255)), ('stone_bricks', '基座', (148, 163, 184, 255)), ('stone_bricks', '基座', (148, 163, 184, 255)) ],
                [ None, None, None, ('stone_bricks', '基座', (148, 163, 184, 255)), None ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 输水管道、流体阀门与分液池)",
            'note': "主管串联阀门通入分液池，分流至支线管网",
            'grid': [
                [ None, None, None, ('glass', '支管1', (56, 189, 248, 255)), None ],
                [ ('glass', '主管', (56, 189, 248, 255)), ('iron_door_top', '流体阀门', (239, 68, 68, 255)), ('glass', '导管', (56, 189, 248, 255)), ('cauldron_side', '分液池', (249, 115, 22, 255)), ('glass', '支管3', (56, 189, 248, 255)) ],
                [ None, None, None, ('glass', '支管2', (56, 189, 248, 255)), None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 闸阀开关手柄与开启指示)",
            'note': "阀门向上延伸为双格高闸门，右键启闭",
            'grid': [
                [ None, None, None, None, None ],
                [ None, ('iron_door_top', '阀门顶部', (239, 68, 68, 255)), None, None, None ],
                [ None, None, None, None, None ]
            ]
        }
    ]
    m52 = [
        "【流体阀门】× 1（截流闸板阀门，右键快速切换通断）",
        "【分液池】× 1（铸铁深池构造，多向轮询分流中枢）",
        "【流体管道】× 5（主干管、导管与多路分配支管）",
        "【加固基座】× 7（平整地面承托阀门与水池）"
    ]
    ann52 = [
        {
            'rel_pos': (0.35, 0.40), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【流体阀门闸板】", 'lines': ["基座上安放截流闸阀，串联在管道干线中段", "右键快速切换通断，断流时彻底阻断流体，方便分段检修"]
        },
        {
            'rel_pos': (0.65, 0.48), 'card_x': 1140, 'card_y': 350, 'color': (249, 115, 22),
            'title': "【多向分液池】", 'lines': ["单入多出轮询分流中枢，自动无需复杂红石配置", "将一路大流量水流均衡分流至各车间独立支管"]
        },
        {
            'rel_pos': (0.80, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【分配输出支管】", 'lines': ["多路管线井然有序引向各加工母机与发电机组", "彻底杜绝单管供液不足与管路紊乱问题"]
        }
    ]
    compose_blueprint(img52, os.path.join(OUT_DIR, "fluid-valve-and-splitter.png"), "流体阀门与分液池分配网蓝图 (Fluid Valve & Splitter)", l52, m52, ann52)

    # 53. 传送带流量计监测站
    b53 = [
        (0, 0, 0, "stone_slab_top"),
        (0, 1, 0, "comparator", 0, 180),
        (1, 1, 0, "redstone_lamp")
    ]
    img53 = render_scene(b53, scale=4.0)
    l53 = [
        {
            'title': "第 1 层 (Y=1 连续物流传送带)",
            'note': "平铺传送带半砖，承载流通物品",
            'grid': [ [ ('stone_slab_top', '带面', (249, 115, 22, 255)), None ] ]
        },
        {
            'title': "第 2 层 (Y=2 流量计与红石指示灯)",
            'note': "流量计置于半砖上方，侧接红石指示灯",
            'grid': [ [ ('comparator', '流量计', (56, 189, 248, 255)), ('redstone_lamp', '指示灯', (234, 179, 8, 255)) ] ]
        }
    ]
    m53 = [
        "【流量计】× 1（架设于传送带半砖上方，统计流经物品数）",
        "【传送带半砖】× 1（承载物料平稳滑行通过）",
        "【红石指示灯】× 1（检测到物流时高亮发光）"
    ]
    ann53 = [
        {
            'rel_pos': (0.42, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【传送带流量计】", 'lines': ["直接安放于传送带半砖正上方，实时统计通过物品", "有物流通过时自动输出红石信号"]
        },
        {
            'rel_pos': (0.75, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (234, 179, 8),
            'title': "【红石信号输出】", 'lines': ["物流流通即时触发红石脉冲", "可直连指示灯目视监控，或联动报警停机"]
        },
        {
            'rel_pos': (0.42, 0.72), 'card_x': 1140, 'card_y': 500, 'color': (249, 115, 22),
            'title': "【连续传送带】", 'lines': ["无感原位测流，不阻挡货品滑行", "流水线全程保持高速连续运转"]
        }
    ]
    compose_blueprint(img53, os.path.join(OUT_DIR, "flow-meter-setup.png"), "传送带流量计监测站蓝图 (Flow Meter Setup)", l53, m53, ann53)

    # 54. 轻型钻井平台开采站
    b54 = [
        (0, 0, 0, "dispenser", 180, 0),
        (0, 0, -1, "redstone_block"),
        (1, 0, 0, "barrel")
    ]
    img54 = render_scene(b54, scale=4.0)
    l54 = [{
        'title': "第 1 层 (Y=1 钻机、电缆与矿石收集箱)",
        'note': "中置钻机（钻头朝下），后接电网，侧放料箱",
        'grid': [
            [ ('redstone_block', '电网', (234, 179, 8, 255)), None ],
            [ ('dispenser_front', '钻井机', (239, 68, 68, 255)), ('barrel_top', '矿石箱', (34, 197, 94, 255)) ]
        ]
    }]
    m54 = [
        "【轻型钻井平台】× 1（3×3 范围逐层下探采掘，20 能量/格）",
        "【矿物提取箱】× 1（侧面暂存采掘出的纯净矿石）",
        "【工业供电线路】× 1（接入电网持续供电）"
    ]
    ann54 = [
        {
            'rel_pos': (0.42, 0.48), 'card_x': 1140, 'card_y': 220, 'color': (239, 68, 68),
            'title': "【轻型钻井平台】", 'lines': ["3×3 范围逐层垂直下探采掘", "自动原位废石充填，杜绝深渊空洞安全隐患"]
        },
        {
            'rel_pos': (0.75, 0.58), 'card_x': 1140, 'card_y': 360, 'color': (34, 197, 94),
            'title': "【矿物提取箱】", 'lines': ["自动过滤废石，仅提取有效矿藏", "矿石自动归仓，支持直连传送带发运"]
        },
        {
            'rel_pos': (0.35, 0.28), 'card_x': 1140, 'card_y': 500, 'color': (234, 179, 8),
            'title': "【工业供电线路】", 'lines': ["每挖掘一格仅消耗 20 能量单位", "开荒采矿自动化标配设备"]
        }
    ]
    compose_blueprint(img54, os.path.join(OUT_DIR, "mining-drill-setup.png"), "轻型钻井平台开采站蓝图 (Mining Drill Setup)", l54, m54, ann54)

    # 55. 气流电梯井道
    b55 = [
        (0, 0, 0, "quartz_pillar"),
        (-1, 0, 0, "quartz_block"), (1, 0, 0, "quartz_block"), (0, 0, -1, "quartz_block"),
        (-1, 1, 0, "quartz_block"), (1, 1, 0, "quartz_block"), (0, 1, -1, "quartz_block")
    ]
    img55 = render_scene(b55, scale=3.6)
    l55 = [
        {
            'title': "第 1 层 (Y=1 升降机底座与三面井壁)",
            'note': "井底中心平铺升降机方块",
            'grid': [
                [ None, ('quartz_block_side', '井壁', (148, 163, 184, 255)), None ],
                [ ('quartz_block_side', '井壁', (148, 163, 184, 255)), ('quartz_pillar_top', '升降机', (56, 189, 248, 255)), ('quartz_block_side', '井壁', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 垂直导向井道)",
            'note': "三面包围引导气流直冲云霄",
            'grid': [
                [ None, ('quartz_block_side', '井壁', (148, 163, 184, 255)), None ],
                [ ('quartz_block_side', '井壁', (148, 163, 184, 255)), None, ('quartz_block_side', '井壁', (148, 163, 184, 255)) ]
            ]
        }
    ]
    m55 = [
        "【气流升降机】× 1（平铺于电梯井底地面，右键乘上升气流）",
        "【石英结构井壁】× 6（封闭三面形成笔直垂直气流井道）"
    ]
    ann55 = [
        {
            'rel_pos': (0.50, 0.65), 'card_x': 1140, 'card_y': 220, 'color': (56, 189, 248),
            'title': "【气流升降机】", 'lines': ["右键点击即可乘强劲上升气流直达高层", "潜行（Shift）右键平稳下行，完全零电耗"]
        },
        {
            'rel_pos': (0.32, 0.35), 'card_x': 1140, 'card_y': 360, 'color': (148, 163, 184),
            'title': "【垂直导向井壁】", 'lines': ["建议三面或四面包围封闭井道", "防止玩家升空过程中偏航跌落"]
        },
        {
            'rel_pos': (0.50, 0.18), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【高层出站口】", 'lines': ["直通高层车间或高山观察哨", "多层厂房秒级人员穿梭利器"]
        }
    ]
    compose_blueprint(img55, os.path.join(OUT_DIR, "elevator-shaft-setup.png"), "气流电梯井道蓝图 (Elevator Shaft Setup)", l55, m55, ann55)

    # 56. 矿区滑轮缆绳电梯
    b56 = [
        (0, 0, 0, "stone_bricks"), (0, 1, 0, "stone_bricks"), (0, 2, 0, "stone_bricks"),
        (1, 2, 0, "iron_bars_post"),
        (1, 1, 0, "iron_bars_post"),
        (1, 0, 0, "iron_bars_post")
    ]
    img56 = render_scene(b56, scale=3.6)
    l56 = [
        {
            'title': "第 1~3 层 (Y=1~3 缆绳与井壁装配)",
            'note': "井顶放滑轮，向下同轴铺高强度绳索",
            'grid': [ [ ('stone_bricks', '井壁', (148, 163, 184, 255)), ('iron_bars', '缆绳', (249, 115, 22, 255)) ] ]
        }
    ]
    m56 = [
        "【升降机滑轮】× 1（安装于井顶或井底）",
        "【高强度绳索】× 3（贴滑轮同轴垂直铺设）",
        "【加固井壁】× 3（立柱承重支柱）"
    ]
    ann56 = [
        {
            'rel_pos': (0.65, 0.22), 'card_x': 1140, 'card_y': 220, 'color': (249, 115, 22),
            'title': "【升降机滑轮】", 'lines': ["安装于深井天井顶部或井底", "右键滑轮或绳索自动升降搭乘"]
        },
        {
            'rel_pos': (0.65, 0.55), 'card_x': 1140, 'card_y': 360, 'color': (249, 115, 22),
            'title': "【高强度绳索】", 'lines': ["同轴垂直向下或向上铺设成缆", "乘行中右键可换向，潜行脱离，绳断即停"]
        },
        {
            'rel_pos': (0.35, 0.45), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【坚固承重井壁】", 'lines': ["靠墙铺设形成真实矿井升降机感", "深矿矿坑快速安全通勤首选"]
        }
    ]
    compose_blueprint(img56, os.path.join(OUT_DIR, "rope-pulley-elevator.png"), "矿区滑轮缆绳电梯蓝图 (Rope Pulley Elevator)", l56, m56, ann56)

    # 57. 陆地工程车底盘组装
    b57 = [
        (0, 0, 0, "smooth_stone"), (1, 0, 0, "smooth_stone"),
        (0, 1, 0, "dark_oak_stairs", 0, 180),
        (1, 1, 0, "furnace", 0, 180)
    ]
    img57 = render_scene(b57, scale=3.8)
    l57 = [
        {
            'title': "第 1 层 (Y=1 载具车架底盘)",
            'note': "平滑石相连成排构成车架",
            'grid': [ [ ('smooth_stone', '底盘', (148, 163, 184, 255)), ('smooth_stone', '底盘', (148, 163, 184, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 驾驶座与车辆发动机)",
            'note': "前放驾驶座，后装大扭矩发动机",
            'grid': [ [ ('dark_oak_planks', '驾驶座', (234, 179, 8, 255)), ('furnace_front_on', '发动机', (239, 68, 68, 255)) ] ]
        }
    ]
    m57 = [
        "【载具底盘】× 2（平滑石相连成排构成车身骨架）",
        "【驾驶座】× 1（载具控制中枢，手持扳手登记结构）",
        "【车辆发动机】× 1（陆地动力核心，消耗煤炭燃料，具备 1 格台阶爬升能力）"
    ]
    ann57 = [
        {
            'rel_pos': (0.42, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (234, 179, 8),
            'title': "【驾驶座】", 'lines': ["放在底盘框架上，扳手右键登记车辆结构", "空手右键坐上开行，视线方向即为前进方向"]
        },
        {
            'rel_pos': (0.68, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (239, 68, 68),
            'title': "【车辆发动机】", 'lines': ["每车仅限一个，右键放入固体煤炭驱动", "平地快速行驶，遇 1 格台阶自动爬升"]
        },
        {
            'rel_pos': (0.45, 0.72), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【载具底盘】", 'lines': ["平滑石与铁锭打造刚性龙骨", "相邻水平拼接即可蔓延扩展车身"]
        }
    ]
    compose_blueprint(img57, os.path.join(OUT_DIR, "vehicle-car-assembly.png"), "陆地工程车底盘组装蓝图 (Land Vehicle Assembly)", l57, m57, ann57)

    # 58. 水面机动船组装
    b58 = [
        (0, 0, 0, "smooth_stone"), (1, 0, 0, "smooth_stone"),
        (0, 1, 0, "dark_oak_stairs", 0, 180),
        (1, 1, 0, "furnace", 0, 180)
    ]
    img58 = render_scene(b58, scale=3.8)
    l58 = [
        {
            'title': "第 1 层 (Y=1 船体底盘骨架)",
            'note': "浮于水面上的平滑石底盘",
            'grid': [ [ ('smooth_stone', '船架', (148, 163, 184, 255)), ('smooth_stone', '船架', (148, 163, 184, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 驾驶座与船用发动机)",
            'note': "前驾驶座，后装高燃效船机",
            'grid': [ [ ('dark_oak_planks', '驾驶座', (234, 179, 8, 255)), ('furnace_front_on', '船用发动机', (56, 189, 248, 255)) ] ]
        }
    ]
    m58 = [
        "【载具底盘】× 2（轻质平滑石船体框架）",
        "【驾驶座】× 1（Shift+扳手切换为水面船舶模式）",
        "【船只发动机】× 1（水面专用发动机，燃料利用率提升 50%）"
    ]
    ann58 = [
        {
            'rel_pos': (0.42, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (234, 179, 8),
            'title': "【船舶驾驶座】", 'lines': ["手持扳手 Shift+右键切换为船舶模式", "锁定在水面高度开行，杜绝沉底翻船"]
        },
        {
            'rel_pos': (0.68, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (56, 189, 248),
            'title': "【船只发动机】", 'lines': ["水面推进效率卓越，燃料利用率高达 150%", "消耗少量煤炭即可跨洋远航巡航"]
        },
        {
            'rel_pos': (0.45, 0.72), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【轻量化船体】", 'lines': ["浮水底盘可左右扩展船身", "支持搭载鱼网、货柜与探照灯"]
        }
    ]
    compose_blueprint(img58, os.path.join(OUT_DIR, "vehicle-boat-assembly.png"), "水面机动船组装蓝图 (Motorboat Assembly)", l58, m58, ann58)

    # 59. 飞行勘探飞艇组装
    b59 = [
        (0, 0, 0, "smooth_stone"), (1, 0, 0, "smooth_stone"),
        (0, 1, 0, "dark_oak_stairs", 0, 180),
        (1, 1, 0, "furnace", 0, 180)
    ]
    img59 = render_scene(b59, scale=3.8)
    l59 = [
        {
            'title': "第 1 层 (Y=1 飞艇吊舱底盘)",
            'note': "底盘骨架平铺",
            'grid': [ [ ('smooth_stone', '吊舱', (148, 163, 184, 255)), ('smooth_stone', '吊舱', (148, 163, 184, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 驾驶座与航空发动机)",
            'note': "前部驾驶座，后装高功率航机",
            'grid': [ [ ('dark_oak_planks', '驾驶座', (234, 179, 8, 255)), ('furnace_front_on', '航机', (168, 85, 247, 255)) ] ]
        }
    ]
    m59 = [
        "【载具底盘】× 2（轻质飞艇吊舱车架）",
        "【驾驶座】× 1（Shift+扳手切换为飞行飞艇模式）",
        "【航空发动机】× 1（高功率航空引擎，速度 2 tick/格）"
    ]
    ann59 = [
        {
            'rel_pos': (0.42, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (234, 179, 8),
            'title': "【飞艇驾驶座】", 'lines': ["Shift+扳手切换为飞艇模式，空手右键登艇", "仰角 >40° 爬升，俯角 <-40° 下降，平视为平飞"]
        },
        {
            'rel_pos': (0.68, 0.45), 'card_x': 1140, 'card_y': 360, 'color': (168, 85, 247),
            'title': "【航空发动机】", 'lines': ["高功率强劲涡轮推力，航速极快", "空中巡航无视高山与峡谷险阻"]
        },
        {
            'rel_pos': (0.45, 0.72), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【轻质飞艇底盘】", 'lines': ["平滑石底盘铺设飞行骨架", "仅需底盘+驾驶座+航机即可升空飞行"]
        }
    ]
    compose_blueprint(img59, os.path.join(OUT_DIR, "vehicle-airship-assembly.png"), "飞行勘探飞艇组装蓝图 (Airship Assembly)", l59, m59, ann59)

    # 60. 密集仓储货架集群
    b60 = [
        (0, 0, 0, "bookshelf"), (1, 0, 0, "bookshelf"),
        (0, 1, 0, "bookshelf"), (1, 1, 0, "bookshelf"),
        (2, 0, 0, "barrel")
    ]
    img60 = render_scene(b60, scale=3.6)
    l60 = [
        {
            'title': "第 1 层 (Y=1 货架底层与出料料箱)",
            'note': "2×1 并排货架，侧接周转箱",
            'grid': [ [ ('bookshelf', '货架', (249, 115, 22, 255)), ('bookshelf', '货架', (249, 115, 22, 255)), ('barrel_top', '周转箱', (34, 197, 94, 255)) ] ]
        },
        {
            'title': "第 2 层 (Y=2 向上堆叠扩展)",
            'note': "纵向扩展形成密集货架墙",
            'grid': [ [ ('bookshelf', '货架', (249, 115, 22, 255)), ('bookshelf', '货架', (249, 115, 22, 255)), None ] ]
        }
    ]
    m60 = [
        "【密集仓储货架】× 4（单格容纳 576 件同类物品，手持同类右键成批存取）",
        "【周转料箱】× 1（侧面暂存混合零散物料）"
    ]
    ann60 = [
        {
            'rel_pos': (0.45, 0.45), 'card_x': 1140, 'card_y': 220, 'color': (249, 115, 22),
            'title': "【密集货架墙】", 'lines': ["单格专储一种物品，最大容量达 576 件", "手持同类物品右键瞬间全存，空手右键成组取出"]
        },
        {
            'rel_pos': (0.75, 0.65), 'card_x': 1140, 'card_y': 360, 'color': (34, 197, 94),
            'title': "【周转料箱】", 'lines': ["侧面摆放普通木桶用于临时暂存", "支持漏斗与机械臂高速存取周转"]
        },
        {
            'rel_pos': (0.45, 0.18), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【靠墙货架布局】", 'lines': ["靠车间墙面铺设形成整齐壮观的工业仓储走廊", "极其适合金属锭、矿粉与板材的分类专储"]
        }
    ]
    compose_blueprint(img60, os.path.join(OUT_DIR, "shelf-storage-setup.png"), "密集仓储货架集群蓝图 (Shelf Storage Setup)", l60, m60, ann60)

    print("Batch 3 blueprints successfully generated!")

if __name__ == "__main__":
    generate_batch3()
