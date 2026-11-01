"""
渲染全部场景：

    MC_ASSETS=<解包目录>/assets/minecraft python3 -m ztech_render.build <输出目录> [场景名...]

同时在本目录写出 legends.json（编号 → 说明），供编写维基图例时对照。
"""
import json
import os
import sys
import time

from .compose import build
from .scenes import SCENES


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "out"
    only = set(sys.argv[2:])
    legends = {}
    for fn in SCENES:
        sc = fn()
        if only and sc.name not in only:
            continue
        t = time.time()
        path, size = build(sc, out)
        legends[sc.name] = {str(k): v for k, v in sorted(sc.legend.items())}
        print(f"{sc.name:28s} {size[0]}x{size[1]}  {time.time() - t:.1f}s")
    if not only:
        with open(os.path.join(os.path.dirname(__file__), "legends.json"), "w", encoding="utf-8") as f:
            json.dump(legends, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
