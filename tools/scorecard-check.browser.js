/* Browser check for scorecard rows (svgkit 1.2.0). Open a skill's sample page
 * (served with python3 -m http.server), set the window to 1280 wide, paste
 * this file into the console, then do the same at 390 wide. For every
 * scorecard frame on the page (.scg, or the site's [data-scorecard]) it
 * checks:
 *   - every text node renders 12px or 14px: computed font-size x currentCSSZoom;
 *   - no text inside an SVG;
 *   - no bordered or outlined box larger than 40 x 20;
 *   - no text box intersects a picture;
 *   - content reaches at least 95% of the frame's width.
 * It prints one row per frame and fails loudly (console.error) on any miss.
 * It returns the rows, so an agent can read them with a javascript tool. */
;(() => {
  const frames = [...document.querySelectorAll('.scg, [data-scorecard]')].filter((f) => f.getClientRects().length)
  const rows = frames.map((f) => {
    const sizes = {}
    const off = []
    const texts = []
    const walk = document.createTreeWalker(f, NodeFilter.SHOW_TEXT)
    while (walk.nextNode()) {
      const n = walk.currentNode
      const el = n.parentElement
      if (!n.textContent.trim() || !el.getClientRects().length) continue
      if (el.closest('svg')) off.push(`text in svg: ${n.textContent.trim()}`)
      const px = Math.round(parseFloat(getComputedStyle(el).fontSize) * (el.currentCSSZoom || 1) * 10) / 10
      sizes[px] = (sizes[px] || 0) + 1
      if (px !== 12 && px !== 14) off.push(`${px}px: ${n.textContent.trim().slice(0, 24)}`)
      const r = document.createRange()
      r.selectNodeContents(n)
      texts.push(...r.getClientRects())
    }
    const frame = f.getBoundingClientRect()
    let right = frame.left
    let boxes = 0
    for (const e of f.querySelectorAll('*')) {
      const b = e.getBoundingClientRect()
      if (!b.width || !b.height) continue
      right = Math.max(right, b.right)
      const cs = getComputedStyle(e)
      const bordered = ['Top', 'Right', 'Bottom', 'Left'].every((s) => parseFloat(cs[`border${s}Width`]) > 0 && cs[`border${s}Style`] !== 'none')
      const outlined = cs.outlineStyle !== 'none' && parseFloat(cs.outlineWidth) > 0
      if ((bordered || outlined) && b.width > 40 && b.height > 20) boxes++
    }
    const marks = [...f.querySelectorAll('.sc-p > *')].map((m) => m.getBoundingClientRect()).filter((m) => m.width > 20)
    let overlaps = 0
    for (const t of texts) for (const m of marks) if (t.left < m.right - 0.5 && t.right > m.left + 0.5 && t.top < m.bottom - 0.5 && t.bottom > m.top + 0.5) overlaps++
    const reach = Math.round(((right - frame.left) / frame.width) * 1000) / 10
    return { width: innerWidth, label: (f.getAttribute('aria-label') || '').slice(0, 40), sizes: JSON.stringify(sizes), off: off.length, boxes, overlaps, reach, detail: off.slice(0, 3).join(' | ') }
  })
  console.table(rows)
  const bad = rows.filter((r) => r.off || r.boxes || r.overlaps || r.reach < 95)
  if (!rows.length || bad.length) console.error('scorecard-check: FAIL', rows.length ? bad : 'no scorecard frame on the page')
  else console.log(`scorecard-check: ok, ${rows.length} frame(s) at ${innerWidth}px, every text 12 or 14px`)
  return rows
})()
