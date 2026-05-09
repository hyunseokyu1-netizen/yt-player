#!/usr/bin/env python3
"""YT Player 스토어 에셋 일괄 생성 스크립트."""

from PIL import Image, ImageDraw, ImageFont
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets')

DARK_BG = (20, 20, 20)
RED = (220, 30, 30)
WHITE = (255, 255, 255)


def get_font(size, korean=False):
    paths = (
        ['/System/Library/Fonts/AppleSDGothicNeo.ttc',
         '/Library/Fonts/Arial Unicode.ttf']
        if korean else
        ['/System/Library/Fonts/Supplemental/Arial Bold.ttf',
         '/System/Library/Fonts/HelveticaNeue.ttc',
         '/System/Library/Fonts/Supplemental/Arial.ttf']
    )
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def rounded_rect(draw, xy, r, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
    draw.ellipse([x0, y0, x0 + 2*r, y0 + 2*r], fill=fill)
    draw.ellipse([x1 - 2*r, y0, x1, y0 + 2*r], fill=fill)
    draw.ellipse([x0, y1 - 2*r, x0 + 2*r, y1], fill=fill)
    draw.ellipse([x1 - 2*r, y1 - 2*r, x1, y1], fill=fill)


def play_triangle(draw, cx, cy, half_h, fill=WHITE):
    ofs = half_h * 0.07
    pts = [
        (cx - half_h * 0.36 + ofs, cy - half_h * 0.62),
        (cx - half_h * 0.36 + ofs, cy + half_h * 0.62),
        (cx + half_h * 0.62 + ofs, cy),
    ]
    draw.polygon(pts, fill=fill)


def draw_yt_badge(draw, x, y, size):
    """유튜브 스타일 배지 (빨간 둥근 사각형 + 흰 삼각형)."""
    hm = int(size * 0.13)
    vm = int(size * 0.27)
    r = int(size * 0.115)
    rounded_rect(draw, (x + hm, y + vm, x + size - hm, y + size - vm), r, RED)
    cx, cy = x + size // 2, y + size // 2
    play_triangle(draw, cx, cy, (size - 2 * vm) * 0.43)


# ── 아이콘 (앱용 1024, 스토어용 512) ────────────────────────────────────────

def make_icon_rgb(size, bg=DARK_BG):
    img = Image.new('RGB', (size, size), bg)
    draw = ImageDraw.Draw(img)
    draw_yt_badge(draw, 0, 0, size)
    return img


def make_adaptive_fg(size=1024):
    """배경 투명, 안전 영역(72%) 안에 배지."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    scale = 0.72
    s = int(size * scale)
    offset = (size - s) // 2
    draw_yt_badge(draw, offset, offset, s)
    return img


def make_splash(size=1024):
    """흰 배경, 중앙에 작은 배지."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    badge_size = int(size * 0.4)
    offset = (size - badge_size) // 2
    draw_yt_badge(draw, offset, offset, badge_size)
    return img


# ── 피처 그래픽 1024×500 ────────────────────────────────────────────────────

def make_feature_graphic():
    W, H = 1024, 500
    img = Image.new('RGB', (W, H), DARK_BG)
    draw = ImageDraw.Draw(img)

    # 오른쪽 절반 살짝 밝게
    for x in range(W):
        t = x / W
        v = int(20 + 14 * t)
        draw.line([(x, 0), (x, H)], fill=(v, v, v))

    # 왼쪽 — 텍스트
    title = get_font(72, korean=True)
    sub = get_font(30, korean=True)
    small = get_font(22, korean=True)

    draw.text((72, 100), "YT Player", fill=WHITE, font=title)
    draw.text((76, 192), "YouTube 플레이리스트 플레이어", fill=(170, 170, 170), font=sub)

    bullets = [
        "유튜브 영상 순차 자동 재생",
        "플레이리스트 저장 및 관리",
        "Premium 없이도 동작",
    ]
    y = 258
    for b in bullets:
        # 빨간 점 대신 빨간 작은 삼각형
        draw.polygon([(76, y+7), (76, y+17), (84, y+12)], fill=RED)
        draw.text((92, y), b, fill=(140, 140, 140), font=small)
        y += 38

    # 오른쪽 — 아이콘
    badge = 260
    bx = W - badge - 90
    by = (H - badge) // 2
    draw_yt_badge(draw, bx, by, badge)

    return img


# ── 메인 ────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(BASE_DIR, exist_ok=True)

    # 스토어 고해상도 아이콘 512×512 (알파 없음)
    make_icon_rgb(512).save(os.path.join(BASE_DIR, 'icon_512.png'))
    print("✓ store/icon_512.png       512×512  (Play Store 고해상도 아이콘)")

    # 피처 그래픽 1024×500
    make_feature_graphic().save(os.path.join(BASE_DIR, 'feature_graphic.png'))
    print("✓ store/feature_graphic.png  1024×500  (Play Store 피처 그래픽)")

    # assets/ 업데이트
    make_icon_rgb(1024).save(os.path.join(ASSETS_DIR, 'icon.png'))
    print("✓ assets/icon.png          1024×1024 (앱 아이콘)")

    make_adaptive_fg().save(os.path.join(ASSETS_DIR, 'adaptive-icon.png'))
    print("✓ assets/adaptive-icon.png 1024×1024 RGBA (어댑티브 아이콘 전경)")

    make_splash().save(os.path.join(ASSETS_DIR, 'splash-icon.png'))
    print("✓ assets/splash-icon.png   1024×1024 (스플래시)")

    print("\n완료!")


if __name__ == '__main__':
    main()
