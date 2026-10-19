#!/usr/bin/env python3
"""Generate OGP + SNS price chart images from src/data/clinics.json (掲載値のみ、推定なし).
Requires Pillow and Noto Sans CJK JP (fonts-noto-cjk). Output: public/og/*.png"""
import json, os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'public', 'og'); os.makedirs(OUT, exist_ok=True)
FB = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
f = lambda s, b=True: ImageFont.truetype(FB if b else FR, s, index=0)  # index 0 = JP
NAVY, TEAL, PALE, INK, GREY = '#1f4a5c', '#2b5f75', '#eef3f5', '#222222', '#666666'
d = json.load(open(os.path.join(ROOT, 'src', 'data', 'clinics.json'), encoding='utf-8'))

def both(p):  # same rule as src/data/util.js bothSides()
    return p['price'] if p['unit'] == '両脇' else p['price'] * 2 if p['unit'] == '片側' else None
def stats(t):
    v = sorted(x for c in d['clinics'] for p in c['prices'] if p['t'] == t and (x := both(p)) is not None)
    n = len(v); med = v[(n - 1) // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    return dict(min=v[0], med=round(med), max=v[-1], n=n)
yen = lambda n: f'{n:,}円'
checked = sorted({c.get('checked_at', d['checked_at']) for c in d['clinics']})
period = f'{checked[0]}〜{checked[-1]}'
ncl = len(d['clinics'])

def ctext(dr, xy, s, font, fill, anchor='mm'): dr.text(xy, s, font=font, fill=fill, anchor=anchor)

# 1) default OGP 1200x630
im = Image.new('RGB', (1200, 630), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 1200, 630], fill=PALE)
dr.rounded_rectangle([40, 40, 1160, 590], 28, fill='white', outline='#cfdde3', width=3)
dr.rounded_rectangle([40, 40, 1160, 590], 28, fill='white', outline=TEAL, width=6)
dr.rectangle([140, 120, 1060, 128], fill=TEAL)
ctext(dr, (600, 230), 'ワキガ費用ナビ', f(108), NAVY)
ctext(dr, (600, 345), 'ワキガ治療の費用を公式掲載値で比較', f(52), INK)
ctext(dr, (600, 425), '剪除法（保険・自費）／ミラドライ／ボトックス', f(34, False), GREY)
dr.rounded_rectangle([300, 475, 900, 535], 30, fill=TEAL)
ctext(dr, (600, 505), f'{ncl}院の料金を出典URL・確認日つきで掲載', f(28), 'white')
im.save(os.path.join(OUT, 'default.png'), optimize=True)

# 2) price chart (16:9, 1200x675) – range bar + median, linear scale
items = [('senjo_ins', '剪除法（保険・3割負担）'), ('botox', 'ワキのボトックス注射'), ('miradry', 'ミラドライ'), ('senjo', '自費の手術（剪除法など）')]
S = {k: stats(k) for k, _ in items}
W, H = 1200, 675
im = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, W, 96], fill=TEAL)
dr.text((40, 48), 'ワキガ・多汗症治療の掲載料金（両脇換算）', font=f(40), fill='white', anchor='lm')
dr.text((W - 40, 48), 'ワキガ費用ナビ', font=f(28), fill='white', anchor='rm')
dr.text((40, 125), f'各クリニック公式サイトの掲載値から集計：中央値（●）と範囲（最小〜最大）', font=f(24, False), fill=GREY, anchor='lm')
X0, X1 = 400, 1150; vmax = 600000
sx = lambda v: X0 + (X1 - X0) * v / vmax
for t in range(0, vmax + 1, 100000):
    x = sx(t); dr.line([x, 160, x, 560], fill='#e3e8ea', width=2)
    dr.text((x, 572), f'{t // 10000}万円' if t else '0', font=f(20, False), fill=GREY, anchor='mt')
for i, (k, name) in enumerate(items):
    s = S[k]; y = 205 + i * 100
    dr.text((40, y - 14), name, font=f(28), fill=INK, anchor='lm')
    dr.text((40, y + 22), f'{s["n"]}件', font=f(20, False), fill=GREY, anchor='lm')
    dr.rounded_rectangle([sx(s['min']), y - 12, max(sx(s['max']), sx(s['min']) + 8), y + 12], 12, fill='#9cc3d1')
    cx = sx(s['med']); dr.ellipse([cx - 13, y - 13, cx + 13, y + 13], fill=NAVY, outline='white', width=3)
    lab = f'中央値 {yen(s["med"])}（{yen(s["min"])}〜{yen(s["max"])}）'
    tx = max(sx(s['max']) + 16, X0 + 10) if sx(s['max']) < 760 else sx(s['min'])
    anchor = 'lm'
    if sx(s['max']) >= 760: dr.text((sx(s['min']), y + 34), lab, font=f(22), fill=NAVY, anchor='lm')
    else: dr.text((tx, y), lab, font=f(22), fill=NAVY, anchor='lm')
dr.text((40, 615), f'確認日 {period}／{ncl}院の掲載データ。片側表記は×2、単位不明は除外。保険診療は目安で、初診料・検査料等が別途かかる場合あり。', font=f(16, False), fill=GREY, anchor='lm')
dr.text((40, 645), '治療法の優劣・効果を示すものではありません。治療の適否は医師にご相談ください。最新の料金は各公式サイトでご確認ください。', font=f(16, False), fill=GREY, anchor='lm')
im.save(os.path.join(OUT, 'price-chart.png'), optimize=True)

# 3) square card 1080x1080 – medians for 3 main treatments
im = Image.new('RGB', (1080, 1080), PALE); dr = ImageDraw.Draw(im)
dr.rectangle([0, 0, 1080, 150], fill=TEAL)
ctext(dr, (540, 60), 'ワキガ治療、いくらかかる？', f(56), 'white')
ctext(dr, (540, 120), f'公式サイト掲載値の中央値（両脇換算・{ncl}院の掲載データより）', f(28, False), 'white')
for i, (k, name) in enumerate([('senjo_ins', '剪除法（保険・3割負担）'), ('miradry', 'ミラドライ'), ('botox', 'ワキのボトックス注射（1回）')]):
    s = S[k]; y0 = 190 + i * 255
    dr.rounded_rectangle([60, y0, 1020, y0 + 225], 24, fill='white', outline='#cfdde3', width=3)
    ctext(dr, (540, y0 + 45), name, f(36), INK)
    ctext(dr, (540, y0 + 118), f'中央値 {yen(s["med"])}', f(64), NAVY)
    ctext(dr, (540, y0 + 185), f'範囲 {yen(s["min"])}〜{yen(s["max"])}（{s["n"]}件）', f(28, False), GREY)
ctext(dr, (540, 975), f'確認日 {period}。保険診療は目安で、初診料・検査料等が別途かかる場合あり。', f(22, False), GREY)
ctext(dr, (540, 1010), '効果・優劣を示すものではありません。治療の適否は医師にご相談ください。', f(22, False), GREY)
ctext(dr, (540, 1050), 'ワキガ費用ナビ  umeboshi-bit.github.io/wakiga-cost', f(24), TEAL)
im.save(os.path.join(OUT, 'price-medians-square.png'), optimize=True)
print(json.dumps(S, ensure_ascii=False), period)
