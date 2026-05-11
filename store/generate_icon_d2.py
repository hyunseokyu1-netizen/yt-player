#!/usr/bin/env python3
"""D안 변형 — 플레이 삼각형 크기별 3종 (D2·D3·D4)."""

from PIL import Image, ImageDraw, ImageFilter
import math, os

S  = 512
CX = CY = S // 2
OUT = os.path.dirname(os.path.abspath(__file__))

CYAN = (0, 240, 255)
BG   = (3, 3, 10)

def canvas():
    return Image.new('RGBA', (S, S), (*BG, 255))

def hex_pts(cx, cy, r, rot=-90):
    return [(cx + r * math.cos(math.radians(60*i + rot)),
             cy + r * math.sin(math.radians(60*i + rot)))
            for i in range(6)]

def tri_pts(cx, cy, h):
    ofs = h * 0.07
    return [(cx - h*.36 + ofs, cy - h*.62),
            (cx - h*.36 + ofs, cy + h*.62),
            (cx + h*.62 + ofs, cy)]

def glow(img, draw_fn, blur=18, passes=2):
    for _ in range(passes):
        lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        draw_fn(ImageDraw.Draw(lay))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

def outline(d, pts, color, width=4):
    for i in range(len(pts)):
        d.line([pts[i], pts[(i+1) % len(pts)]], fill=color, width=width)

def make_portal(tri_size):
    img = canvas()

    radii  = [210, 170, 132, 96, 62]
    widths = [6, 5, 5, 4, 4]
    alphas = [110, 140, 170, 200, 240]

    for r, w, a in zip(radii, widths, alphas):
        c = (*CYAN, a)
        def _draw(d, _r=r, _w=w, _c=c):
            outline(d, hex_pts(CX, CY, _r), _c, _w)
        glow(img, _draw, blur=20, passes=2)
        _draw(ImageDraw.Draw(img))

    # 삼각형 글로우
    tp = tri_pts(CX, CY, tri_size)
    glow(img, lambda d: d.polygon(tp, fill=(160, 240, 255, 180)), blur=28, passes=3)
    glow(img, lambda d: d.polygon(tp, fill=(220, 250, 255, 120)), blur=12, passes=2)
    # 삼각형 본체
    ImageDraw.Draw(img).polygon(tp, fill=(255, 255, 255, 255))

    return img.convert('RGB')


if __name__ == '__main__':
    # D2: 조금 더 크게 (원래 82 → 115)
    make_portal(115).save(os.path.join(OUT, 'icon_variant_D2_115.png'))
    print('✓ D2  tri_size=115')

    # D3: 훨씬 크게 — 링 2~3개 관통 (140)
    make_portal(140).save(os.path.join(OUT, 'icon_variant_D3_140.png'))
    print('✓ D3  tri_size=140')

    # D4: 극대화 — 링을 뚫고 나옴 (170)
    make_portal(170).save(os.path.join(OUT, 'icon_variant_D4_170.png'))
    print('✓ D4  tri_size=170')

    print('\n완료!')
