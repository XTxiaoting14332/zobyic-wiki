import os
from .rasterizer import render_scene
from .composer import compose_blueprint

OUT_DIR = "/home/nightwind/workspace/zobyic-wiki/docs/public/images/ztech"

def generate_batch5():
    print("=== Generating Blueprints Batch 5 (Logistics, Splitters, Meters, Gearboxes) ===")

    # ================= 66. 倾斜传送带爬升与俯冲 =================
    b66 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_stairs", 0, 0),
        (2, 1, 0, "stone_stairs", 0, 0),
        (3, 2, 0, "iron_block"),
        (0, 0, 1, "redstone_block")
    ]
    img66 = render_scene(b66, scale=3.6)
    l66 = [
        {
            'title': "第 1 层 (Y=1 低位驱动端与起坡段)",
            'note': "起点支架接入电网，紧接首段爬升楼梯",
            'grid': [
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None, None ],
                [ ('iron_block', '起点支架', (239, 68, 68, 255)), ('stone_stairs', '倾斜带面', (148, 163, 184, 255)), None, None ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 45° 中位平滑爬升段)",
            'note': "楼梯方块连续咬合，工件平稳爬升不后溜",
            'grid': [
                [ None, None, None, None ],
                [ None, None, ('stone_stairs', '倾斜带面', (148, 163, 184, 255)), None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 高位出料与接驳支架)",
            'note': "流水线高处末端，直连高层车间产线",
            'grid': [
                [ None, None, None, None ],
                [ None, None, None, ('iron_block', '终点支架', (34, 197, 94, 255)) ]
            ]
        }
    ]
    m66 = [
        "【倾斜传送带】× 2（连续楼梯段咬合形成 45° 爬升斜坡）",
        "【传送带支架】× 2（低位入料驱动端与高位出料支架）",
        "【供电线路】× 1（上行消耗 2 能量/秒，下行重力免费）"
    ]
    ann66 = [
        {
            'rel_pos': (0.18, 0.65), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【低位驱动支架】", 'lines': ["低端动力核心输入端，连接平地车间物料干线", "上行爬升耗电 2 能量/秒，下行重力俯冲完全零能耗"]
        },
        {
            'rel_pos': (0.46, 0.48), 'card_x': 1140, 'card_y': 350, 'color': (148, 163, 184),
            'title': "【45° 倾斜带面】", 'lines': ["石楼梯方块连续紧密咬合，形成 45° 攀爬斜坡", "手持工业扳手右键敲击，可一键翻转输送方向"]
        },
        {
            'rel_pos': (0.78, 0.30), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【高位接驳终点】", 'lines': ["平滑送达二层或立体高架货仓，杜绝卡料脱落", "末端可直接衔接水平流水线或原位加工机台"]
        }
    ]
    compose_blueprint(img66, os.path.join(OUT_DIR, "ramp-belt-setup.png"), "倾斜传送带爬升流水线蓝图 (Ramp Belt Setup)", l66, m66, ann66)

    # ================= 67. 重力滑道与拐弯滑轨 =================
    b67 = [
        (0, 3, 0, "barrel"),
        (1, 2, 0, "sandstone_stairs", 0, 180),
        (2, 1, 0, "sandstone_stairs_inner", 0, 180),
        (2, 0, 1, "sandstone_stairs", 0, 90),
        (2, 0, 2, "barrel")
    ]
    img67 = render_scene(b67, scale=3.6)
    l67 = [
        {
            'title': "第 1 层 (Y=1 出料滑槽与底层收纳箱)",
            'note': "滑轨末端接入收集料箱，平稳承接货物",
            'grid': [
                [ None, None, None ],
                [ None, None, ('sandstone_stairs', '出料滑槽', (249, 115, 22, 255)) ],
                [ None, None, ('barrel_top', '收料箱', (34, 197, 94, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 拐弯换向滑槽)",
            'note': "直角转向平滑过渡，绕开承重立柱",
            'grid': [
                [ None, None, ('sandstone_stairs', '转弯槽', (249, 115, 22, 255)) ],
                [ None, None, None ],
                [ None, None, None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 首段俯冲滑槽)",
            'note': "承接高位下坠物料，开启极速滑降",
            'grid': [
                [ None, ('sandstone_stairs', '俯冲滑槽', (249, 115, 22, 255)), None ],
                [ None, None, None ],
                [ None, None, None ]
            ]
        },
        {
            'title': "第 4 层 (Y=4 高位集料中转仓)",
            'note': "顶层料斗或箱子，物料自然滑入",
            'grid': [
                [ ('barrel_top', '高位仓', (56, 189, 248, 255)), None, None ],
                [ None, None, None ],
                [ None, None, None ]
            ]
        }
    ]
    m67 = [
        "【重力滑轨】× 3（砂岩滑道，顺重力单向高速极速滑降）",
        "【进料储物仓】× 1（高位物料源泉，自然倾泻入槽）",
        "【收料储物桶】× 1（底层平稳承接滑降货物）"
    ]
    ann67 = [
        {
            'rel_pos': (0.45, 0.22), 'card_x': 1140, 'card_y': 200, 'color': (56, 189, 248),
            'title': "【高位重力进料口】", 'lines': ["从高位料仓、粉碎机出料口直接落入滑轨", "借助自然重力驱动下坠，完全不需要消耗任何电力"]
        },
        {
            'rel_pos': (0.75, 0.55), 'card_x': 1140, 'card_y': 350, 'color': (249, 115, 22),
            'title': "【零能耗高速滑槽】", 'lines': ["砂岩内咬合滑道顺向导流，高阶承料、低阶出料", "支持 90° 灵活拐弯转弯，巧妙绕过车间承重立柱"]
        },
        {
            'rel_pos': (0.45, 0.90), 'card_x': 1140, 'card_y': 500, 'color': (34, 197, 94),
            'title': "【底层自动收纳箱】", 'lines': ["工件滑至底端平稳落入储物木箱或分拣带", "开荒初期最廉价高效的高空矿物输送方案"]
        }
    ]
    compose_blueprint(img67, os.path.join(OUT_DIR, "slide-rail-setup.png"), "重力滑道与拐弯滑轨蓝图 (Slide Rail Setup)", l67, m67, ann67)

    # ================= 68. 垂直溜槽与智能过滤料井 =================
    b68 = [
        (0, 3, 0, "barrel"),
        (0, 2, 0, "hopper", 0, 0),
        (0, 1, 0, "hopper", 0, 0),
        (0, 0, 0, "stone_slab_top"),
        (1, 0, 0, "iron_block"),
        (-1, 0, 0, "iron_block")
    ]
    img68 = render_scene(b68, scale=3.6)
    l68 = [
        {
            'title': "第 1 层 (Y=1 底层接料流水线)",
            'note': "溜槽正下方对齐传送带半砖，接纳落料",
            'grid': [
                [ ('iron_block', '起点支架', (148, 163, 184, 255)), ('stone', '接料带面', (56, 189, 248, 255)), ('iron_block', '终点支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 标准垂直溜槽管道)",
            'note': "垂直叠放形成重力下落管道，瞬间直落",
            'grid': [
                [ None, ('hopper_top', '重力溜槽', (148, 163, 184, 255)), None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 智能白名单过滤溜槽)",
            'note': "集成过滤逻辑，仅允许白名单工件掉落",
            'grid': [
                [ None, ('hopper_top', '智能溜槽', (239, 68, 68, 255)), None ]
            ]
        },
        {
            'title': "第 4 层 (Y=4 顶置总原料仓储库)",
            'note': "顶置储物箱持续为落料井供料",
            'grid': [
                [ None, ('barrel_top', '原料料箱', (234, 179, 8, 255)), None ]
            ]
        }
    ]
    m68 = [
        "【智能溜槽】× 1（内嵌电路过滤，仅放行白名单内工件）",
        "【重力溜槽】× 1（垂直叠放，形成瞬时重力落料管道）",
        "【顶置储料仓】× 1（上方大容量供料箱）",
        "【底层传送带】× 1（两端支架承接垂直落料，平稳送出）"
    ]
    ann68 = [
        {
            'rel_pos': (0.50, 0.16), 'card_x': 1140, 'card_y': 200, 'color': (234, 179, 8),
            'title': "【顶置高位原料仓】", 'lines': ["从上方料仓底部直接垂直引出落料井", "物料受重力牵引垂直下落，不吸附地面掉落杂物"]
        },
        {
            'rel_pos': (0.50, 0.40), 'card_x': 1140, 'card_y': 350, 'color': (239, 68, 68),
            'title': "【智能过滤溜槽】", 'lines': ["右键设置白名单，精准拦截不合规杂质与废矿", "仅允许目标工件穿透下坠，实现垂直重力分选"]
        },
        {
            'rel_pos': (0.50, 0.75), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【底层传送带承接】", 'lines': ["垂直下坠工件精准平躺落在传送带半砖正中央", "瞬间随带面平稳滑行送往下一加工工位"]
        }
    ]
    compose_blueprint(img68, os.path.join(OUT_DIR, "chute-and-smart-chute-setup.png"), "垂直重力溜槽与智能过滤料井蓝图 (Chute Setup)", l68, m68, ann68)

    # ================= 69. 顶置四向智能物料分拣机 =================
    b69 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "stone_slab_top"),
        (3, 0, 0, "iron_block"),
        (1, 0, 1, "stone_slab_top"),
        (1, 0, 2, "iron_block"),
        (1, 0, -1, "stone_slab_top"),
        (1, 0, -2, "iron_block"),
        (1, 1, 0, "dispenser", -90, 0),
        (0, 0, 1, "redstone_block")
    ]
    img69 = render_scene(b69, scale=3.2)
    l69 = [
        {
            'title': "第 1 层 (Y=1 十字交汇传送带网络)",
            'note': "主干流水线贯通，中间交汇点向南北引出支线",
            'grid': [
                [ None, ('iron_block', '北线终点', (34, 197, 94, 255)), None, None ],
                [ None, ('stone', '北向支线', (56, 189, 248, 255)), None, None ],
                [ ('iron_block', '主线起点', (239, 68, 68, 255)), ('stone', '十字交汇', (148, 163, 184, 255)), ('stone', '主线跑道', (148, 163, 184, 255)), ('iron_block', '主线终点', (34, 197, 94, 255)) ],
                [ ('redstone_block', '电网', (234, 179, 8, 255)), ('stone', '南向支线', (56, 189, 248, 255)), None, None ],
                [ None, ('iron_block', '南线终点', (34, 197, 94, 255)), None, None ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶置智能分拣机机头)",
            'note': "分拣机架设在十字半砖正上方第 1 格",
            'grid': [
                [ None, None, None, None ],
                [ None, None, None, None ],
                [ None, ('dispenser_front', '智能分拣机', (239, 68, 68, 255)), None, None ],
                [ None, None, None, None ],
                [ None, None, None, None ]
            ]
        }
    ]
    m69 = [
        "【智能分拣机】× 1（架设于带面上方，按类别 4 向分流）",
        "【传送带支架】× 4（主线进出端与南北双支线驱动支架）",
        "【传送带半砖】× 4（十字交叉输送带面）",
        "【供电线路】× 1（接入电网提供 2 能量/秒）"
    ]
    ann69 = [
        {
            'rel_pos': (0.40, 0.36), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【顶置四向分拣机】", 'lines': ["直接架设在十字传送带交叉点正上方第 1 格高度", "工件随传送带滑入正下方时，瞬间完成精准分流"]
        },
        {
            'rel_pos': (0.65, 0.55), 'card_x': 1140, 'card_y': 350, 'color': (234, 179, 8),
            'title': "【四向类别独立设置】", 'lines': ["右键打开配置界面，自由分配前后左右四个方向的物料类型", "原矿入粉碎车间、板材入装配车间、杂质直接归仓"]
        },
        {
            'rel_pos': (0.42, 0.78), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【全自动立体物流网】", 'lines': ["单条主干进料线同时供给四个独立车间", "彻底解决多车间混料分选与物流堵塞难题"]
        }
    ]
    compose_blueprint(img69, os.path.join(OUT_DIR, "sorting-machine-setup.png"), "顶置四向智能物料分拣机蓝图 (Sorting Machine Setup)", l69, m69, ann69)

    # ================= 70. 物品探测器红石脉冲控制站 =================
    b70 = [
        (0, 0, 0, "iron_block"),
        (1, 0, 0, "stone_slab_top"),
        (2, 0, 0, "iron_block"),
        (1, 0, 1, "observer", 0, 0),
        (1, 0, 2, "redstone_block"),
        (2, 0, 2, "redstone_lamp_on"),
        (0, 0, -1, "redstone_block")
    ]
    img70 = render_scene(b70, scale=3.8)
    l70 = [
        {
            'title': "第 1 层 (Y=1 检测跑道、探测器与指示灯)",
            'note': "探测器紧贴带面侧面，后接红石线路与报警灯",
            'grid': [
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None ],
                [ ('iron_block', '起点支架', (148, 163, 184, 255)), ('stone', '检测带面', (148, 163, 184, 255)), ('iron_block', '终点支架', (148, 163, 184, 255)) ],
                [ None, ('observer_front', '物品探测器', (239, 68, 68, 255)), None ],
                [ None, ('redstone_block', '信号线', (234, 179, 8, 255)), ('redstone_lamp', '状态灯', (56, 189, 248, 255)) ]
            ]
        }
    ]
    m70 = [
        "【物品探测器】× 1（手持目标物右键绑定，检测带面物料）",
        "【红石指示灯】× 1（检测到目标时高亮发光提示）",
        "【传送带流水线】× 1（承载物料滑行通过感应区）",
        "【红石控制线】× 1（向后传递强红石控制脉冲）"
    ]
    ann70 = [
        {
            'rel_pos': (0.42, 0.52), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【物品探测器】", 'lines': ["侧向紧贴传送带半砖安装，手持目标物品右键完成检测绑定", "当目标工件从带面上经过时，瞬间向后方输出红石信号"]
        },
        {
            'rel_pos': (0.24, 0.40), 'card_x': 1140, 'card_y': 350, 'color': (148, 163, 184),
            'title': "【在线无损感测】", 'lines': ["全程无物理碰撞阻碍，不降低带面物料滑行速度", "可同时监测金刚石、稀有矿石或精密合金构件"]
        },
        {
            'rel_pos': (0.75, 0.70), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【红石联动控制】", 'lines': ["输出 15 级强红石信号，直接激活活塞推杆、报警灯或分流器", "实现工件到达自动停机、定量计数与防漏料联动"]
        }
    ]
    compose_blueprint(img70, os.path.join(OUT_DIR, "content-observer-setup.png"), "物品探测器红石控制站蓝图 (Content Observer Setup)", l70, m70, ann70)

    # ================= 71. 黄铜高速漏斗与高吞吐装卸 =================
    b71 = [
        (0, 2, 0, "barrel"),
        (0, 1, 0, "copper_block"),
        (0, 0, 0, "stone_slab_top"),
        (1, 0, 0, "iron_block"),
        (-1, 0, 0, "iron_block")
    ]
    img71 = render_scene(b71, scale=3.8)
    l71 = [
        {
            'title': "第 1 层 (Y=1 底部高速流水线)",
            'note': "传送带平整贯穿漏斗下方，接纳吸料",
            'grid': [
                [ ('iron_block', '入料支架', (148, 163, 184, 255)), ('stone', '承接带面', (56, 189, 248, 255)), ('iron_block', '出料支架', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 黄铜高速漏斗中枢)",
            'note': "5 倍极速下料，右键配置过滤白名单",
            'grid': [
                [ None, ('copper_block', '黄铜漏斗', (249, 115, 22, 255)), None ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 顶层物料中转料仓)",
            'note': "大容量中转箱持续供给大宗货物",
            'grid': [
                [ None, ('barrel_top', '储料仓', (234, 179, 8, 255)), None ]
            ]
        }
    ]
    m71 = [
        "【黄铜高速漏斗】× 1（吞吐流速高达原版 5 倍，支持右键过滤）",
        "【进料储物仓】× 1（大容量中转箱，防积料外溢）",
        "【底层传送带】× 1（平稳承接整组高速倾泻的物料）"
    ]
    ann71 = [
        {
            'rel_pos': (0.50, 0.45), 'card_x': 1140, 'card_y': 200, 'color': (249, 115, 22),
            'title': "【5 倍速黄铜漏斗】", 'lines': ["由黄铜机壳与精密齿轮铣削而成，吞吐速度是原版漏斗的 5 倍", "单次瞬间抽取并喷吐成组货物，彻底根除产线拥堵卡料"]
        },
        {
            'rel_pos': (0.50, 0.18), 'card_x': 1140, 'card_y': 350, 'color': (234, 179, 8),
            'title': "【白名单精准抽取】", 'lines': ["右键打开过滤配置界面，直接手持目标物品设置白名单", "仅从上方大料仓抽取指定原料，杂质自动留存仓内"]
        },
        {
            'rel_pos': (0.50, 0.76), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【传送带极速送出】", 'lines': ["瞬间下落的物料在带面上快速成列排开", "与高速/极速传送带支架完美配合，吞吐能力翻倍提升"]
        }
    ]
    compose_blueprint(img71, os.path.join(OUT_DIR, "brass-hopper-setup.png"), "黄铜高速漏斗装卸工位蓝图 (Brass Hopper Setup)", l71, m71, ann71)

    # ================= 72. 红石请求器定额自动出料站 =================
    b72 = [
        (0, 0, -1, "barrel"),
        (0, 0, 0, "note_block"),
        (0, 1, 0, "lever"),
        (-1, 0, 1, "iron_block"),
        (0, 0, 1, "stone_slab_top"),
        (1, 0, 1, "iron_block"),
        (-1, 0, 2, "redstone_block")
    ]
    img72 = render_scene(b72, scale=3.8)
    l72 = [
        {
            'title': "第 1 层 (Y=1 容器、请求器与前出流水线)",
            'note': "背部紧贴大料箱，正面紧邻完整贯通成品流水线",
            'grid': [
                [ None, ('barrel_top', '后备料仓', (148, 163, 184, 255)), None ],
                [ None, ('note_block', '红石请求器', (239, 68, 68, 255)), None ],
                [ ('iron_block', '入料支架', (148, 163, 184, 255)), ('stone', '承接带面', (56, 189, 248, 255)), ('iron_block', '出料支架', (34, 197, 94, 255)) ],
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None, None ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 红石脉冲触发扳柄)",
            'note': "手持拉杆或红石线输入单次脉冲",
            'grid': [
                [ None, None, None ],
                [ None, ('lever', '控制扳手', (234, 179, 8, 255)), None ],
                [ None, None, None ],
                [ None, None, None ]
            ]
        }
    ]
    m72 = [
        "【红石请求器】× 1（红石脉冲触发，从后仓抽取定量工件喷出）",
        "【后备大料箱】× 1（储备大宗原材料）",
        "【承接传送带】× 1（前置完整流水线，接纳喷射出的物料）",
        "【红石控制端】× 1（接收车间触发信号）"
    ]
    ann72 = [
        {
            'target_block': (0, 0, 0), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【红石定额请求器】", 'lines': ["独立落地控制中枢，右键设置单次请求的目标货物", "接收到红石信号瞬间从背部料箱抓料并从正面喷出"]
        },
        {
            'target_block': (0, 0, -1), 'card_x': 1140, 'card_y': 350, 'color': (148, 163, 184),
            'title': "【后置大容量仓储】", 'lines': ["背部紧贴任何大容量箱子、货架或保险库", "避免人工频繁搬运，实现原料自动定额配给"]
        },
        {
            'target_block': (0, 0, 1), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【按需上料流水线】", 'lines': ["正前方铺设完整传送带，两端支架贯通闭合", "喷射出的物料落入带面平稳运往后级加工工段"]
        }
    ]
    compose_blueprint(img72, os.path.join(OUT_DIR, "redstone-requester-setup.png"), "红石请求器定额出料站蓝图 (Redstone Requester Setup)", l72, m72, ann72)

    # ================= 73. 工业状态指示灯巡检工作站 =================
    b73 = [
        (0, 0, 0, "blast_furnace"),
        (0, 1, 0, "redstone_lamp_on"),
        (0, 0, -1, "redstone_block"),
        (1, 0, 0, "barrel")
    ]
    img73 = render_scene(b73, scale=4.0)
    l73 = [
        {
            'title': "第 1 层 (Y=1 工作母机与电网接驳)",
            'note': "高炉后接电网，侧接原料收集箱",
            'grid': [
                [ ('redstone_block', '电网', (234, 179, 8, 255)), None ],
                [ ('blast_furnace', '工业高炉', (239, 68, 68, 255)), ('barrel_top', '储料仓', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 顶置状态指示灯)",
            'note': "贴合机器顶面，自动侦测设备工况",
            'grid': [
                [ None, None ],
                [ ('redstone_lamp_on', '状态指示灯', (56, 189, 248, 255)), None ]
            ]
        }
    ]
    m73 = [
        "【工业状态指示灯】× 1（贴近机器安装，实时反映运行状态）",
        "【工业冶炼高炉】× 1（被监控的核心工作母机）",
        "【供电线路】× 1（接入电网提供稳定电力）",
        "【储料箱】× 1（持续吞吐原料与成品）"
    ]
    ann73 = [
        {
            'rel_pos': (0.45, 0.28), 'card_x': 1140, 'card_y': 200, 'color': (56, 189, 248),
            'title': "【工业状态指示灯】", 'lines': ["紧贴工作母机顶面或侧面安装，完全不需要繁琐红石走线", "机器正常运转时常亮，缺电、卡料或故障时慢闪报警"]
        },
        {
            'rel_pos': (0.45, 0.60), 'card_x': 1140, 'card_y': 350, 'color': (239, 68, 68),
            'title': "【被监控工作母机】", 'lines': ["支持高炉、冲压机、拉丝机、水泵与搅拌机等全系工业设备", "旁边没有机器或断电时指示灯自动熄灭"]
        },
        {
            'rel_pos': (0.75, 0.65), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【车间全景目视巡检】", 'lines': ["在工厂中央控制台或走廊一眼望穿数十台机器工况", "哪台机器缺电停机瞬间定位，彻底消除隐蔽断料停产"]
        }
    ]
    compose_blueprint(img73, os.path.join(OUT_DIR, "status-lamp-monitoring-setup.png"), "工业状态指示灯巡检工作站蓝图 (Status Lamp Setup)", l73, m73, ann73)

    # ================= 74. 黏性动力活塞往复拉回机构 =================
    b74 = [
        (-1, 0, 0, "lightning_rod", 90, 90),
        (0, 0, 0, "sticky_piston", 0, 90),
        (1, 0, 0, "iron_block"),
        (0, 1, 0, "lever")
    ]
    img74 = render_scene(b74, scale=4.2)
    l74 = [
        {
            'title': "第 1 层 (Y=1 动力轴、黏性活塞与推拉工件)",
            'note': "传动轴同轴输入动能，活塞推拉前方工件",
            'grid': [
                [ ('lightning_rod', '传动轴', (249, 115, 22, 255)), ('piston_top_sticky', '黏性活塞', (34, 197, 94, 255)), ('iron_block', '推拉工件', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 红石控制手柄)",
            'note': "拉杆控制活塞伸出与缩回动作",
            'grid': [
                [ None, ('lever', '控制拉杆', (234, 179, 8, 255)), None ]
            ]
        }
    ]
    m74 = [
        "【黏性动力活塞】× 1（应力驱动+红石触发，推拉双向动作）",
        "【动力传动轴】× 1（向活塞持续注入 64 应力单位）",
        "【推拉受力方块】× 1（被活塞推移与拉回的目标构件）",
        "【红石拉杆】× 1（切换推移与复位状态）"
    ]
    ann74 = [
        {
            'rel_pos': (0.48, 0.48), 'card_x': 1140, 'card_y': 200, 'color': (34, 197, 94),
            'title': "【黏性动力活塞】", 'lines': ["背部接入旋转应力，顶部输入红石信号触发伸出", "头部涂抹强力胶质，不仅能向前推移，失电时更能拉回方块"]
        },
        {
            'rel_pos': (0.18, 0.52), 'card_x': 1140, 'card_y': 350, 'color': (249, 115, 22),
            'title': "【机械应力供给】", 'lines': ["单次推拉仅消耗 64 应力单位，转速决定活塞伸缩频率", "支持推拉长达 8 格整列方块链条"]
        },
        {
            'rel_pos': (0.80, 0.52), 'card_x': 1140, 'card_y': 500, 'color': (148, 163, 184),
            'title': "【往复循环机构】", 'lines': ["广泛应用于自动化折叠门、活动桥梁、矿车拦截闸门", "与循环推料工位无缝协同，打造全动态机械工厂"]
        }
    ]
    compose_blueprint(img74, os.path.join(OUT_DIR, "sticky-piston-setup.png"), "黏性动力活塞往复拉回机构蓝图 (Sticky Piston Setup)", l74, m74, ann74)

    # ================= 75. 直角齿轮箱与垂直伞齿轮换向系统 =================
    b75 = [
        (-1, -1, 0, "stone_bricks"), (0, -1, 0, "stone_bricks"), (0, -1, 1, "stone_bricks"),
        (-1, 0, 0, "lightning_rod", 90, 90),
        (0, 0, 0, "barrel"),
        (0, 0, 1, "lightning_rod", 90, 0),
        (0, 1, 0, "lightning_rod", 0, 0)
    ]
    img75 = render_scene(b75, scale=3.8)
    l75 = [
        {
            'title': "第 1 层 (Y=1 平整地基基座)",
            'note': "铺设坚固石砖承托转角齿轮箱",
            'grid': [
                [ ('stone_bricks', '基座', (148, 163, 184, 255)), ('stone_bricks', '基座', (148, 163, 184, 255)) ],
                [ None, ('stone_bricks', '基座', (148, 163, 184, 255)) ]
            ]
        },
        {
            'title': "第 2 层 (Y=2 齿轮箱、水平输入轴与偏转轴)",
            'note': "水平直线输入旋转动能，直角偏折 90° 导出",
            'grid': [
                [ ('lightning_rod', '输入轴', (249, 115, 22, 255)), ('barrel_top', '垂直齿轮箱', (239, 68, 68, 255)) ],
                [ None, ('lightning_rod', '直角偏转轴', (234, 179, 8, 255)) ]
            ]
        },
        {
            'title': "第 3 层 (Y=3 垂直换向输出传动轴)",
            'note': "伞齿轮向上垂直导出同速旋转动力",
            'grid': [
                [ None, ('lightning_rod', '垂直输出轴', (56, 189, 248, 255)) ],
                [ None, None ]
            ]
        }
    ]
    m75 = [
        "【垂直齿轮箱】× 1（精密伞齿轮构型，90° 动力换向中枢）",
        "【传动轴】× 3（水平输入轴、直角偏转轴与垂直输出轴）",
        "【稳固地基】× 3（承托重型换向机构）"
    ]
    ann75 = [
        {
            'rel_pos': (0.50, 0.50), 'card_x': 1140, 'card_y': 200, 'color': (239, 68, 68),
            'title': "【垂直齿轮箱】", 'lines': ["内部嵌装 45° 咬合的耐磨伞齿轮组，转速与应力 1:1 无损传递", "手持工业扳手右键敲击外壳，可随时翻转齿轮轴心朝向"]
        },
        {
            'rel_pos': (0.20, 0.45), 'card_x': 1140, 'card_y': 350, 'color': (249, 115, 22),
            'title': "【水平输入与偏折】", 'lines': ["同轴接入水车或蒸汽引擎旋转动力", "可沿水平直角偏折 90° 导出，轻松绕开障碍墙体"]
        },
        {
            'rel_pos': (0.50, 0.18), 'card_x': 1140, 'card_y': 500, 'color': (56, 189, 248),
            'title': "【立式垂直换向】", 'lines': ["顶部立式接出垂直转轴，将地面旋转动力一路向上传输", "完美驱动楼上高位冲压机、搅拌机与飞轮蓄能机组"]
        }
    ]
    compose_blueprint(img75, os.path.join(OUT_DIR, "gearbox-transmission-setup.png"), "直角齿轮箱与垂直换向系统蓝图 (Gearbox Setup)", l75, m75, ann75)

    print("Batch 5 blueprints successfully generated!")

if __name__ == "__main__":
    generate_batch5()
