#!/usr/bin/env python3
"""D4 그라데이션 — 팁이 앞으로 튀어나오는 느낌."""

from PIL import Image, ImageDraw, ImageFilter
import math, os

S = 512; CX = CY = S // 2
OUT  = os.path.dirname(os.path.abspath(__file__))
CYAN = (0, 240, 255)
BG   = (3, 3, 10)
TRI  = 170

def canvas():
    return Image.new('RGBA', (S, S), (*BG, 255))

def hex_pts(cx, cy, r, rot=-90):
    return [(cx + r*math.cos(math.radians(60*i+rot)),
             cy + r*math.sin(math.radians(60*i+rot))) for i in range(6)]

def tri_pts(cx, cy, h):
    ofs = h * 0.07
    return [(cx - h*.36+ofs, cy - h*.62),   # 좌상
            (cx - h*.36+ofs, cy + h*.62),   # 좌하
            (cx + h*.62+ofs, cy)]            # 우측 팁

def glow(img, fn, blur=18, passes=2):
    for _ in range(passes):
        lay = Image.new('RGBA', (S,S), (0,0,0,0))
        fn(ImageDraw.Draw(lay))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

def outline(d, pts, color, w=4):
    for i in range(len(pts)):
        d.line([pts[i], pts[(i+1)%len(pts)]], fill=color, width=w)


def make():
    img = canvas()

    # ── 1. 헥사곤 포탈 링 ──────────────────────────────────────────────────
    for r, w, a in zip([210,170,132,96,62], [6,5,5,4,4], [110,140,170,200,240]):
        c = (*CYAN, a)
        def _d(d, _r=r, _w=w, _c=c):
            outline(d, hex_pts(CX,CY,_r), _c, _w)
        glow(img, _d, blur=20, passes=2)
        _d(ImageDraw.Draw(img))

    tp = tri_pts(CX, CY, TRI)

    # ── 2. 그림자 (우하단 오프셋 → 깊이감) ───────────────────────────────
    sh_tp = tri_pts(CX+10, CY+9, TRI)
    sl = Image.new('RGBA', (S,S), (0,0,0,0))
    ImageDraw.Draw(sl).polygon(sh_tp, fill=(0, 20, 30, 180))
    img.alpha_composite(sl.filter(ImageFilter.GaussianBlur(14)))

    # ── 3. 시안 외곽 글로우 (포탈 빛 반사) ────────────────────────────────
    glow(img, lambda d: d.polygon(tp, fill=(*CYAN, 90)), blur=32, passes=2)
    glow(img, lambda d: d.polygon(tp, fill=(*CYAN, 60)), blur=14, passes=1)

    # ── 4. 좌→우 그라데이션 삼각형 ────────────────────────────────────────
    # 왼쪽(left_x): 짙은 청록  →  오른쪽 팁(right_x): 순백
    left_x  = int(min(p[0] for p in tp)) - 2
    right_x = int(max(p[0] for p in tp)) + 2

    grad = Image.new('RGBA', (S,S), (0,0,0,0))
    gd   = ImageDraw.Draw(grad)
    for x in range(left_x, right_x + 1):
        t = (x - left_x) / max(right_x - left_x, 1)
        t = t ** 0.65          # 밝은 구간을 조금 더 넓게
        r = int(  0*(1-t) + 255*t)
        g = int( 95*(1-t) + 255*t)
        b = int(120*(1-t) + 255*t)
        gd.line([(x, 0), (x, S)], fill=(r, g, b, 255))

    # 삼각형 마스크로 클리핑
    mask = Image.new('L', (S,S), 0)
    ImageDraw.Draw(mask).polygon(tp, fill=255)
    img.paste(grad.convert('RGB'), mask=mask)

    # ── 5. 윗면 하이라이트 선 (좌상→팁 경사면) ────────────────────────────
    top_edge = [tp[0], tp[2]]
    hl = Image.new('RGBA', (S,S), (0,0,0,0))
    ImageDraw.Draw(hl).line(top_edge, fill=(255,255,255,180), width=5)
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(3)))
    ImageDraw.Draw(img).line(top_edge, fill=(255,255,255,110), width=2)


    return img.convert('RGB')


def make_sized(size):
    """S 전역 변수를 교체해 임의 크기로 생성."""
    global S, CX, CY, TRI
    orig = (S, CX, CY, TRI)
    S  = size
    CX = CY = size // 2
    TRI = int(170 * size / 512)
    img = make()
    S, CX, CY, TRI = orig
    return img

def make_adaptive(size=1024):
    """배경 투명, 안전 영역(72%) 안에 아이콘."""
    global S, CX, CY, TRI
    orig = (S, CX, CY, TRI)
    S  = size
    CX = CY = size // 2
    scale = 0.72
    TRI = int(170 * size / 512 * scale)

    # 헥사곤·삼각형 모두 safe zone 안으로 축소
    safe = scale
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    CYAN_local = (0, 240, 255)
    BG_local   = (3, 3, 10)

    def hex_pts_l(cx, cy, r, rot=-90):
        return [(cx + r*math.cos(math.radians(60*i+rot)),
                 cy + r*math.sin(math.radians(60*i+rot))) for i in range(6)]

    def tri_pts_l(cx, cy, h):
        ofs = h * 0.07
        return [(cx - h*.36+ofs, cy - h*.62),
                (cx - h*.36+ofs, cy + h*.62),
                (cx + h*.62+ofs, cy)]

    def glow_l(im, fn, blur=18, passes=2):
        for _ in range(passes):
            lay = Image.new('RGBA', (size, size), (0,0,0,0))
            fn(ImageDraw.Draw(lay))
            im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

    def outline_l(d, pts, color, w=4):
        for i in range(len(pts)):
            d.line([pts[i], pts[(i+1)%len(pts)]], fill=color, width=w)

    radii_s  = [int(r * size/512 * scale) for r in [210,170,132,96,62]]
    widths_s = [int(w * size/512 * scale) for w in [6,5,5,4,4]]

    for r, w, a in zip(radii_s, widths_s, [110,140,170,200,240]):
        c = (*CYAN_local, a)
        def _d(d, _r=r, _w=w, _c=c):
            outline_l(d, hex_pts_l(CX, CY, _r), _c, max(1,_w))
        glow_l(img, _d, blur=int(20*size/512), passes=2)
        _d(ImageDraw.Draw(img))

    tri_h = int(170 * size/512 * scale)
    tp = tri_pts_l(CX, CY, tri_h)

    sh_tp = tri_pts_l(CX+int(10*size/512), CY+int(9*size/512), tri_h)
    sl = Image.new('RGBA', (size,size), (0,0,0,0))
    ImageDraw.Draw(sl).polygon(sh_tp, fill=(0,20,30,180))
    img.alpha_composite(sl.filter(ImageFilter.GaussianBlur(int(14*size/512))))

    glow_l(img, lambda d: d.polygon(tp, fill=(*CYAN_local,90)), blur=int(32*size/512), passes=2)
    glow_l(img, lambda d: d.polygon(tp, fill=(*CYAN_local,60)), blur=int(14*size/512), passes=1)

    left_x  = int(min(p[0] for p in tp)) - 2
    right_x = int(max(p[0] for p in tp)) + 2
    grad = Image.new('RGBA', (size,size), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for x in range(left_x, right_x+1):
        t = (x-left_x)/max(right_x-left_x,1)
        t = t**0.65
        r2 = int(0*(1-t)+255*t); g2 = int(95*(1-t)+255*t); b2 = int(120*(1-t)+255*t)
        gd.line([(x,0),(x,size)], fill=(r2,g2,b2,255))
    mask = Image.new('L', (size,size), 0)
    ImageDraw.Draw(mask).polygon(tp, fill=255)
    img.paste(grad.convert('RGBA'), mask=mask)

    top_edge = [tp[0], tp[2]]
    hl = Image.new('RGBA', (size,size), (0,0,0,0))
    ImageDraw.Draw(hl).line(top_edge, fill=(255,255,255,180), width=max(2,int(5*size/512)))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(int(3*size/512))))

    S, CX, CY, TRI = orig
    return img


if __name__ == '__main__':
    ASSETS = os.path.join(OUT, '..', 'assets')

    # store 미리보기 (512)
    make().save(os.path.join(OUT, 'icon_variant_D4_gradient.png'))
    print('✓ store/icon_variant_D4_gradient.png   512×512')

    # Play Store 고해상도 아이콘 (512, RGB)
    make().save(os.path.join(OUT, 'icon_512.png'))
    print('✓ store/icon_512.png                   512×512')

    # 앱 아이콘 1024 (512 생성 후 업스케일)
    base = make()
    base.resize((1024,1024), Image.LANCZOS).save(os.path.join(ASSETS, 'icon.png'))
    print('✓ assets/icon.png                     1024×1024')

    # 어댑티브 아이콘 전경 (RGBA, 투명 배경)
    make_adaptive(1024).save(os.path.join(ASSETS, 'adaptive-icon.png'))
    print('✓ assets/adaptive-icon.png             1024×1024 RGBA')

    # 스플래시 (흰 배경 + 중앙 40% 크기)
    splash = Image.new('RGB', (1024,1024), (255,255,255))
    small  = base.resize((420,420), Image.LANCZOS)
    splash.paste(small, (302, 302))
    splash.save(os.path.join(ASSETS, 'splash-icon.png'))
    print('✓ assets/splash-icon.png               1024×1024')

    print('\n완료!')
