"""
Z-Tech 维基示意图场景。

方块一律使用插件放置后的真实原版方块（见各机器注册的材质），
摆法按插件代码的实际判定编写；编号与维基正文图例一一对应。

坐标：+x 东（图中右下）、+z 南（图中左下）、+y 上；y=0 为地面层。
看得到的是方块的南面与东面，所以机器正面尽量朝南或朝东。
"""
from .compose import Scene

# ---------------------------------------------------------------- 插件方块外观
BRACKET = "iron_block"                       # 传送带支架（三档同外观）
BELT = "stone_slab[type=top]"                # 传送带半砖
CUBE = "iron_block"                          # 储能方块
CABLE = "redstone_wire"                      # 电缆
VCABLE = "chain[axis=y]"                     # 竖直电缆
PIPE = "glass"                               # 液体管
RPIPE = "tinted_glass"                       # 加强液体管
TANK = "blue_stained_glass"                  # 液体储罐
PUMP = "stone_bricks"                        # 抽水泵
LAVA_PUMP = "nether_bricks"                  # 岩浆泵
DEPOT = "polished_andesite_slab[type=bottom]"
CHEST = "barrel[facing=up]"            # 容器（箱子是实体渲染，示意图统一用木桶）
BARREL = "barrel[facing=up]"


def machine(facing="south"):
    """发射器材质的机器（粉碎机、冲压机、拉丝机、部署器、机械臂、石磨……）"""
    return f"dispenser[facing={facing}]"


def furnace(facing="south", lit=False):
    return f"furnace[facing={facing},lit={'true' if lit else 'false'}]"


def shaft(axis):
    return {"x": "lightning_rod[facing=east]", "z": "lightning_rod[facing=south]", "y": "lightning_rod[facing=up]"}[axis]


def belt_x(x0, x1, y=0, z=0):
    """x0、x1 处为支架，中间铺半砖"""
    out = [(x0, y, z, BRACKET), (x1, y, z, BRACKET)]
    out += [(x, y, z, BELT) for x in range(x0 + 1, x1)]
    return out


def belt_z(z0, z1, x=0, y=0):
    out = [(x, y, z0, BRACKET), (x, y, z1, BRACKET)]
    out += [(x, y, z, BELT) for z in range(z0 + 1, z1)]
    return out


def cable(points, y=0):
    return [(x, y, z, CABLE) for x, z in points]


# ---------------------------------------------------------------- 自动连接
_REDSTONE_PARTNERS = ("lever", "daylight_detector", "observer", "comparator", "redstone_block", "redstone_torch", "note_block")


def _connect(blocks):
    pos = {(x, y, z): s for x, y, z, s in blocks}
    out = []
    dirs = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
    opp = {"north": "south", "south": "north", "west": "east", "east": "west"}
    for x, y, z, s in blocks:
        bid = s.split("[")[0]
        if s == CABLE:
            conn = {}
            for d, (dx, dz) in dirs.items():
                n = pos.get((x + dx, y, z + dz))
                if n and (n == CABLE or n.split("[")[0] in _REDSTONE_PARTNERS):
                    conn[d] = "side"
                elif pos.get((x + dx, y - 1, z + dz)) == CABLE:
                    conn[d] = "side"
                elif pos.get((x + dx, y + 1, z + dz)) == CABLE:
                    conn[d] = "up"
            if len(conn) == 1:  # 原版：只连一侧时向两端延伸
                d = next(iter(conn))
                conn[opp[d]] = "side"
            props = ",".join(f"{d}={conn.get(d, 'none')}" for d in dirs)
            s = f"redstone_wire[{props},power=7]"  # 实际无红石信号时更暗，这里调亮便于辨认
        elif bid in ("iron_bars", "oak_fence") and "[" not in s:
            conn = []
            for d, (dx, dz) in dirs.items():
                n = pos.get((x + dx, y, z + dz))
                if n and n.split("[")[0] not in ("air", "redstone_wire", "lightning_rod"):
                    conn.append(f"{d}=true")
            s = f"{bid}[{','.join(conn)}]" if conn else bid
        out.append((x, y, z, s))
    return out


def S(name, blocks, labels, legend, **kw):
    return Scene(name, _connect(blocks), labels=labels, legend=legend, **kw)


SCENES = []


def scene(fn):
    SCENES.append(fn)
    return fn

# ================================================================ 开荒

@scene
def first_power():
    b = [(0, 0, 0, furnace(lit=True))] + cable([(1, 0), (2, 0), (3, 0)]) + [
        (4, 0, 0, machine()), (4, 0, -1, CUBE)]
    return S("first-power", b, {1: (0, 0, 0), 2: (2, 0, 0), 3: (4, 0, 0), 4: (4, 0, -1)}, {
        1: "土制燃煤发电机：放入煤炭或木炭后发电",
        2: "电缆：铺设方式与红石粉相同，用于连接发电机与机器",
        3: "粉碎机：装入研磨头后，可将 1 份粗铁或粗铜粉碎为 2 份矿粉",
        4: "储能方块（可选）：储存多余电力，机器优先从储能方块取电",
    })


@scene
def starter_millstone():
    b = [(0, 0, 0, "lever[face=floor,facing=east]"), (1, 0, 0, shaft("x")), (2, 0, 0, machine())]
    return S("starter-millstone", b, {1: (0, 0, 0), 2: (1, 0, 0), 3: (2, 0, 0)}, {
        1: "手摇曲柄：空手右键摇动，每次持续约 5 秒",
        2: "传动轴",
        3: "石磨磨坊：处理圆石、砂砾、骨头、黑曜石等材料",
    }, scale=72)

# ================================================================ 电力

@scene
def power_grid():
    b = [(0, 0, 0, furnace(lit=True))] + cable([(1, 0), (2, 0)]) + [
        (3, 0, 0, CUBE),
        (4, 0, 0, VCABLE), (4, 1, 0, VCABLE), (4, 2, 0, VCABLE),
        (4, 3, 0, machine()),
    ]
    return S("power-grid", b, {1: (0, 0, 0), 2: (1, 0, 0), 3: (3, 0, 0), 4: (4, 1, 0), 5: (4, 3, 0)}, {
        1: "发电机",
        2: "电缆：仅可铺设于地面",
        3: "储能方块：相邻即连通，同时可作为电网中继",
        4: "竖直电缆：外观为锁链，向上叠放，用于沿墙或跨楼层布线",
        5: "上层机器：与竖直电缆顶端相邻即可取电",
    })


@scene
def generators_fuel():
    b = [
        (0, 0, 0, "lever[face=floor,facing=south]"),
        (2, 0, 0, furnace(lit=True)),
        (4, 0, 0, furnace(lit=True)), (4, 0, -1, PIPE),
        (6, 0, 0, furnace(lit=True)),
        (8, 0, 0, furnace(lit=True)),
    ]
    return S("generators-fuel", b, {1: (0, 0, 0), 2: (2, 0, 0), 3: (4, 0, 0), 4: (6, 0, 0), 5: (8, 0, 0), 6: (4, 0, -1)}, {
        1: "手摇发电机：空手右键一次发电 20 RF",
        2: "土制燃煤发电机：燃烧煤炭、木炭等燃料，3 RF/t",
        3: "简易蒸汽机：消耗燃料与水，4 RF/t",
        4: "蒸汽锅炉：消耗燃料与水，12 RF/t",
        5: "生物燃油发电机：燃烧海带、种子、作物等植物类燃料，5 RF/t",
        6: "液体管：可为简易蒸汽机与蒸汽锅炉供水，替代手动放入水桶",
    })


@scene
def generators_natural():
    b = [
        (0, 0, 0, "spruce_log[axis=x]"), (0, 0, 1, "water"), (1, 0, 1, "water"), (-1, 0, 1, "water"),
        (3, 0, 0, "crying_obsidian"), (3, 0, 1, "lava"), (4, 0, 1, "lava"),
        (6, 0, 0, "daylight_detector"),
        (9, 0, 0, "oak_fence"), (9, 1, 0, "oak_fence"), (9, 2, 0, "oak_fence"), (9, 3, 0, "lightning_rod[facing=up]"),
    ]
    return S("generators-natural", b, {1: (0, 0, 0), 2: (3, 0, 0), 3: (6, 0, 0), 4: (9, 3, 0)}, {
        1: "水车：周围存在水源方块时发电（流动水不计），3 RF/t",
        2: "热力发电机：周围存在岩浆源时发电，6 RF/t",
        3: "太阳能板：白天且上方无遮挡时发电，4 RF/t",
        4: "风力发电机：发电量取决于所在高度，Y64 以下不发电",
    })


@scene
def steam_turbine():
    b = [(0, 0, 0, "water"), (1, 0, 0, PUMP), (2, 0, 0, PIPE), (3, 0, 0, PIPE), (4, 0, 0, furnace(lit=True)),
         (4, 0, -1, CUBE)] + cable([(1, -1), (2, -1), (3, -1)])
    return S("steam-turbine", b, {1: (0, 0, 0), 2: (1, 0, 0), 3: (2, 0, 0), 4: (4, 0, 0), 5: (4, 0, -1)}, {
        1: "水源",
        2: "抽水泵：耗电 2 RF/t",
        3: "液体管：末端与蒸汽轮机相邻",
        4: "蒸汽轮机：有水送入时持续发电，8 RF/t",
        5: "储能方块：储存轮机产出的电力，同时为抽水泵供电",
    })

# ================================================================ 应力

@scene
def stress_basics():
    b = [(0, 0, 0, "lever[face=floor,facing=east]"), (1, 0, 0, shaft("x")), (2, 0, 0, shaft("x")), (3, 0, 0, shaft("x")),
         (4, 0, 0, machine())]
    return S("stress-basics", b, {1: (0, 0, 0), 2: (2, 0, 0), 3: (4, 0, 0)}, {
        1: "动力源（图中为手摇曲柄）",
        2: "传动轴：首尾相接，沿直线排列",
        3: "应力机器（图中为石磨磨坊）",
    })


@scene
def stress_gears():
    b = [(0, 0, 0, "blast_furnace[facing=south,lit=true]"), (1, 0, 0, shaft("x")), (2, 0, 0, "carved_pumpkin[facing=south]"),
         (3, 0, 0, shaft("x")), (4, 0, 0, machine()),
         (0, 0, 2, "blast_furnace[facing=south,lit=true]"), (1, 0, 2, shaft("x")), (2, 0, 2, "pumpkin"),
         (3, 0, 2, shaft("x")), (4, 0, 2, machine())]
    return S("stress-gears", b, {1: (0, 0, 0), 2: (2, 0, 0), 3: (4, 0, 0), 4: (2, 0, 2), 5: (4, 0, 2)}, {
        1: "蒸汽引擎：64 RPM",
        2: "小齿轮：下游转速 ×2，下游机器的应力消耗同样 ×2",
        3: "该机器以 128 RPM 运转",
        4: "大齿轮：下游转速 ×0.5，应力消耗同样 ×0.5",
        5: "该机器以 32 RPM 运转，应力消耗减半",
    })


@scene
def vertical_gearbox():
    b = [(0, 0, 0, "blast_furnace[facing=south,lit=true]"), (1, 0, 0, shaft("x")), (2, 0, 0, "barrel[facing=up]"),
         (2, 1, 0, shaft("y")), (2, 2, 0, shaft("y")), (2, 3, 0, machine()),
         (1, 2, 0, "smooth_stone"), (1, 2, -1, "smooth_stone"), (2, 2, -1, "smooth_stone"), (3, 2, -1, "smooth_stone"), (3, 2, 0, "smooth_stone")]
    return S("vertical-gearbox", b, {1: (1, 0, 0), 2: (2, 0, 0), 3: (2, 1, 0), 4: (2, 3, 0)}, {
        1: "水平传动轴",
        2: "垂直齿轮箱：将水平方向的转动转向竖直方向，反之亦可",
        3: "竖直传动轴",
        4: "上层的应力机器",
    })


@scene
def wall_bearing():
    b = [(0, 0, 0, shaft("x")), (1, 0, 0, "iron_bars"), (2, 0, 0, shaft("x")),
         (1, 0, -1, "stone_bricks"), (1, 0, 1, "stone_bricks"), (1, 1, -1, "stone_bricks"), (1, 1, 0, "stone_bricks"),
         (1, 1, 1, "stone_bricks"), (1, 0, -2, "stone_bricks"), (1, 1, -2, "stone_bricks")]
    return S("wall-bearing", b, {1: (1, 0, 0), 2: (2, 0, 0)}, {
        1: "穿墙轴承：嵌于墙洞内，以 1:1 传递转动",
        2: "墙两侧的传动轴对准轴承",
    }, scale=64)


@scene
def clutch_flywheel():
    b = [(0, 0, 0, "blast_furnace[facing=south,lit=true]"), (1, 0, 0, shaft("x")), (2, 0, 0, "repeater[facing=west]"),
         (3, 0, 0, shaft("x")), (4, 0, 0, "grindstone[face=floor,facing=east]"), (5, 0, 0, shaft("x")), (6, 0, 0, machine())]
    return S("clutch-flywheel", b, {1: (2, 0, 0), 2: (4, 0, 0), 3: (6, 0, 0)}, {
        1: "离合器：空手右键切换接合与分离，分离后下游停转",
        2: "飞轮：有动力时蓄能，动力源停止后以 16 RPM 持续运转一段时间",
        3: "下游机器",
    })


@scene
def stress_sources_natural():
    b = [(0, 0, 0, "water"), (1, 0, 0, "water"), (-1, 0, 0, "water"), (0, 1, 0, "spruce_log[axis=x]"), (1, 1, 0, shaft("x")),
         (4, 0, 0, "oak_log[axis=y]"), (4, 1, 0, "oak_log[axis=y]"), (4, 2, 0, "oak_log[axis=y]"), (4, 3, 0, "white_wool"),
         (5, 3, 0, shaft("x")),
         (8, 0, 0, "spruce_log[axis=x]"), (8, 0, 1, "water"), (9, 0, 0, shaft("x"))]
    return S("stress-sources-natural", b, {1: (0, 1, 0), 2: (4, 3, 0), 3: (8, 0, 0)}, {
        1: "大型水车：周围 5×5×5 范围内存在水（含流动水）时运转，32 RPM · 4096 SU",
        2: "风车：上方露天或位于 Y100 及以上时运转，32 RPM · 4096 SU",
        3: "水车：周围存在水源方块时运转，32 RPM · 2048 SU，同时可发电",
    })


@scene
def stress_sources_engine():
    b = [(0, 0, 0, "blast_furnace[facing=south,lit=true]"), (1, 0, 0, shaft("x")), (2, 0, 0, shaft("x")),
         (5, 0, 0, CUBE), (6, 0, 0, CABLE), (7, 0, 0, "waxed_copper_block"), (8, 0, 0, shaft("x")), (9, 0, 0, shaft("x"))]
    return S("stress-sources-engine", b, {1: (0, 0, 0), 2: (7, 0, 0), 3: (6, 0, 0)}, {
        1: "蒸汽引擎：放入煤炭或木炭后运转，64 RPM · 4096 SU，无需供水",
        2: "动力曲柄箱：消耗电力输出转动，32 RPM · 2048 SU",
        3: "动力曲柄箱需接入电网，耗电 12 RF/t",
    })


@scene
def stress_dynamo():
    b = [(0, 0, 0, "blast_furnace[facing=south,lit=true]"), (1, 0, 0, shaft("x")), (2, 0, 0, machine()),
         (3, 0, 0, CABLE), (4, 0, 0, CUBE)]
    return S("stress-dynamo", b, {1: (0, 0, 0), 2: (2, 0, 0), 3: (4, 0, 0)}, {
        1: "动力源",
        2: "应力发电机：发电量（RF/t）= 转速（上限 64）÷ 10",
        3: "电网（储能方块）",
    })


@scene
def gauges():
    b = [(0, 0, 0, "lever[face=floor,facing=east]"), (1, 0, 0, shaft("x")), (2, 0, 0, shaft("x")), (3, 0, 0, shaft("x")),
         (4, 0, 0, machine()), (1, 1, 0, "quartz_block"), (2, 1, 0, "quartz_block")]
    return S("gauges", b, {1: (1, 1, 0), 2: (2, 1, 0)}, {
        1: "转速表：与任意应力方块相邻，上方显示转速",
        2: "应力表：与任意应力方块相邻，上方显示应力需求与供给，超载时显示为红色",
    }, scale=64)

# ================================================================ 加工

@scene
def inline_processing():
    b = belt_x(0, 5) + [(1, 1, 0, machine()), (2, 1, 0, machine()), (3, 1, 0, machine()), (4, 1, 0, machine()),
                        (0, 1, 0, CUBE), (-1, 0, 0, furnace(lit=True)), (6, 0, 0, CHEST)]
    return S("inline-processing", b, {1: (1, 1, 0), 2: (2, 1, 0), 3: (3, 1, 0), 4: (4, 1, 0), 5: (0, 1, 0), 6: (-1, 0, 0), 7: (6, 0, 0)}, {
        1: "粉碎机",
        2: "液压冲压机",
        3: "拉丝机",
        4: "动力锯",
        5: "储能方块：同时与支架和第一台机器相邻；相邻的加工机之间可相互传电",
        6: "发电机",
        7: "末端容器：加工完成的物品存入此处",
    }, arrows=[((0.5, 0.75, 1.3), (5.0, 0.75, 1.3))])


@scene
def depot_press():
    b = [(0, 0, 0, DEPOT), (0, 2, 0, machine("down")), (0, 0, -1, "stone_bricks"), (0, 1, -1, "stone_bricks"), (0, 2, -1, CUBE),
         (3, 0, 0, DEPOT), (3, 2, 0, machine("down")), (3, 3, 0, shaft("y")), (3, 0, -1, "stone_bricks"), (3, 1, -1, "stone_bricks"),
         (3, 2, -1, "stone_bricks")]
    return S("depot-press", b, {1: (0, 0, 0), 2: (0, 1, 0), 3: (0, 2, 0), 4: (0, 2, -1), 5: (3, 2, 0), 6: (3, 3, 0)}, {
        1: "置物台：手持物品右键放置",
        2: "机器与置物台之间可留空一格，也可直接相邻",
        3: "液压冲压机（电力）：位于置物台正上方 1～2 格内",
        4: "储能方块或电缆：为液压冲压机供电",
        5: "机械压榨机（应力）：同样位于置物台正上方 1～2 格内",
        6: "传动轴：接入应力网络",
    })


@scene
def deployer():
    b = belt_x(0, 4) + [(2, 0, -1, machine("south")), (2, 1, -1, shaft("y")), (2, 2, -1, shaft("y")),
                        (1, 0, 1, machine("north")), (1, 1, 1, shaft("y"))]
    return S("deployer", b, {1: (2, 0, -1), 2: (1, 0, 1), 3: (2, 2, -1), 4: (3, 0, 0)}, {
        1: "部署器：位于传送带半砖侧面，与半砖同一高度，正面朝向半砖",
        2: "传送带另一侧亦可放置，按物品经过的顺序依次加工",
        3: "部署器由应力驱动",
        4: "传送带本身仍需通电",
    }, arrows=[((0.5, 0.75, 0.5), (4.0, 0.75, 0.5))])


@scene
def spout():
    b = belt_x(0, 4) + [(2, 1, 0, machine("down")), (2, 2, 0, PIPE), (2, 2, -1, PIPE), (2, 1, -1, PIPE),
                        (2, 0, -1, PUMP), (3, 0, -1, "water")]
    return S("spout", b, {1: (2, 1, 0), 2: (2, 2, -1), 3: (2, 0, -1), 4: (3, 0, -1)}, {
        1: "注液器：位于传送带半砖或置物台正上方",
        2: "液体管：连接注液器顶部或侧面",
        3: "抽水泵：需接入电网",
        4: "水源",
    })


@scene
def blower():
    b = [(0, 0, 0, shaft("x")), (1, 0, 0, machine("east")), (5, 0, 0, "fire"), (5, -1, 0, "netherrack"),
         (0, 0, 2, shaft("x")), (1, 0, 2, machine("east")), (5, 0, 2, "water")]
    return S("blower", b, {1: (1, 0, 0), 2: (5, 0, 0), 3: (1, 0, 2), 4: (5, 0, 2)}, {
        1: "鼓风机：朝放置时玩家面对的方向吹出 8 格气流，由应力驱动",
        2: "气流路径中有火、岩浆或岩浆块时：气流范围内的掉落物被烧炼",
        3: "另一台鼓风机",
        4: "气流路径中有水时：红沙与砂砾被淘洗为沙子",
    }, arrows=[((1.9, 0.5, 0.5), (4.6, 0.5, 0.5)), ((1.9, 0.5, 2.5), (4.6, 0.5, 2.5))])


@scene
def cooling_tower():
    b = [(0, 0, 0, machine()), (1, 0, 0, "snow_block"), (1, 1, 0, PIPE), (1, 1, -1, PIPE)]
    return S("cooling-tower", b, {1: (0, 0, 0), 2: (1, 0, 0), 3: (1, 1, 0)}, {
        1: "超频的加工机",
        2: "冷却塔：与加工机相邻放置",
        3: "液体管：为冷却塔供水",
    }, scale=64)

# ================================================================ 冶炼

@scene
def smeltery():
    b = [(0, 0, 0, furnace(lit=True)), (-1, 0, 0, "blast_furnace[facing=south]"), (1, 0, 0, "blast_furnace[facing=south]"),
         (0, 0, -1, "blast_furnace[facing=south]"), (0, 1, 0, "blast_furnace[facing=south]")] + cable([(0, 1), (0, 2)]) + [
        (0, 0, 3, furnace(lit=True)),
        (4, 0, 0, "smoker[facing=south,lit=true]"), (3, 0, 0, "blast_furnace[facing=south]"), (5, 0, 0, "blast_furnace[facing=south]"),
        (4, 0, -1, "blast_furnace[facing=south]"), (4, 1, 0, "blast_furnace[facing=south]")] + cable([(4, 1), (4, 2)]) + [
        (4, 0, 3, furnace(lit=True))]
    return S("smeltery", b, {1: (0, 0, 0), 2: (0, 1, 0), 3: (0, 0, 2), 4: (4, 0, 0)}, {
        1: "锻造炉核心",
        2: "加热模块：贴于核心任意一面，每个使速度提高 50%",
        3: "电缆：需直接连接核心（加热模块不导电）",
        4: "合金炉核心：搭建方式与锻造炉相同",
    })


@scene
def blast_furnace():
    b = [(0, 1, 0, "blast_furnace[facing=south,lit=true]"), (0, 2, 0, "hopper[facing=down]"), (1, 1, 0, "hopper[facing=west]"),
         (0, 0, 0, "hopper[facing=east]"), (1, 0, 0, CHEST)]
    return S("blast-furnace", b, {1: (0, 1, 0), 2: (0, 2, 0), 3: (1, 1, 0), 4: (0, 0, 0), 5: (1, 0, 0)}, {
        1: "高炉",
        2: "顶部漏斗：送入粗矿",
        3: "侧面漏斗：送入燃料",
        4: "底部漏斗：抽出成品",
        5: "成品容器",
    }, scale=64)

# ================================================================ 传送带

@scene
def belt_basic():
    b = [(0, 0, 0, CHEST)] + belt_x(1, 5) + [(6, 0, 0, CHEST)] + cable([(1, 1), (1, 2)]) + [(1, 0, 3, furnace(lit=True))]
    return S("belt-basic", b, {1: (1, 0, 0), 2: (3, 0, 0), 3: (5, 0, 0), 4: (0, 0, 0), 5: (6, 0, 0), 6: (1, 0, 2)}, {
        1: "起点支架",
        2: "传送带半砖（上半砖）",
        3: "终点支架",
        4: "起点支架后方的容器：传送带从中逐个取货",
        5: "终点外侧的容器：物品到达后自动存入",
        6: "电缆：连接任意一端的支架",
    }, arrows=[((1.6, 0.75, 0.5), (4.4, 0.75, 0.5))])


@scene
def belt_corner():
    b = belt_x(0, 4) + belt_z(-1, 3, x=5)
    return S("belt-corner", b, {1: (4, 0, 0), 2: (5, 0, 0)}, {
        1: "第一条传送带的终点支架",
        2: "终点支架正前方的格子须为第二条传送带的半砖",
    }, arrows=[((0.8, 0.75, 0.5), (4.2, 0.75, 0.5)), ((5.5, 0.75, 0.6), (5.5, 0.75, 2.6))])


@scene
def loader_unloader():
    b = belt_x(0, 5) + [(2, 0, -1, machine("south")), (2, 0, -2, CHEST), (6, 0, 0, "dropper[facing=east]"), (7, 0, 0, CHEST)]
    return S("loader-unloader", b, {1: (2, 0, -1), 2: (2, 0, -2), 3: (6, 0, 0), 4: (7, 0, 0)}, {
        1: "装载机：正面朝向半砖",
        2: "装载机后方的容器",
        3: "卸载机：位于终点支架外侧，正面朝向目标容器",
        4: "目标容器",
    }, arrows=[((0.6, 0.75, 0.5), (5.0, 0.75, 0.5))])


@scene
def tunnel():
    b = belt_x(0, 5) + [(2, 1, 0, "andesite"), (3, 1, 0, "andesite")]
    return S("tunnel", b, {1: (2, 1, 0)}, {
        1: "传送带隧道：覆盖于半砖正上方，该段运输速度提高至 1.5 倍",
    }, scale=64)


@scene
def ramp_belt():
    b = belt_x(0, 3) + [(4, 0, 0, "stone_stairs[facing=east]"), (5, 1, 0, "stone_stairs[facing=east]"),
                        (6, 2, 0, "stone_stairs[facing=east]"), (7, 2, 0, CHEST)] + cable([(3, 1), (4, 1)])
    return S("ramp-belt", b, {1: (3, 0, 0), 2: (4, 0, 0), 3: (6, 2, 0), 4: (7, 2, 0), 5: (4, 0, 1)}, {
        1: "水平传送带的终点支架",
        2: "倾斜传送带最下一级（驱动端）",
        3: "逐级向上铺设，至少 2 级",
        4: "顶端外侧可连接容器、传送带或机器",
        5: "上坡运输需供电，电源接于驱动端旁；下坡运输不耗电",
    }, arrows=[((4.5, 1.0, 0.5), (6.5, 3.0, 0.5))])


@scene
def slide_rail():
    b = [(x, 0, 0, "smooth_stone") for x in range(0, 4)] + belt_x(0, 3, y=1) + [
        (4, 1, 0, "sandstone_stairs[facing=west]"), (5, 0, 0, "sandstone_stairs[facing=west]"), (4, 0, 0, "smooth_stone"),
        (6, 0, 0, CHEST)]
    return S("slide-rail", b, {1: (4, 1, 0), 2: (5, 0, 0), 3: (6, 0, 0)}, {
        1: "滑轨第一级：紧邻传送带终点支架外侧",
        2: "逐级向下铺设，可转弯；物品仅能由高处滑向低处，不耗电",
        3: "底端外侧放置容器",
    }, arrows=[((4.5, 1.6, 0.5), (5.8, 0.6, 0.5))])


@scene
def vertical_belt():
    b = belt_x(0, 2) + [(3, y, 0, "polished_basalt[axis=y]") for y in range(4)] + [
        (4, 3, 0, CHEST), (4, 0, 0, "stone_bricks"), (4, 1, 0, "stone_bricks"), (4, 2, 0, "stone_bricks")] + cable([(3, 1), (2, 1)])
    return S("vertical-belt", b, {1: (2, 0, 0), 2: (3, 1, 0), 3: (3, 0, 0), 4: (4, 3, 0), 5: (3, 0, 1)}, {
        1: "水平传送带终点紧邻垂直传送带，物品自动转入",
        2: "垂直传送带：沿竖直方向叠放，自动连接为一列",
        3: "最下一节为驱动端",
        4: "顶端旁可连接容器、机器或传送带半砖",
        5: "驱动端旁接入电网：向上运输 2 RF/t，向下运输不耗电",
    }, arrows=[((3.5, 0.6, 1.1), (3.5, 3.6, 1.1))])


@scene
def item_splitter():
    b = [(x, 0, 0, "smooth_stone") for x in range(0, 6)] + belt_x(0, 5, y=1) + [
        (2, 2, 0, "observer[facing=south]"), (2, 1, 1, "sandstone_stairs[facing=north]"), (2, 0, 2, "sandstone_stairs[facing=north]"),
        (2, 0, 1, "smooth_stone"), (2, 0, 3, CHEST)]
    return S("item-splitter", b, {1: (2, 2, 0), 2: (2, 1, 1), 3: (2, 0, 3)}, {
        1: "物品分流器：位于半砖正上方，正面朝向分流方向（可用扳手旋转）",
        2: "分流方向上紧邻的滑轨或倾斜传送带：白名单物品转入该线路",
        3: "滑轨末端的容器",
    }, arrows=[((0.6, 1.75, 0.5), (5.0, 1.75, 0.5)), ((2.5, 1.7, 0.9), (2.5, 0.8, 2.6))])


@scene
def sorting_machine():
    b = belt_x(0, 4) + [(2, 1, 0, machine("up"))]
    return S("sorting-machine", b, {1: (2, 1, 0)}, {
        1: "分拣机：位于半砖正上方，可为前、后、左、右四个方向分别指定物品",
    }, arrows=[((2.5, 1.0, 1.0), (2.5, 1.0, 2.6)), ((2.5, 1.0, 0.0), (2.5, 1.0, -1.4)), ((0.6, 0.75, 1.1), (4.2, 0.75, 1.1))], scale=64)


@scene
def observer_flowmeter():
    b = belt_x(0, 4) + [(2, 0, 1, "lever[face=wall,facing=south,powered=true]"), (2, 0, 2, CABLE.replace("wire", "wire")),
                        (2, 0, 3, "redstone_lamp[lit=true]"), (3, 1, 0, "comparator[facing=south]")]
    return S("observer-flowmeter", b, {1: (2, 0, 1), 2: (2, 0, 3), 3: (3, 1, 0)}, {
        1: "物品探测器：贴于半砖侧面，检测到目标物品时输出红石信号",
        2: "由信号点亮的红石灯",
        3: "流量计：位于半砖正上方，右键可查看流量，有物品通过时输出红石信号",
    }, scale=64)

# ================================================================ 仓储与自动化

@scene
def chute():
    b = belt_x(-1, 2) + [(0, 1, 0, "hopper[facing=down]"), (0, 2, 0, "hopper[facing=down]"), (0, 3, 0, CHEST)]
    return S("chute", b, {1: (0, 3, 0), 2: (0, 2, 0), 3: (0, 1, 0), 4: (0, 0, 0)}, {
        1: "顶部容器",
        2: "智能溜槽：仅放行白名单内的物品",
        3: "溜槽：竖直叠放，不耗电",
        4: "底端正对传送带半砖时，物品直接落到传送带上",
    }, scale=64)


@scene
def mechanical_arm():
    b = belt_x(0, 4) + [(2, 0, -2, machine("south")), (2, 0, -3, CHEST)]
    return S("mechanical-arm", b, {1: (2, 0, -2), 2: (2, 0, 0), 3: (2, 0, -3)}, {
        1: "机械臂：正面朝向传送带，沿正面方向最远 4 格",
        2: "抓取位置：正面方向上的第一格半砖",
        3: "后方 1～3 格内的容器、加工机或发电机",
    }, arrows=[((2.5, 0.9, 0.4), (2.5, 0.9, -2.1))])


@scene
def auto_crafter():
    b = [(0, 0, 0, machine()), (0, 0, -1, CHEST), (0, 0, 1, CHEST)] + cable([(1, 0), (2, 0)]) + [(3, 0, 0, CUBE)]
    return S("auto-crafter", b, {1: (0, 0, 0), 2: (0, 0, -1), 3: (0, 0, 1), 4: (3, 0, 0)}, {
        1: "自动合成器：右键设置 3×3 配方模板",
        2: "后方 1～3 格内的原料容器",
        3: "正面的容器或传送带：接收成品",
        4: "电网：每次合成耗电 80 RF",
    }, scale=64)


@scene
def item_vault():
    b = [(0, 0, 0, BARREL), (1, 0, 0, BARREL), (0, 0, 1, BARREL), (1, 0, 1, BARREL), (2, 0, 0, BARREL),
         (0, 1, 0, "hopper[facing=down]"), (0, 2, 0, CHEST)]
    return S("item-vault", b, {1: (1, 0, 1), 2: (0, 1, 0)}, {
        1: "物品保险库：水平相邻的保险库自动成组，库存在组内自动均摊",
        2: "溜槽：自顶部向保险库送货",
    }, scale=64)


@scene
def storage_misc():
    b = [(0, 0, 0, "bookshelf"), (1, 0, 0, "bookshelf"), (0, 1, 0, "bookshelf"), (1, 1, 0, "bookshelf"),
         (4, 0, 0, CHEST), (4, 1, 0, "copper_block"),
         (7, 0, 0, CHEST), (7, 0, 1, "note_block"), (7, 1, 1, "lever[face=floor,facing=south]")]
    return S("storage-misc", b, {1: (1, 1, 0), 2: (4, 1, 0), 3: (4, 0, 0), 4: (7, 0, 1), 5: (7, 0, 0)}, {
        1: "货架：每个仅存放一种物品，最多 576 个",
        2: "黄铜漏斗：吸取上方及周围的掉落物",
        3: "黄铜漏斗下方须为容器",
        4: "红石请求器：收到红石信号时取出一组指定物品并从正面抛出",
        5: "请求器后方的容器",
    })


@scene
def harvester():
    b = [(2, 0, 2, "hay_block[axis=y]")]
    for x in range(5):
        for z in range(5):
            if (x, z) != (2, 2):
                b.append((x, -1, z, "farmland[moisture=7]"))
                b.append((x, 0, z, "wheat[age=7]"))
    return S("harvester", b, {1: (2, 0, 2), 2: (0, 0, 4)}, {
        1: "自动收割机：收割周围 9×9 范围内（同层及上一层）的成熟作物并补种",
        2: "成熟作物被收割后，掉落物留在原位",
    }, floor="dirt", scale=48)


@scene
def seeder():
    b = [(2, 0, 2, machine("up")), (2, 1, 2, "hopper[facing=down]"), (3, 0, 2, CUBE)]
    for x in range(5):
        for z in range(5):
            if (x, z) in ((2, 2), (3, 2)):
                continue
            b.append((x, -1, z, "farmland[moisture=7]"))
            if x + z < 5:
                b.append((x, 0, z, "wheat[age=1]"))
    return S("seeder", b, {1: (2, 0, 2), 2: (2, 1, 2), 3: (3, 0, 2), 4: (0, 0, 3), 5: (4, 0, 4)}, {
        1: "自动播种机：在周围 9×9 范围内与其同层或低一层的空耕地上播种",
        2: "漏斗或溜槽：向播种机补充种子",
        3: "电网：每播种一株耗电 10 RF",
        4: "已播种的耕地",
        5: "尚未播种的耕地",
    }, floor="dirt", scale=48)


@scene
def plough():
    b = [(0, 0, 0, "polished_andesite"), (-1, 0, 0, shaft("x"))]
    for x in range(1, 6):
        for z in range(-2, 3):
            b.append((x, 0, z, "farmland" if x <= 3 else "grass_block"))
    return S("plough", b, {1: (0, 0, 0), 2: (-1, 0, 0), 3: (2, 0, 0), 4: (5, 0, 2)}, {
        1: "动力犁：朝放置时玩家面对的方向工作",
        2: "接入应力网络",
        3: "前方 5×5 范围内的草方块与泥土被翻耕为耕地",
        4: "动力犁须与地面位于同一高度",
    }, floor="dirt", scale=48)


@scene
def mech_piston():
    b = [(0, 0, 0, "piston[facing=east]"), (0, 1, 0, shaft("y")), (1, 0, 0, "oak_planks"), (2, 0, 0, "oak_planks")]
    return S("mech-piston", b, {1: (0, 0, 0), 2: (0, 1, 0), 3: (2, 0, 0)}, {
        1: "动力活塞：有应力时逐格推出，最多 8 格；断开应力后缩回",
        2: "传动轴",
        3: "被推动的方块列",
    }, scale=64)

# ================================================================ 流体

@scene
def pump_tank():
    b = [(0, 0, 0, "water"), (-1, 0, 0, "water"), (1, 0, 0, PUMP), (2, 0, 0, PIPE), (3, 0, 0, PIPE),
         (4, 0, 0, TANK), (5, 0, 0, TANK), (4, 1, 0, TANK), (5, 1, 0, TANK), (1, 1, 0, CUBE)]
    return S("pump-tank", b, {1: (0, 0, 0), 2: (1, 0, 0), 3: (2, 0, 0), 4: (5, 1, 0), 5: (1, 1, 0)}, {
        1: "水源（不会被消耗）",
        2: "抽水泵：与水源相邻放置",
        3: "液体管：六个方向均可连接，相连即构成管网",
        4: "液体储罐：相邻自动成组，每格容量 8000 mB",
        5: "抽水泵需接入电网，耗电 2 RF/t",
    })


@scene
def lava_pump():
    b = [(0, 0, 0, "lava"), (-1, 0, 0, "lava"), (1, 0, 0, LAVA_PUMP), (2, 0, 0, RPIPE), (3, 0, 0, RPIPE),
         (4, 0, 0, "cauldron"), (1, 1, 0, CUBE)]
    return S("lava-pump", b, {1: (0, 0, 0), 2: (1, 0, 0), 3: (2, 0, 0), 4: (4, 0, 0), 5: (1, 1, 0)}, {
        1: "岩浆源：每次抽取消耗一格，会逐渐被抽干",
        2: "岩浆泵",
        3: "加强液体管：整个管网须全部使用加强液体管",
        4: "炼药锅等出口",
        5: "岩浆泵需接入电网，耗电 4 RF/t",
    })


@scene
def valve_splitter():
    b = [(0, 0, 0, PIPE), (1, 0, 0, "iron_door[half=lower,facing=east]"), (1, 1, 0, "iron_door[half=upper,facing=east]"),
         (2, 0, 0, PIPE), (3, 0, 0, "cauldron"), (3, 0, -1, PIPE), (3, 0, 1, PIPE), (4, 0, 0, PIPE)]
    return S("valve-splitter", b, {1: (1, 0, 0), 2: (3, 0, 0)}, {
        1: "流体阀门：串接于管道中，空手右键切换开关",
        2: "分液池：一路输入、多路输出，轮流分配",
    }, scale=64)

# ================================================================ 采矿

@scene
def mining_drill():
    b = [(0, 0, 0, machine("down"))] + cable([(1, 0), (2, 0)]) + [(3, 0, 0, CUBE)]
    return S("mining-drill", b, {1: (0, 0, 0), 2: (3, 0, 0)}, {
        1: "轻型钻井平台：放置于地面，自正下方逐层处理 3×3 范围",
        2: "电网：每处理一格耗电 20 RF",
    }, scale=64)


@scene
def geothermal_rig():
    b = [(2, 0, 2, "crafter[orientation=north_up]"), (2, 0, 3, CUBE)]
    for x in range(5):
        for z in range(5):
            if x in (0, 4) or z in (0, 4):
                b.append((x, 0, z, "iron_bars"))
    return S("geothermal-rig", b, {1: (2, 0, 2), 2: (0, 0, 4), 3: (2, 0, 3)}, {
        1: "重型地脉勘探开采平台：位于 5×5 区域正中心",
        2: "外圈 16 根铁栏杆：与平台同一高度，须完整闭合",
        3: "电网：持续耗电",
    }, scale=52)

# ================================================================ 载具与升降

@scene
def vehicle_car():
    b = [(0, 0, 0, "smooth_stone"), (1, 0, 0, "smooth_stone"), (2, 0, 0, "smooth_stone"), (0, 0, 1, "smooth_stone"),
         (1, 0, 1, "smooth_stone"), (2, 0, 1, "smooth_stone"),
         (2, 1, 0, "dark_oak_stairs[facing=west]"), (0, 1, 0, furnace()), (1, 1, 1, CHEST)]
    return S("vehicle-car", b, {1: (1, 0, 1), 2: (2, 1, 0), 3: (0, 1, 0), 4: (1, 1, 1)}, {
        1: "载具底盘：相邻的底盘连接为车架",
        2: "驾驶座：放置于底盘上",
        3: "发动机：放置于底盘上，每台载具限一个",
        4: "底盘正上方可放置箱子等普通方块作为货物",
    }, floor="grass_block", scale=64)


@scene
def vehicle_boat():
    b = []
    for x in range(-1, 4):
        for z in range(-1, 3):
            b.append((x, -1, z, "water"))
    b += [(0, -1, 0, "smooth_stone"), (1, -1, 0, "smooth_stone"), (2, -1, 0, "smooth_stone"),
          (0, -1, 1, "smooth_stone"), (1, -1, 1, "smooth_stone"), (2, -1, 1, "smooth_stone"),
          (2, 0, 0, "dark_oak_stairs[facing=west]"), (0, 0, 0, furnace())]
    return S("vehicle-boat", b, {1: (1, -1, 1), 2: (2, 0, 0), 3: (0, 0, 0)}, {
        1: "底盘铺设于水面高度",
        2: "驾驶座",
        3: "船只发动机",
    }, floor="sand", scale=64)


@scene
def elevator():
    b = [(0, 0, 0, "quartz_pillar[axis=y]")]
    for y in range(0, 3):
        b += [(-1, y, 0, "quartz_block"), (1, y, 0, "quartz_block"), (0, y, -1, "quartz_block"), (-1, y, -1, "quartz_block"),
              (1, y, -1, "quartz_block")]
    return S("elevator", b, {1: (0, 0, 0)}, {
        1: "气流升降机：右键产生持续 3 秒的上升气流，潜行右键产生下降气流；上方受阻时停止",
    }, scale=64)


@scene
def rope_pulley():
    b = [(0, 4, 0, "white_wool")] + [(0, y, 0, "iron_bars") for y in range(0, 4)]
    for y in range(0, 5):
        b.append((0, y, -1, "stone_bricks"))
    return S("rope-pulley", b, {1: (0, 4, 0), 2: (0, 2, 0)}, {
        1: "升降机滑轮：放置于井口",
        2: "绳索：自滑轮正下方逐格向下铺设，中间不得中断",
    }, scale=64)
