#!/usr/bin/env python3
"""아이콘 D~G — 글로우·네온·기하 구조 실험 디자인."""

from PIL import Image, ImageDraw, ImageFilter
import math, os

S  = 512
CX = CY = S // 2
OUT = os.path.dirname(os.path.abspath(__file__))


# ── 공통 유틸 ────────────────────────────────────────────────────────────────

def canvas(bg=(5, 5, 12)):
    return Image.new('RGBA', (S, S), (*bg, 255))

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
    """draw_fn(ImageDraw) 으로 그린 뒤 blur 적용해 img에 합성."""
    for _ in range(passes):
        lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
        draw_fn(ImageDraw.Draw(lay))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

def draw_poly_outline(draw, pts, color, width=4):
    for i in range(len(pts)):
        draw.line([pts[i], pts[(i+1) % len(pts)]], fill=color, width=width)

def draw_sharp(img, draw_fn):
    draw_fn(ImageDraw.Draw(img))


# ── D: 네온 헥사곤 포탈 ──────────────────────────────────────────────────────
# 동심 육각형 5겹이 빛을 뿜으며 수렴 — 다른 차원으로 이어지는 포탈
def make_d():
    CYAN = (0, 240, 255)
    img  = canvas((3, 3, 10))

    radii  = [210, 170, 132, 96, 62]
    widths = [6, 5, 5, 4, 4]
    alphas = [110, 140, 170, 200, 240]

    for r, w, a in zip(radii, widths, alphas):
        c = (*CYAN, a)
        def _draw(d, _r=r, _w=w, _c=c):
            draw_poly_outline(d, hex_pts(CX, CY, _r), _c, _w)
        glow(img, _draw, blur=20, passes=2)
        draw_sharp(img, lambda d, _r=r, _w=w, _c=c:
                   draw_poly_outline(d, hex_pts(CX, CY, _r), _c, _w))

    # 중앙 플레이 삼각형 (흰색 + 강한 글로우)
    tp = tri_pts(CX, CY, 82)
    glow(img, lambda d: d.polygon(tp, fill=(180, 245, 255, 200)), blur=22, passes=3)
    draw_sharp(img, lambda d: d.polygon(tp, fill=(255, 255, 255, 255)))

    return img.convert('RGB')


# ── E: 오비탈 리액터 ─────────────────────────────────────────────────────────
# 동심 원형 링 4겹 + 황금빛 플레이 — 에너지 코어 느낌
def make_e():
    GOLD   = (255, 210, 60)
    ORANGE = (255, 140, 20)
    img    = canvas((6, 3, 2))

    # 중앙 코어 글로우
    glow(img, lambda d: d.ellipse(
        [CX-50, CY-50, CX+50, CY+50], fill=(255, 180, 0, 160)), blur=40, passes=2)

    radii  = [88, 135, 178, 218]
    widths = [14, 10, 8,  6]
    colors = [(255,220,80,230),(255,170,40,190),(255,120,20,150),(200,80,10,100)]

    for r, w, c in zip(radii, widths, colors):
        # 링 = 큰 원 outline
        def _draw(d, _r=r, _w=w, _c=c):
            d.ellipse([CX-_r, CY-_r, CX+_r, CY+_r], outline=_c, width=_w)
        glow(img, _draw, blur=14, passes=2)
        draw_sharp(img, _draw)

    # 플레이 삼각형 (금색)
    tp = tri_pts(CX, CY, 90)
    glow(img, lambda d: d.polygon(tp, fill=(*GOLD, 200)), blur=20, passes=3)
    draw_sharp(img, lambda d: d.polygon(tp, fill=(*GOLD, 255)))

    return img.convert('RGB')


# ── F: 타이탄 — 거대 삼각형이 곧 아이콘 ─────────────────────────────────────
# 플레이 버튼 자체가 아이콘의 75% 를 차지. 심플하지만 압도적.
def make_f():
    VIOLET = (130, 50, 255)
    BRIGHT = (190, 120, 255)
    img    = canvas((4, 2, 10))

    # 배경 중앙 희미한 글로우
    glow(img, lambda d: d.ellipse(
        [CX-200, CY-200, CX+200, CY+200], fill=(80, 20, 160, 60)), blur=80, passes=1)

    # 거대 삼각형 — 여러 겹 블러로 빛 번짐
    big = tri_pts(CX, CY, 205)
    for blur, a in [(60, 50), (35, 80), (18, 110), (8, 150)]:
        glow(img, lambda d, _a=a: d.polygon(big, fill=(*VIOLET, _a)),
             blur=blur, passes=1)

    # 삼각형 본체
    draw_sharp(img, lambda d: d.polygon(big, fill=(*BRIGHT, 255)))

    # 상단 엣지 하이라이트 (삼각형 위쪽 면을 더 밝게)
    edge_l = [(big[0][0]-1, big[0][1]-1), (big[2][0]+1, big[2][1])]
    glow(img, lambda d: d.line(edge_l, fill=(230, 200, 255, 200), width=3),
         blur=5, passes=2)

    # 내부 작은 흰 삼각형 (핵심 포인트)
    sm = tri_pts(CX, CY, 58)
    glow(img, lambda d: d.polygon(sm, fill=(255, 255, 255, 220)), blur=12, passes=2)
    draw_sharp(img, lambda d: d.polygon(sm, fill=(255, 255, 255, 255)))

    # 좌상단 미니 코너 삼각형 (액센트)
    corner = [(22, 22), (58, 22), (22, 58)]
    glow(img, lambda d: d.polygon(corner, fill=(180, 130, 255, 160)), blur=5, passes=1)
    draw_sharp(img, lambda d: d.polygon(corner, fill=(200, 160, 255, 200)))

    return img.convert('RGB')


# ── G: 프리즘 코어 — 헥사곤 패싯 + 중앙 플레이 ────────────────────────────
# 보석을 위에서 내려다본 구조. 각 면이 다른 색조. 중앙에 민트 플레이.
def make_g():
    MINT  = (0, 255, 180)
    img   = canvas((2, 8, 8))

    R = 220
    outer = hex_pts(CX, CY, R, rot=-90)

    # 파세트 6개 (중심→꼭짓점 삼각형)
    shades = [
        (0, 160, 140), (0, 130, 160), (0, 90, 130),
        (0, 70, 110),  (0, 50,  90), (0, 110, 130),
    ]
    for i, shade in enumerate(shades):
        tri = [(CX, CY), outer[i], outer[(i+1) % 6]]
        draw_sharp(img, lambda d, t=tri, s=shade: d.polygon(t, fill=(*s, 255)))

    # 파세트 경계선 글로우 (팔각 구조감)
    for i in range(6):
        line = [(CX, CY), outer[i]]
        glow(img, lambda d, l=line: d.line(l, fill=(0, 80, 100, 100), width=2),
             blur=3, passes=1)

    # 외곽 육각형 테두리 글로우
    glow(img, lambda d: draw_poly_outline(d, outer, (0, 220, 200, 160), 5),
         blur=10, passes=2)
    draw_sharp(img, lambda d: draw_poly_outline(d, outer, (0, 200, 180, 180), 2))

    # 중앙 어두운 원 (플레이 배경)
    cr = 112
    draw_sharp(img, lambda d: d.ellipse(
        [CX-cr, CY-cr, CX+cr, CY+cr], fill=(2, 8, 8, 240)))

    # 원 테두리 글로우
    glow(img, lambda d: d.ellipse(
        [CX-cr, CY-cr, CX+cr, CY+cr], outline=(*MINT, 220), width=5),
        blur=10, passes=2)
    draw_sharp(img, lambda d: d.ellipse(
        [CX-cr, CY-cr, CX+cr, CY+cr], outline=(*MINT, 200), width=3))

    # 민트 플레이 삼각형
    tp = tri_pts(CX, CY, 78)
    glow(img, lambda d: d.polygon(tp, fill=(*MINT, 210)), blur=14, passes=3)
    draw_sharp(img, lambda d: d.polygon(tp, fill=(200, 255, 235, 255)))

    return img.convert('RGB')


# ── 실행 ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    for name, fn in [
        ('icon_variant_D_portal.png',  make_d),
        ('icon_variant_E_reactor.png', make_e),
        ('icon_variant_F_titan.png',   make_f),
        ('icon_variant_G_prism.png',   make_g),
    ]:
        fn().save(os.path.join(OUT, name))
        print(f'✓ store/{name}')
    print('\n완료!')
