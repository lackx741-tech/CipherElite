from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

SIZE = 2048
CENTER = SIZE // 2
OUTPUT_PATH = Path(__file__).resolve().parent / "images" / "v26_logo.png"
LOCAL_FONT = Path(__file__).resolve().parent / "resources" / "fonts" / "assfont.ttf"
FONT_CANDIDATES = [
    Path("/usr/share/fonts/truetype/lato/Lato-Black.ttf"),
    Path("/usr/share/fonts/truetype/lato/Lato-Bold.ttf"),
    LOCAL_FONT,
]


def clamp(value: int) -> int:
    return max(0, min(255, int(value)))


def blend(c1: tuple[int, int, int], c2: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    return tuple(clamp(a * (1 - ratio) + b * ratio) for a, b in zip(c1, c2))


def pick_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def polar_points(radius: float, steps: int, rotation: float = 0.0) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for step in range(steps):
        angle = rotation + math.tau * step / steps
        points.append((CENTER + math.cos(angle) * radius, CENTER + math.sin(angle) * radius))
    return points


def add_background(base: Image.Image) -> None:
    px = base.load()
    core = (44, 8, 68)
    mid = (13, 9, 27)
    edge = (2, 2, 8)
    for y in range(SIZE):
        for x in range(SIZE):
            dx = x - CENTER
            dy = y - CENTER
            distance = math.hypot(dx, dy) / CENTER
            angle = (math.atan2(dy, dx) + math.pi) / math.tau
            swirl = (math.sin(angle * 12 + distance * 18) + 1) / 2
            ratio = min(1.0, distance)
            color = blend(core, mid, min(1.0, ratio * 1.15))
            color = blend(color, edge, min(1.0, max(0.0, (ratio - 0.45) / 0.55)))
            glow = max(0.0, 1.0 - distance * 1.1)
            r = clamp(color[0] + glow * 18 + swirl * 8)
            g = clamp(color[1] + glow * 6)
            b = clamp(color[2] + glow * 20 + swirl * 10)
            px[x, y] = (r, g, b, 255)


def add_stars(layer: Image.Image, rng: random.Random) -> None:
    draw = ImageDraw.Draw(layer)
    for _ in range(220):
        x = rng.randint(0, SIZE - 1)
        y = rng.randint(0, SIZE - 1)
        radius = rng.randint(1, 3)
        alpha = rng.randint(40, 130)
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(220, 235, 255, alpha))


def add_sacred_geometry(layer: Image.Image) -> None:
    draw = ImageDraw.Draw(layer)
    line = (216, 224, 245, 130)
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    for radius, width in ((770, 4), (630, 3), (500, 3), (365, 2), (245, 2)):
        box = (CENTER - radius, CENTER - radius, CENTER + radius, CENTER + radius)
        draw.ellipse(box, outline=line, width=width)
        glow_draw.ellipse(box, outline=(255, 180, 120, 18), width=width + 8)

    orbit = 365
    circle_r = 280
    for i in range(6):
        angle = math.tau * i / 6 - math.pi / 2
        cx = CENTER + math.cos(angle) * orbit
        cy = CENTER + math.sin(angle) * orbit
        box = (cx - circle_r, cy - circle_r, cx + circle_r, cy + circle_r)
        draw.ellipse(box, outline=(194, 210, 235, 110), width=2)
        glow_draw.ellipse(box, outline=(255, 150, 92, 18), width=8)

    for radius, color, width in ((820, (255, 110, 52, 70), 8), (860, (255, 170, 82, 40), 12)):
        draw.regular_polygon((CENTER, CENTER, radius), 6, rotation=30, outline=color, width=width)

    outer_hex = polar_points(720, 6, math.pi / 6)
    inner_hex = polar_points(520, 6, math.pi / 6)
    draw.line(outer_hex + [outer_hex[0]], fill=(220, 226, 242, 120), width=3)
    draw.line(inner_hex + [inner_hex[0]], fill=(220, 226, 242, 120), width=2)
    for a, b in zip(outer_hex, inner_hex):
        draw.line((a, b), fill=(230, 236, 250, 95), width=2)

    for points in (outer_hex, inner_hex):
        for point in points:
            draw.ellipse((point[0] - 10, point[1] - 10, point[0] + 10, point[1] + 10), fill=(255, 180, 120, 170))

    petals: list[tuple[float, float]] = []
    for i in range(18):
        angle = math.tau * i / 18 - math.pi / 2
        radius = 590 if i % 2 == 0 else 430
        petals.append((CENTER + math.cos(angle) * radius, CENTER + math.sin(angle) * radius))
    draw.polygon(petals, outline=(255, 150, 88, 110), width=4)

    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(14)))


def draw_blade(draw: ImageDraw.ImageDraw, blade_x: int, top: int, bottom: int) -> None:
    blade = [
        (blade_x, top),
        (blade_x - 68, top + 215),
        (blade_x - 28, bottom),
        (blade_x + 28, bottom),
        (blade_x + 68, top + 215),
    ]
    draw.polygon(blade, fill=(228, 232, 244, 255), outline=(255, 255, 255, 230))
    draw.line((blade_x, top + 22, blade_x, bottom - 14), fill=(150, 162, 188, 180), width=8)


def add_sword(layer: Image.Image) -> None:
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    draw = ImageDraw.Draw(layer)

    for offset, alpha in ((0, 70), (18, 40), (32, 18)):
        glow_draw.rounded_rectangle((CENTER - 78 - offset, 340 - offset, CENTER + 78 + offset, 1540 + offset), radius=80, outline=(255, 140, 70, alpha), width=18)
    glow_draw.polygon([(CENTER, 238), (CENTER - 132, 520), (CENTER + 132, 520)], fill=(255, 130, 54, 45))
    layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(24)))

    draw_blade(draw, CENTER, 280, 1380)
    draw.polygon([(CENTER, 210), (CENTER - 90, 420), (CENTER + 90, 420)], fill=(244, 246, 252, 255), outline=(255, 255, 255, 230))
    draw.rounded_rectangle((CENTER - 310, 920, CENTER + 310, 1010), radius=30, fill=(118, 66, 48, 255), outline=(255, 175, 92, 220), width=6)
    draw.rectangle((CENTER - 48, 1010, CENTER + 48, 1480), fill=(38, 26, 26, 255), outline=(180, 126, 78, 240), width=6)
    draw.ellipse((CENTER - 88, 1442, CENTER + 88, 1620), fill=(88, 52, 46, 255), outline=(255, 188, 96, 220), width=6)
    draw.ellipse((CENTER - 34, 1488, CENTER + 34, 1556), fill=(255, 170, 94, 255))


def flame_points(angle: float, base_radius: float, inner_radius: float, outer_radius: float, width: float) -> list[tuple[float, float]]:
    left = angle - width / 2
    right = angle + width / 2
    return [
        (CENTER + math.cos(left) * base_radius, CENTER + math.sin(left) * base_radius),
        (CENTER + math.cos(angle - width / 6) * inner_radius, CENTER + math.sin(angle - width / 6) * inner_radius),
        (CENTER + math.cos(angle) * outer_radius, CENTER + math.sin(angle) * outer_radius),
        (CENTER + math.cos(angle + width / 6) * inner_radius, CENTER + math.sin(angle + width / 6) * inner_radius),
        (CENTER + math.cos(right) * base_radius, CENTER + math.sin(right) * base_radius),
    ]


def add_flames(layer: Image.Image, rng: random.Random) -> None:
    flame = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(flame)
    for i in range(28):
        angle = math.tau * i / 28 + rng.uniform(-0.04, 0.04)
        base = 860 + rng.randint(-25, 30)
        inner = base + rng.randint(90, 160)
        outer = base + rng.randint(200, 330)
        width = 0.18 + rng.random() * 0.08
        points = flame_points(angle, base, inner, outer, width)
        draw.polygon(points, fill=(255, 104 + rng.randint(0, 40), 20 + rng.randint(0, 30), 130))
        inner_points = flame_points(angle, base + 8, inner - 18, outer - 56, width * 0.62)
        draw.polygon(inner_points, fill=(255, 206, 100, 160))

    ring_box = (CENTER - 880, CENTER - 880, CENTER + 880, CENTER + 880)
    draw.arc(ring_box, start=0, end=359, fill=(255, 120, 50, 200), width=24)
    draw.arc((CENTER - 915, CENTER - 915, CENTER + 915, CENTER + 915), start=0, end=359, fill=(255, 200, 120, 110), width=12)
    flame = flame.filter(ImageFilter.GaussianBlur(10))
    layer.alpha_composite(flame)


def add_text(layer: Image.Image) -> None:
    text_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)

    title_font = pick_font(340)
    subtitle_font = pick_font(92)

    banner_box = (CENTER - 480, 1510, CENTER + 480, 1840)
    draw.rounded_rectangle(banner_box, radius=72, fill=(8, 8, 18, 200), outline=(255, 122, 46, 190), width=6)
    draw.rounded_rectangle((banner_box[0] + 18, banner_box[1] + 18, banner_box[2] - 18, banner_box[3] - 18), radius=56, outline=(220, 225, 245, 70), width=3)

    text = "V26"
    bbox = draw.textbbox((0, 0), text, font=title_font, stroke_width=8)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = CENTER - text_w / 2
    text_y = 1540

    for blur, alpha in ((30, 110), (16, 150)):
        glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.text((text_x, text_y), text, font=title_font, fill=(255, 120, 40, alpha), stroke_width=12, stroke_fill=(255, 200, 110, alpha))
        layer.alpha_composite(glow.filter(ImageFilter.GaussianBlur(blur)))

    draw.text((text_x, text_y), text, font=title_font, fill=(246, 248, 252, 255), stroke_width=8, stroke_fill=(255, 132, 36, 255))
    subtitle = "SACRED FIRE PROTOCOL"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_x = CENTER - (sub_bbox[2] - sub_bbox[0]) / 2
    draw.text((sub_x, 1725), subtitle, font=subtitle_font, fill=(233, 207, 160, 235), spacing=4)

    layer.alpha_composite(text_layer)


def add_vignette(base: Image.Image) -> None:
    vignette = Image.new("L", (SIZE, SIZE), 0)
    px = vignette.load()
    for y in range(SIZE):
        for x in range(SIZE):
            dx = (x - CENTER) / CENTER
            dy = (y - CENTER) / CENTER
            distance = math.sqrt(dx * dx + dy * dy)
            px[x, y] = clamp(max(0, (distance - 0.35) / 0.65) * 255)
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow.putalpha(vignette)
    base.alpha_composite(shadow)


def build_logo() -> Image.Image:
    rng = random.Random(26)
    base = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 255))
    add_background(base)

    stars = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    add_stars(stars, rng)
    base.alpha_composite(stars)

    geometry = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    add_sacred_geometry(geometry)
    add_flames(geometry, rng)
    add_sword(geometry)
    base.alpha_composite(geometry)

    add_text(base)
    add_vignette(base)

    sharpened = ImageChops.screen(base, base.filter(ImageFilter.GaussianBlur(2)))
    return sharpened.convert("RGB")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    logo = build_logo()
    logo.save(OUTPUT_PATH, format="PNG", optimize=True)
    print(f"Saved logo to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
