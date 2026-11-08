// 正文里的图片按比例缩放、表格按内容分配列宽，算出来的尺寸常常带小数，
// 后面的文字就会落在半像素上发虚。这里把它们取成整数像素（样式部分见 custom.css 的「像素对齐」）。

function snapImages(root: HTMLElement) {
  root.querySelectorAll<HTMLImageElement>('img').forEach((img) => {
    const fit = () => {
      if (!img.naturalWidth) return
      img.style.height = ''
      const r = img.getBoundingClientRect()
      const h = Math.floor(r.height)
      if (h !== r.height) img.style.height = `${h}px`
    }
    if (img.complete) fit()
    else img.addEventListener('load', fit, { once: true })
  })
}

function snapTables(root: HTMLElement) {
  root.querySelectorAll<HTMLTableElement>('table').forEach((table) => {
    const row = table.rows[0]
    if (!row) return
    const cells = Array.from(row.cells)
    cells.forEach((c) => (c.style.width = ''))
    const widths = cells.map((c) => c.getBoundingClientRect().width)
    if (widths.every((w) => w === Math.floor(w))) return
    // 每列都给定整数宽度后，表格总宽就是各列之和，列和行的位置都是整数
    cells.forEach((c, i) => (c.style.width = `${Math.floor(widths[i])}px`))
  })
}

export function snap() {
  const root = document.querySelector<HTMLElement>('.vp-doc')
  if (!root) return
  snapTables(root)
  snapImages(root)
}

let frame = 0
export function snapOnResize() {
  window.addEventListener('resize', () => {
    cancelAnimationFrame(frame)
    frame = requestAnimationFrame(snap)
  })
}
