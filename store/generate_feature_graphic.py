#!/usr/bin/env python3
"""ChainPlay 피처 그래픽 1024×500 생성."""

import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT  = os.path.dirname(os.path.abspath(__file__))
CYAN = (0, 240, 255)
BG   = (3, 3, 10)
WHITE = (255, 255, 255)
W, H = 1024, 500


def get_font(size, bold=False, korean=False):
    if korean:
        paths = ['/System/Library/Fonts/AppleSDGothicNeo.ttc',
                 '/Library/Fonts/Arial Unicode.ttf']
    elif bold:
        paths = ['/System/Library/Fonts/Supplemental/Arial Bold.ttf',
                 '/System/Library/Fonts/HelveticaNeue.ttc']
    else:
        paths = ['/System/Library/Fonts/Supplemental/Arial.ttf',
                 '/System/Library/Fonts/HelveticaNeue.ttc']
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def hex_pts(cx, cy, r, rot=-90):
    return [(cx + r*math.cos(math.radians(60*i+rot)),
             cy + r*math.sin(math.radians(60*i+rot))) for i in range(6)]

def tri_pts(cx, cy, h):
    ofs = h * 0.07
    return [(cx - h*.36+ofs, cy - h*.62),
            (cx - h*.36+ofs, cy + h*.62),
            (cx + h*.62+ofs, cy)]

def outline(d, pts, color, w=4):
    for i in range(len(pts)):
        d.line([pts[i], pts[(i+1)%len(pts)]], fill=color, width=w)

def glow(img, size, fn, blur=18, passes=2):
    for _ in range(passes):
        lay = Image.new('RGBA', size, (0,0,0,0))
        fn(ImageDraw.Draw(lay))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def draw_d4_icon(icon_size):
    """D4 그라데이션 아이콘을 icon_size 크기로 생성해 RGBA 반환."""
    S = icon_size
    CX = CY = S // 2
    scale = S / 512

    img = Image.new('RGBA', (S, S), (*BG, 255))

    # 헥사곤 포탈 링
    for r, w, a in zip([210,170,132,96,62], [6,5,5,4,4], [110,140,170,200,240]):
        rs, ws = int(r*scale), max(1, int(w*scale))
        c = (*CYAN, a)
        def _d(d, _r=rs, _w=ws, _c=c):
            outline(d, hex_pts(CX, CY, _r), _c, _w)
        glow(img, (S,S), _d, blur=int(20*scale), passes=2)
        _d(ImageDraw.Draw(img))

    TRI = int(170 * scale)
    tp = tri_pts(CX, CY, TRI)

    # 그림자
    sh_tp = tri_pts(CX+int(10*scale), CY+int(9*scale), TRI)
    sl = Image.new('RGBA', (S,S), (0,0,0,0))
    ImageDraw.Draw(sl).polygon(sh_tp, fill=(0,20,30,180))
    img.alpha_composite(sl.filter(ImageFilter.GaussianBlur(int(14*scale))))

    # 시안 외곽 글로우
    glow(img, (S,S), lambda d: d.polygon(tp, fill=(*CYAN, 90)), blur=int(32*scale), passes=2)
    glow(img, (S,S), lambda d: d.polygon(tp, fill=(*CYAN, 60)), blur=int(14*scale), passes=1)

    # 좌→우 그라데이션 삼각형
    left_x  = int(min(p[0] for p in tp)) - 2
    right_x = int(max(p[0] for p in tp)) + 2
    grad = Image.new('RGBA', (S,S), (0,0,0,0))
    gd = ImageDraw.Draw(grad)
    for x in range(left_x, right_x+1):
        t = (x-left_x) / max(right_x-left_x, 1)
        t = t**0.65
        r2 = int(0*(1-t)+255*t); g2 = int(95*(1-t)+255*t); b2 = int(120*(1-t)+255*t)
        gd.line([(x,0),(x,S)], fill=(r2,g2,b2,255))
    mask = Image.new('L', (S,S), 0)
    ImageDraw.Draw(mask).polygon(tp, fill=255)
    img.paste(grad.convert('RGBA'), mask=mask)

    # 윗면 하이라이트
    top_edge = [tp[0], tp[2]]
    hl = Image.new('RGBA', (S,S), (0,0,0,0))
    ImageDraw.Draw(hl).line(top_edge, fill=(255,255,255,180), width=max(2,int(5*scale)))
    img.alpha_composite(hl.filter(ImageFilter.GaussianBlur(int(3*scale))))
    ImageDraw.Draw(img).line(top_edge, fill=(255,255,255,110), width=max(1,int(2*scale)))

    return img


def make_feature_graphic(lang='ko'):
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 배경 그라데이션
    for x in range(W):
        t = x / W
        v = int(3 + 20 * t)
        draw.line([(x, 0), (x, H)], fill=(v, v, v+4))

    # 오른쪽 사이안 안개
    fog = Image.new('RGBA', (W, H), (0,0,0,0))
    ImageDraw.Draw(fog).ellipse([620, 80, 1010, 420], fill=(*CYAN, 18))
    img_rgba = img.convert('RGBA')
    img_rgba.alpha_composite(fog.filter(ImageFilter.GaussianBlur(60)))
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)

    # ── 텍스트 (언어별) ──────────────────────────────────────────────────
    is_ko = (lang == 'ko')

    font_title   = get_font(80, bold=True)
    font_sub     = get_font(26, korean=is_ko)
    font_bullet  = get_font(22, korean=is_ko)
    font_tagline = get_font(20, korean=is_ko)

    sub_text     = "알고리즘 말고, 내가 만든 순서대로" if is_ko else "Your order. Not the algorithm's."
    bullets      = (
        ["원하는 영상만 골라 나만의 플레이리스트",
         "한 영상 끝나면 다음으로 자동 재생",
         "URL 붙여넣기만으로 즉시 추가"]
        if is_ko else
        ["Pick any videos — build your own playlist",
         "Auto-plays the next video when one ends",
         "Just paste a URL to add instantly"]
    )
    tagline_text = ("알고리즘 없이, 내 플레이리스트를 내 순서대로"
                    if is_ko else
                    "No algorithm. Just your playlist, your way.")

    # 앱 이름
    draw.text((70, 72), "ChainPlay", fill=WHITE, font=font_title)

    # 사이안 언더라인
    draw.rectangle([70, 162, 290, 165], fill=(*CYAN, 220))

    # 서브타이틀
    draw.text((70, 180), sub_text, fill=(0, 200, 215), font=font_sub)

    # 불릿
    y = 242
    for b in bullets:
        draw.polygon([(70, y+8), (70, y+20), (80, y+14)], fill=(*CYAN, 200))
        draw.text((90, y), b, fill=(160, 160, 160), font=font_bullet)
        y += 38

    # 태그라인
    draw.text((70, H-58), tagline_text, fill=(80, 80, 100), font=font_tagline)

    # ── D4 아이콘 (오른쪽) ───────────────────────────────────────────────
    icon_size = 320
    icon = draw_d4_icon(icon_size)

    img_rgba2 = img.convert('RGBA')
    icon_pos_x = W - icon_size - 60
    icon_pos_y = (H - icon_size) // 2

    icon_bg = Image.new('RGBA', (W, H), (0,0,0,0))
    icon_bg.paste(icon, (icon_pos_x, icon_pos_y))
    img_rgba2.alpha_composite(icon_bg)

    return img_rgba2.convert('RGB')


if __name__ == '__main__':
    ko_path = os.path.join(OUT, 'feature_graphic.png')
    en_path = os.path.join(OUT, 'feature_graphic_en.png')

    make_feature_graphic('ko').save(ko_path)
    print(f'✓ {ko_path}  ({W}×{H})')

    make_feature_graphic('en').save(en_path)
    print(f'✓ {en_path}  ({W}×{H})')
