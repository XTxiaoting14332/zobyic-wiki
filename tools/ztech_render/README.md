# Z-Tech 示意图渲染器

读取原版客户端的方块状态、模型与贴图，在内存中拼装场景并输出等轴测 PNG，用于 `docs/ztech/` 的示意图。

## 用法

```bash
./fetch_assets.sh                    # 首次：下载 1.21.8 客户端并解出资源到 ./mc
cd ..                                # 回到 tools/
MC_ASSETS=ztech_render/mc/assets/minecraft \
  python3 -m ztech_render.build ../docs/public/images/ztech [场景名...]
```

依赖 Python 3、numpy、Pillow；标注字体使用 DejaVu Sans Bold。

## 文件

- `render.py`：方块状态 → 模型解析、z-buffer 光栅化
- `compose.py`：铺底板、编号标注、流向箭头
- `scenes.py`：全部场景。方块一律用插件放置后的真实材质（传送带支架=铁块、粉碎机=发射器……），摆法按插件代码的实际判定；每个场景的 `legend` 与维基正文图例逐字一致，修改时两边同步
- `build.py`：批量渲染，同时输出 `legends.json`

箱子是实体渲染、没有方块模型，场景里的容器统一用木桶表示。
