#!/usr/bin/env python3
"""
ChainPlay 스토어 스크린샷 생성기 (1080×2340, Samsung Galaxy 기준)
- screenshot_store_ko_1.png : 한국어 메인 화면 (재생 중)
- screenshot_store_ko_2.png : 한국어 URL 추가 모달
- screenshot_store_en_1.png : 영어 메인 화면 (재생 중)
- screenshot_store_en_2.png : 영어 URL 추가 모달
"""

import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT   = os.path.dirname(os.path.abspath(__file__))
W, H  = 1080, 2340
SCALE = 3.0   # 360dp → 1080px

BG          = (15,  15,  26)
PLAYER_BG   = ( 8,   8,  18)
CYAN        = ( 0, 240, 255)
WHITE       = (255, 255, 255)
RED_BTN     = (139,  26,  26)
BORDER1     = ( 30,  30,  46)
BORDER2     = ( 42,  42,  62)
ITEM_BG     = ( 20,  20,  34)
GRAY        = (136, 136, 136)
DARK_GRAY   = ( 60,  60,  80)
MODAL_BG    = ( 26,  26,  26)
INPUT_BG    = ( 42,  42,  42)

def px(dp): return int(dp * SCALE)

def font(size_dp, bold=False, korean=False):
    size = px(size_dp)
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
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

# 썸네일 색상 팔레트 (저작권 없는 직접 제작 그라데이션)
THUMB_PALETTES = [
    [(20,10,60),  (80,30,160)],   # 보라
    [(0,40,60),   (0,160,140)],   # 청록
    [(60,10,10),  (180,60,20)],   # 주황
    [(10,20,60),  (30,80,180)],   # 파랑
    [(20,40,20),  (40,140,80)],   # 초록
    [(40,40,50),  (100,100,130)], # 회청
]

def make_thumb(idx, w, h, label=''):
    """저작권 없는 그라데이션 썸네일 생성."""
    c1, c2 = THUMB_PALETTES[idx % len(THUMB_PALETTES)]
    img = Image.new('RGB', (w, h), c1)
    d = ImageDraw.Draw(img)
    # 좌→우 그라데이션
    for x in range(w):
        t = x / w
        r = int(c1[0]*(1-t) + c2[0]*t)
        g = int(c1[1]*(1-t) + c2[1]*t)
        b = int(c1[2]*(1-t) + c2[2]*t)
        d.line([(x,0),(x,h)], fill=(r,g,b))
    # 하단 어두운 그라데이션
    for y in range(h//3):
        alpha = int(180 * y / (h//3))
        d.line([(0, h-1-y),(w, h-1-y)], fill=(0,0,0,alpha))
    # 중앙 play 아이콘 원
    cx, cy = w//2, h//2 - h//12
    r = min(w,h)//7
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(0,0,0,120))
    # 삼각형
    ts = r//2
    d.polygon([(cx-ts+2, cy-ts), (cx-ts+2, cy+ts), (cx+ts+2, cy)],
              fill=(255,255,255,220))
    # 하단 제목 바
    if label:
        try:
            f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', max(10, h//10))
        except:
            f = ImageFont.load_default()
        d.rectangle([0, h-h//5, w, h], fill=(0,0,0,160))
        d.text((w//20, h - h//5 + h//20), label[:28], fill=(220,220,220), font=f)
    return img

def rounded_rect(draw, xy, r, fill=None, outline=None, width=1):
    x0,y0,x1,y1 = xy
    if fill:
        draw.rectangle([x0+r,y0,x1-r,y1], fill=fill)
        draw.rectangle([x0,y0+r,x1,y1-r], fill=fill)
        for ex,ey in [(x0,y0),(x1-2*r,y0),(x0,y1-2*r),(x1-2*r,y1-2*r)]:
            draw.ellipse([ex,ey,ex+2*r,ey+2*r], fill=fill)
    if outline:
        draw.rounded_rectangle(xy, radius=r, outline=outline, width=width)

def draw_play_triangle(draw, cx, cy, size, color=WHITE):
    h = size
    pts = [(cx - h*0.35, cy - h*0.6),
           (cx - h*0.35, cy + h*0.6),
           (cx + h*0.6,  cy)]
    draw.polygon(pts, fill=color)

def draw_logo_icon(draw, x, y, s=px(36)):
    # 아이콘 배경
    rounded_rect(draw, [x,y,x+s,y+s], px(8), fill=(3,3,10))
    draw.rounded_rectangle([x,y,x+s,y+s], radius=px(8),
                            outline=(*CYAN,), width=px(1.5))
    # 삼각형
    cx, cy = x + s//2 + px(1), y + s//2
    th = px(7)
    draw.polygon([(cx-px(6),cy-th),(cx-px(6),cy+th),(cx+px(6),cy)],
                 fill=(0, 216, 240))

def draw_thumb_item(draw, img_base, item_thumb, x, y, item_w, is_active):
    th_w, th_h = px(120), px(68)
    pad = px(10)
    item_h = th_h + pad * 2

    # 배경
    draw.rectangle([x, y, x+item_w, y+item_h], fill=ITEM_BG)

    # 활성 아이템 왼쪽 cyan 세로선
    if is_active:
        draw.rectangle([x, y, x+px(3), y+item_h], fill=CYAN)

    # 썸네일
    tx = x + px(48) + pad
    ty = y + pad
    if item_thumb:
        resized = item_thumb.resize((th_w, th_h), Image.LANCZOS)
        img_base.paste(resized, (tx, ty))
    draw.rectangle([tx,ty,tx+th_w,ty+th_h], outline=(40,40,60), width=1)

    return item_h

def draw_item_text(draw, title, x, y, item_h, th_w, is_active, is_ko):
    pad = px(10)
    tx = x + px(48) + pad
    ty = y + pad
    title_x = tx + th_w + px(10)
    title_y = ty + px(4)
    color = WHITE if is_active else (180, 180, 180)
    f = font(12.5, korean=is_ko)
    max_w = W - title_x - px(36)
    # 단어 단위 줄바꿈
    words = title.split()
    line1, line2 = '', ''
    for w in words:
        test = (line1 + ' ' + w).strip()
        if draw.textlength(test, font=f) > max_w:
            if not line2:
                line2 = w
            else:
                test2 = line2 + ' ' + w
                if draw.textlength(test2, font=f) <= max_w:
                    line2 = test2
        else:
            line1 = test
    draw.text((title_x, title_y),          line1, fill=color, font=f)
    draw.text((title_x, title_y + px(18)), line2,  fill=color, font=f)

def draw_move_buttons(draw, x, y, item_h, is_first, is_last):
    cx = x + px(24)
    cy = y + item_h // 2
    # ▲
    ac = DARK_GRAY if is_first else GRAY
    draw.polygon([(cx,cy-px(18)),(cx-px(8),cy-px(8)),(cx+px(8),cy-px(8))], fill=ac)
    # ▼
    bc = DARK_GRAY if is_last else GRAY
    draw.polygon([(cx,cy+px(18)),(cx-px(8),cy+px(8)),(cx+px(8),cy+px(8))], fill=bc)

def draw_delete_btn(draw, x, y, item_w, item_h):
    # ✕ 대신 직접 × 선으로 그림 (폰트 호환 문제 방지)
    cx = x + item_w - px(22)
    cy = y + item_h // 2
    s = px(7)
    c = (90, 90, 110)
    draw.line([(cx-s, cy-s), (cx+s, cy+s)], fill=c, width=px(2))
    draw.line([(cx+s, cy-s), (cx-s, cy+s)], fill=c, width=px(2))

# ─────────────────────────────────────────────────────────────────────────────

ITEMS_KO = [
    {"title": "여름날의 노래 — 플레이리스트 Vol.1"},
    {"title": "새벽 감성 모음 — Lo-fi 힐링 음악"},
    {"title": "운동할 때 듣기 좋은 노래 Best 10"},
]
ITEMS_EN = [
    {"title": "Morning Chill Mix — Playlist Vol.1"},
    {"title": "Late Night Vibes — Lo-fi & Calm"},
    {"title": "Workout Energy Boost — Top Hits"},
]

# ─────────────────────────────────────────────────────────────────────────────

def make_screen1(lang):
    is_ko   = (lang == 'ko')
    items   = ITEMS_KO if is_ko else ITEMS_EN
    img     = Image.new('RGB', (W, H), BG)
    draw    = ImageDraw.Draw(img)

    # ── 상태바 (시뮬레이션) ────────────────────────────────────────────
    SB_H = px(36)
    draw.rectangle([0, 0, W, SB_H], fill=(10,10,20))
    f_sb = font(9)
    draw.text((px(16), px(10)), "10:30", fill=(200,200,200), font=f_sb)
    draw.text((W-px(60), px(10)), "100%", fill=(200,200,200), font=f_sb)

    y = SB_H

    # ── 헤더 ──────────────────────────────────────────────────────────
    HDR_PY = px(12); HDR_PX = px(16)
    HDR_H  = px(36) + HDR_PY * 2
    draw_logo_icon(draw, HDR_PX, y + HDR_PY)
    f_title = font(18, bold=True)
    draw.text((HDR_PX + px(36) + px(10), y + HDR_PY + px(8)),
              "ChainPlay", fill=WHITE, font=f_title)
    y += HDR_H
    draw.line([(0,y),(W,y)], fill=BORDER1, width=px(1))

    # ── 플레이어 영역 ──────────────────────────────────────────────────
    PLY_H = int(W * 9 / 16)
    draw.rectangle([0, y, W, y+PLY_H], fill=PLAYER_BG)

    # 플레이어 썸네일 (첫 번째 아이템)
    thumb_lg = make_thumb(0, W, PLY_H)
    # 약간 어둡게 처리 (플레이어 느낌)
    overlay = Image.new('RGBA', (W, PLY_H), (0,0,0,80))
    thumb_lg_rgba = thumb_lg.convert('RGBA')
    thumb_lg_rgba.alpha_composite(overlay)
    img.paste(thumb_lg_rgba.convert('RGB'), (0, y))

    # 재생 중 표시 (사이안 테두리 효과)
    draw = ImageDraw.Draw(img)

    # 이전/다음 버튼 오버레이
    def overlay_btn(cx, cy, direction):
        r = px(22)
        draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(0,0,0,140))
        if direction == 'prev':
            # ◀| 모양
            draw.rectangle([cx-px(9), cy-px(8), cx-px(6), cy+px(8)], fill=WHITE)
            draw.polygon([(cx-px(5),cy),(cx+px(9),cy-px(9)),(cx+px(9),cy+px(9))],
                         fill=WHITE)
        else:
            draw.rectangle([cx+px(6),  cy-px(8), cx+px(9),  cy+px(8)], fill=WHITE)
            draw.polygon([(cx+px(5),cy),(cx-px(9),cy-px(9)),(cx-px(9),cy+px(9))],
                         fill=WHITE)

    btn_y = y + PLY_H - px(32)
    overlay_btn(px(50), btn_y, 'prev')
    overlay_btn(W - px(50), btn_y, 'next')

    # 비디오 제목
    y += PLY_H + px(8)
    f_vtitle = font(14, bold=True, korean=is_ko)
    draw.text((px(16), y), items[0]['title'][:45], fill=WHITE, font=f_vtitle)
    y += px(20) + px(6)

    # ── 재생목록 헤더 ──────────────────────────────────────────────────
    LIST_HDR_H = px(15) + px(7)*2
    hdr_label = "재생 목록" if is_ko else "Playlist"
    hdr_count = f"{len(items)}개" if is_ko else str(len(items))
    f_lhdr = font(15, bold=True, korean=is_ko)
    f_cnt  = font(13, korean=is_ko)
    draw.text((px(16), y+px(7)), hdr_label, fill=WHITE, font=f_lhdr)
    draw.text((W-px(16)-draw.textlength(hdr_count, font=f_cnt),
               y+px(9)), hdr_count, fill=GRAY, font=f_cnt)
    y += LIST_HDR_H
    draw.line([(0,y),(W,y)], fill=BORDER2, width=px(1))

    # ── 플레이리스트 아이템 ────────────────────────────────────────────
    thumbs = [make_thumb(i, px(120), px(68))
              for i in range(len(items))]

    for i, (item, thumb) in enumerate(zip(items, thumbs)):
        is_active = (i == 0)
        item_h = draw_thumb_item(draw, img, thumb, 0, y, W, is_active)
        draw_item_text(draw, item['title'], 0, y, item_h, px(120), is_active, is_ko)
        draw_move_buttons(draw, 0, y, item_h, i==0, i==len(items)-1)
        draw_delete_btn(draw, 0, y, W, item_h)
        draw.line([(0,y+item_h),(W,y+item_h)], fill=BORDER2, width=1)
        y += item_h

    # ── + URL 추가 버튼 ────────────────────────────────────────────────
    btn_label = "+ URL 추가" if is_ko else "+ Add URL"
    f_btn = font(14, bold=True, korean=is_ko)
    btn_w = px(120) if is_ko else px(110)
    btn_h = px(40)
    bx = W - btn_w - px(16)
    by = H - btn_h - px(32)
    rounded_rect(draw, [bx, by, bx+btn_w, by+btn_h], px(20), fill=RED_BTN)
    tw = draw.textlength(btn_label, font=f_btn)
    draw.text((bx + (btn_w-tw)//2, by+px(11)), btn_label, fill=WHITE, font=f_btn)

    # ── 하단 내비게이션 바 ─────────────────────────────────────────────
    NAV_H = px(32)
    draw.rectangle([0, H-NAV_H, W, H], fill=(18,18,28))
    nf = font(20)
    for nx, sym in [(W//4, '|||'), (W//2, '○'), (3*W//4, '‹')]:
        tw2 = draw.textlength(sym, font=nf)
        draw.text((nx - tw2//2, H-NAV_H+px(6)), sym, fill=(100,100,120), font=nf)

    return img


def make_screen2(lang, base_img=None):
    """URL 추가 모달이 열린 화면 — base_img(screen1)를 배경으로 사용"""
    is_ko = (lang == 'ko')

    # screen1을 배경으로 사용 (없으면 새로 생성)
    if base_img is None:
        base_img = make_screen1(lang)

    # 어두운 반투명 오버레이
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 170))
    img = base_img.convert('RGBA')
    img.alpha_composite(overlay)
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)

    # ── 바텀시트 모달 ──────────────────────────────────────────────────
    SHEET_H = px(290)
    sy = H - SHEET_H - px(32)   # 키보드 없는 상태

    # 모달 배경 (둥근 모서리)
    draw.rounded_rectangle([0, sy, W, H], radius=px(24), fill=MODAL_BG)

    # 드래그바
    db_w = px(40); db_h = px(4)
    draw.rounded_rectangle(
        [W//2-db_w//2, sy+px(12), W//2+db_w//2, sy+px(12)+db_h],
        radius=db_h//2, fill=(68,68,68))

    cur_y = sy + px(28)

    # 타이틀 행
    modal_title = "YouTube URL 추가" if is_ko else "Add YouTube URL"
    f_mt = font(18, bold=True, korean=is_ko)
    draw.text((px(20), cur_y), modal_title, fill=WHITE, font=f_mt)
    # ✕ 버튼 — 선으로 직접 그림
    xc = W - px(30)
    yc = cur_y + px(10)
    s  = px(8)
    draw.line([(xc-s, yc-s), (xc+s, yc+s)], fill=GRAY, width=px(2))
    draw.line([(xc+s, yc-s), (xc-s, yc+s)], fill=GRAY, width=px(2))
    cur_y += px(18) + px(14)

    # 입력창
    input_h = px(52)
    draw.rounded_rectangle([px(20), cur_y, W-px(20), cur_y+input_h],
                            radius=px(10), fill=INPUT_BG)
    # 링크 아이콘 (간단히)
    ic = px(12)
    ix, iy = px(32), cur_y + input_h//2
    draw.rounded_rectangle([ix-ic,iy-px(4),ix,iy+px(4)],
                            radius=px(3), outline=(120,120,120), width=2)
    draw.rounded_rectangle([ix,iy-px(4),ix+ic,iy+px(4)],
                            radius=px(3), outline=(120,120,120), width=2)
    # placeholder
    ph = "YouTube URL을 붙여넣기 하세요" if is_ko else "Paste YouTube URL here"
    f_ph = font(14, korean=is_ko)
    draw.text((px(52), cur_y+px(17)), ph, fill=(102,102,102), font=f_ph)
    cur_y += input_h + px(14)

    # 추가 버튼
    add_label = "+ 플레이리스트에 추가" if is_ko else "+ Add to Playlist"
    f_add = font(16, bold=True, korean=is_ko)
    add_h = px(54)
    draw.rounded_rectangle([px(20), cur_y, W-px(20), cur_y+add_h],
                            radius=px(10), fill=RED_BTN)
    tw = draw.textlength(add_label, font=f_add)
    draw.text(((W-tw)//2, cur_y+px(16)), add_label, fill=WHITE, font=f_add)
    cur_y += add_h + px(12)

    # 힌트
    hint = ("youtube.com/watch?v=... 또는 youtu.be/... 형식 지원"
            if is_ko else
            "Supports youtube.com/watch?v=... or youtu.be/...")
    f_hint = font(11, korean=is_ko)
    hw = draw.textlength(hint, font=f_hint)
    draw.text(((W-hw)//2, cur_y), hint, fill=(85,85,85), font=f_hint)

    # 하단 내비게이션
    NAV_H = px(32)
    draw.rectangle([0,H-NAV_H,W,H], fill=(18,18,28))
    nf = font(20)
    for nx, sym in [(W//4,'|||'),(W//2,'○'),(3*W//4,'‹')]:
        tw2 = draw.textlength(sym, font=nf)
        draw.text((nx-tw2//2, H-NAV_H+px(6)), sym, fill=(80,80,100), font=nf)

    return img


if __name__ == '__main__':
    for lang in ['ko', 'en']:
        print(f"\n[{lang.upper()}] 스크린샷 생성 중...")

        print("  Screen 1 (메인 화면)...")
        s1 = make_screen1(lang)
        p1 = os.path.join(OUT, f'screenshot_store_{lang}_1.png')
        s1.save(p1)
        print(f"  ✓ {p1}")

        print("  Screen 2 (URL 모달)...")
        s2 = make_screen2(lang, base_img=s1.copy())
        p2 = os.path.join(OUT, f'screenshot_store_{lang}_2.png')
        s2.save(p2)
        print(f"  ✓ {p2}")

    print("\n완료!")
