#!/usr/bin/env python3
"""Build the LEONIDA LOTTO meme (1024x1024 PNG) from its parts.

Parts (all under assets/):
  bg-leonida.webp  - AI-made Leonida sunset background (no text in it)
  ghost-mark.png   - make.fun's official ghost mark, from https://make.fun/press/
                     (mark-1024.png: white ghost, sparkle eyes, magenta star
                     coin on a magenta disc)

The script draws the lottery ticket, the number balls, the captions and the
PAID pill with PIL, and composites the ghost mark as the ticket's winner
seal. Output: assets/meme.png — the picture posted to X.

Deterministic: no randomness, no clock, no network. Run from the repo root:
    python3 tools/build_meme.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")

W = H = 1024
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MAGENTA = (200, 0, 122)       # make.fun magenta (ghost disc)
MAGENTA_D = (160, 0, 96)
CREAM = (255, 248, 231)       # lottery ticket paper
INK = (35, 25, 30)
GOLD = (255, 196, 0)
GOLD_D = (214, 158, 0)
TEAL = (0, 150, 160)
RED = (210, 30, 40)
WHITE = (255, 255, 255)
BLACK = (20, 12, 18)


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def text_outline(d, xy, s, f, fill, outline=BLACK, width=4):
    """Centred text with a thick outline (readable over any background)."""
    d.text(xy, s, font=f, fill=fill, anchor="ma",
           stroke_width=width, stroke_fill=outline)


def main():
    # --- background: top-centred square crop of the Leonida sunset ---
    bg = Image.open(os.path.join(ASSETS, "bg-leonida.webp")).convert("RGB")
    bw, bh = bg.size
    side = min(bw, bh)
    left = (bw - side) // 2
    bg = bg.crop((left, 0, left + side, side)).resize((W, H), Image.LANCZOS)
    img = bg.convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")

    # Soften the top and bottom bands so the captions stay readable.
    for y in range(0, 240):
        a = int(80 * (1 - y / 240))
        d.line([(0, y), (W, y)], fill=(20, 0, 20, a))
    for y in range(790, H):
        a = int(100 * ((y - 790) / (H - 790)))
        d.line([(0, y), (W, y)], fill=(10, 0, 20, a))

    # --- lottery ticket (own layer, so the side notches punch through) ---
    tx0, ty0, tx1, ty1 = 64, 246, W - 64, 758
    # drop shadow on the main image first
    d.rounded_rectangle([tx0 + 10, ty0 + 12, tx1 + 10, ty1 + 12], radius=28,
                        fill=(0, 0, 0, 110))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([tx0, ty0, tx1, ty1], radius=28, fill=CREAM + (255,))
    ld.rounded_rectangle([tx0, ty0, tx1, ty1], radius=28,
                         outline=MAGENTA_D + (255,), width=5)
    # header band (magenta, rounded top only)
    ld.rounded_rectangle([tx0, ty0, tx1, ty0 + 92], radius=28,
                         fill=MAGENTA + (255,))
    ld.rectangle([tx0, ty0 + 64, tx1, ty0 + 92], fill=MAGENTA + (255,))
    ld.text((W // 2, ty0 + 14), "★  LEONIDA LOTTO  ★", font=font(46),
            fill=WHITE + (255,), anchor="ma")
    ld.text((W // 2, ty0 + 62), "S C R A T C H   &   W I N", font=font(20),
            fill=(255, 220, 235, 255), anchor="ma")
    # jackpot line
    ld.text((W // 2, ty0 + 112), "GTA VI JACKPOT", font=font(58),
            fill=INK + (255,), anchor="ma")

    # number balls: 13 YEARS / 2 DELAYS / 214 GB / 19 NOV / 6 GTA VI
    balls = [("13", "YEARS", MAGENTA), ("2", "DELAYS", GOLD_D),
             ("214", "GB", TEAL), ("19", "NOV", MAGENTA),
             ("6", "GTA VI", GOLD_D)]
    ball_d = 118
    gap = 26
    total = len(balls) * ball_d + (len(balls) - 1) * gap
    x = (W - total) // 2
    ball_y = ty0 + 196
    for num, label, color in balls:
        cx = x + ball_d // 2
        ld.ellipse([x + 4, ball_y + 6, x + ball_d + 4, ball_y + ball_d + 6],
                   fill=(0, 0, 0, 60))
        ld.ellipse([x, ball_y, x + ball_d, ball_y + ball_d], fill=color + (255,),
                   outline=WHITE + (255,), width=5)
        fnum = font(52) if len(num) <= 2 else font(42)
        ld.text((cx, ball_y + 30), num, font=fnum, fill=WHITE + (255,),
                anchor="ma")
        ld.text((cx, ball_y + ball_d + 8), label, font=font(21),
                fill=INK + (255,), anchor="ma")
        x += ball_d + gap

    # dashed divider
    div_y = ty0 + 196 + ball_d + 52
    for dx in range(tx0 + 40, tx1 - 40, 26):
        ld.line([(dx, div_y), (dx + 14, div_y)], fill=(180, 160, 140, 255),
                width=3)

    # ticket footer — shifted left so the ghost seal (bottom-right) never
    # covers any text: the seal owns the right ~200px of the lower ticket.
    fx = 470
    ld.text((fx, div_y + 14), "DRAWN IN VICE CITY, LEONIDA",
            font=font(26), fill=(90, 70, 80, 255), anchor="ma")
    ld.text((fx, div_y + 48), "CLAIM YOUR PRIZE AT  make.fun",
            font=font(30), fill=MAGENTA_D + (255,), anchor="ma")

    # red PAID pill: the pitch, inside the ticket
    pill_y0, pill_y1 = ty1 - 58, ty1 - 16
    pill_w = 500
    pill_x0, pill_x1 = fx - pill_w // 2, fx + pill_w // 2
    ld.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=21,
                         fill=RED + (255,))
    ld.text((fx, pill_y0 + 7), "★ PAID BY MY AI AGENT ★", font=font(26),
            fill=WHITE + (255,), anchor="ma")

    img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img, "RGBA")

    # --- ghost winner seal (official mark, bottom-right, overlapping edge) ---
    ghost = Image.open(os.path.join(ASSETS, "ghost-mark.png")).convert("RGBA")
    seal = 200
    ghost = ghost.resize((seal, seal), Image.LANCZOS)
    ghost = ghost.rotate(-8, expand=True, resample=Image.BICUBIC)
    gx, gy = tx1 - seal, ty1 - 173
    d.ellipse([gx + 14, gy + seal - 26, gx + seal - 6, gy + seal + 6],
              fill=(0, 0, 0, 90))
    img.paste(ghost, (gx, gy), ghost)
    d = ImageDraw.Draw(img, "RGBA")

    # --- captions ---
    text_outline(d, (W // 2, 42), "WAITED 13 YEARS", font(74), WHITE, width=6)
    text_outline(d, (W // 2, 128), "FOR GTA 6", font(74), WHITE, width=6)
    text_outline(d, (W // 2, 792), "MY NUMBERS FINALLY CAME UP!",
                 font(52), WHITE, width=6)
    text_outline(d, (W // 2, 868),
                 "MY AI AGENT SCRATCHED IT — AND GOT PAID ON MAKE.FUN",
                 font(27), GOLD, width=4)

    out = os.path.join(ASSETS, "meme.png")
    img.convert("RGB").save(out, "PNG")
    print(f"wrote {out} (1024x1024)")


if __name__ == "__main__":
    main()
