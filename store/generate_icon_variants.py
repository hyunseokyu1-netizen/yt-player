#!/usr/bin/env python3
"""아이콘 대안 디자인 3종 생성."""

from PIL import Image, ImageDraw
import os

OUT = os.path.dirname(os.path.abspath(__file__))
S = 512  # 출력 크기

BG   = (18, 18, 22)       # 진한 네이비블랙
RED  = (220, 50,  50)
MINT = (52, 199, 145)     # 민트그린 (B안용)
BLUE = (60, 130, 240)     # 블루 (C안용)
WHITE = (255, 255, 255)
LGRAY = (180, 180, 190)


def play_triangle(draw, cx, cy, half_h, fill=WHITE):
    ofs = half_h * 0.07
    pts = [
        (cx - half_h * 0.36 + ofs, cy - half_h * 0.62),
        (cx - half_h * 0.36 + ofs, cy + half_h * 0.62),
        (cx + half_h * 0.62 + ofs, cy),
    ]
    draw.polygon(pts, fill=fill)


def rounded_rect(draw, xy, r, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0+r, y0, x1-r, y1], fill=fill)
    draw.rectangle([x0, y0+r, x1, y1-r], fill=fill)
    for ex, ey in [(x0,y0),(x1-2*r,y0),(x0,y1-2*r),(x1-2*r,y1-2*r)]:
        draw.ellipse([ex, ey, ex+2*r, ey+2*r], fill=fill)


# ── A안: 원형 플레이 ──────────────────────────────────────────────────────────
# 다크 배경 + 두꺼운 원 테두리 + 빨간 삼각형
def make_a(size=S):
    img = Image.new('RGB', (size, size), BG)
    draw = ImageDraw.Draw(img)

    cx = cy = size // 2
    r_outer = int(size * 0.40)
    r_inner = int(size * 0.32)
    stroke   = r_outer - r_inner

    # 원 테두리 (밝은 색)
    draw.ellipse([cx-r_outer, cy-r_outer, cx+r_outer, cy+r_outer], fill=(240,240,245))
    draw.ellipse([cx-r_inner, cy-r_inner, cx+r_inner, cy+r_inner], fill=BG)

    # 빨간 채워진 원 (안쪽)
    ri = int(size * 0.28)
    draw.ellipse([cx-ri, cy-ri, cx+ri, cy+ri], fill=RED)

    # 흰 삼각형
    play_triangle(draw, cx, cy, ri * 0.58)

    return img


# ── B안: 플레이리스트 라인 + 플레이 ───────────────────────────────────────────
# 왼쪽: 3줄 목록 라인, 오른쪽 하단: 민트 원형 플레이 버튼
def make_b(size=S):
    img = Image.new('RGB', (size, size), BG)
    draw = ImageDraw.Draw(img)

    # 배경 카드 (살짝 밝은 사각형)
    pad = int(size * 0.10)
    r = int(size * 0.12)
    rounded_rect(draw, (pad, pad, size-pad, size-pad), r, (28, 28, 36))

    # 썸네일 블록 (왼쪽 상단 작은 사각형 3개)
    thumb_w = int(size * 0.22)
    thumb_h = int(size * 0.14)
    tx = int(size * 0.16)
    tr = int(size * 0.03)
    gap = int(size * 0.065)
    colors = [(180,60,60), (100,100,120), (80,110,100)]
    for i, c in enumerate(colors):
        ty = int(size * 0.175) + i * (thumb_h + gap)
        rounded_rect(draw, (tx, ty, tx+thumb_w, ty+thumb_h), tr, c)

    # 라인 3개 (제목 텍스트 대신)
    lx = int(size * 0.46)
    lw_list = [int(size * 0.28), int(size * 0.20), int(size * 0.24)]
    lh = int(size * 0.025)
    lr = lh // 2
    for i, lw in enumerate(lw_list):
        ly = int(size * 0.19) + i * (thumb_h + gap) + (thumb_h - lh) // 2
        rounded_rect(draw, (lx, ly, lx+lw, ly+lh), lr, (90,90,105))
        ly2 = ly + int(size * 0.045)
        lw2 = int(lw * 0.65)
        rounded_rect(draw, (lx, ly2, lx+lw2, ly2+lh), lr, (60,60,72))

    # 민트 원형 플레이 버튼 (오른쪽 하단)
    br = int(size * 0.175)
    bx = int(size * 0.695)
    by = int(size * 0.695)
    # 그림자 효과
    draw.ellipse([bx-br+4, by-br+4, bx+br+4, by+br+4], fill=(20,120,80))
    draw.ellipse([bx-br, by-br, bx+br, by+br], fill=MINT)
    play_triangle(draw, bx, by, br * 0.50)

    return img


# ── C안: 겹친 카드 스택 ────────────────────────────────────────────────────────
# 3장의 카드가 살짝 어긋나게 쌓인 모양 + 파란 플레이 오버레이
def make_c(size=S):
    img = Image.new('RGB', (size, size), BG)
    draw = ImageDraw.Draw(img)

    cx = cy = size // 2
    cw = int(size * 0.62)
    ch = int(size * 0.42)
    r  = int(size * 0.08)

    # 카드 3장 (뒤 → 앞 순서)
    card_colors = [(40,40,55), (55,55,75), (30,30,45)]
    offsets = [(+14, +18), (+7, +9), (0, 0)]
    for (ox, oy), col in zip(offsets, card_colors):
        x0 = cx - cw//2 + ox
        y0 = cy - ch//2 + oy
        rounded_rect(draw, (x0, y0, x0+cw, y0+ch), r, col)

    # 앞 카드 위에 얇은 라인 2개 (목록 느낌)
    x0 = cx - cw//2
    y0 = cy - ch//2
    lh = int(size * 0.025)
    lr = lh // 2
    ly1 = y0 + int(ch * 0.30)
    ly2 = y0 + int(ch * 0.58)
    rounded_rect(draw, (x0+int(cw*0.12), ly1, x0+int(cw*0.72), ly1+lh), lr, (85,85,105))
    rounded_rect(draw, (x0+int(cw*0.12), ly2, x0+int(cw*0.55), ly2+lh), lr, (65,65,85))

    # 파란 원형 플레이 버튼 (오른쪽 하단, 카드 위에 걸쳐짐)
    br = int(size * 0.175)
    bx = cx + int(cw * 0.44)
    by = cy + int(ch * 0.52)
    draw.ellipse([bx-br+5, by-br+5, bx+br+5, by+br+5], fill=(20,60,140))
    draw.ellipse([bx-br, by-br, bx+br, by+br], fill=BLUE)
    play_triangle(draw, bx, by, br * 0.50)

    return img


if __name__ == '__main__':
    for name, fn in [('icon_variant_A_circle.png', make_a),
                     ('icon_variant_B_playlist.png', make_b),
                     ('icon_variant_C_stack.png', make_c)]:
        fn().save(os.path.join(OUT, name))
        print(f'✓ store/{name}')
    print('\n완료!')
