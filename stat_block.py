#!/usr/bin/env python3
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont

CHAR_NAMES = ["Brawn", "Agility", "Intellect", "Cunning", "Willpower", "Presence"]

def load_font(size):
    for name in ["Arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a themed stat block image.")
    parser.add_argument("values", nargs=6, type=int,
                        help="Six characteristic values: brawn agility intellect cunning willpower presence")
    parser.add_argument("--theme", type=str, default="default",
                        help="Theme: blacksun, default")
    parser.add_argument("--output", type=str, default="stats.png", help="output filename")
    return parser.parse_args()

def get_theme(theme_name):
    theme_name = theme_name.lower()

    if theme_name == "blacksun":
        return {
            "circle_inner": (255, 255, 255),
            "label_text": (212, 175, 55),
            "lozenge_fill": (0, 0, 0),
        }

    return {
        "circle_inner": (255, 255, 255),
        "label_text": (255, 255, 255),
        "lozenge_fill": (120, 0, 20),
    }

def main():
    args = parse_args()

    values = args.values
    theme = get_theme(args.theme)

    width = 730
    height = 160
    margin = 20
    box_spacing = 4

    box_width = 110

    NUMBER_Y_OFFSET = -10 # move numbers upward (negative = up)
    LABEL_Y_OFFSET = -2 # move text up

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    label_font = load_font(14)
    value_font = load_font(48)

    top = 10
    x = margin

    for name, value in zip(CHAR_NAMES, values):

        # --- Number Circle ---
        circle_radius = 45
        cx = x + box_width // 2
        cy = top + circle_radius + 10

        # Outer black circle
        draw.ellipse(
            (cx - circle_radius, cy - circle_radius,
             cx + circle_radius, cy + circle_radius),
            fill=(0, 0, 0)
        )

        # Inner white circle
        inner_r = circle_radius - 3
        draw.ellipse(
            (cx - inner_r, cy - inner_r,
             cx + inner_r, cy + inner_r),
            fill=theme["circle_inner"]
        )

        # Thin inner ring
        ring_offset = 5
        ring_r = circle_radius - ring_offset
        draw.ellipse(
            (cx - ring_r, cy - ring_r,
             cx + ring_r, cy + ring_r),
            outline=(0, 0, 0),
            width=1
        )

        # Number text
        value_str = str(value)
        vw, vh = text_size(draw, value_str, value_font)
        draw.text(
            (cx - vw // 2, cy - vh // 2 + NUMBER_Y_OFFSET),
            value_str,
            fill=(0, 0, 0),
            font=value_font
        )

        # --- Attribute Label Lozenge ---
        label_text = name.upper()
        lw, lh = text_size(draw, label_text, label_font)

        lozenge_padding_x = 6
        lozenge_padding_y = 4
        loz_w = lw + lozenge_padding_x * 2
        loz_h = lh + lozenge_padding_y * 2

        loz_x1 = cx - loz_w // 2
        loz_y1 = cy + circle_radius + 12
        loz_x2 = loz_x1 + loz_w
        loz_y2 = loz_y1 + loz_h

        draw.rounded_rectangle(
            (loz_x1, loz_y1, loz_x2, loz_y2),
            radius=10,
            fill=theme["lozenge_fill"]
        )

        draw.text(
            (cx - lw // 2, loz_y1 + (loz_h - lh) // 2 + LABEL_Y_OFFSET),
            label_text,
            fill=theme["label_text"],
            font=label_font
        )

        x += box_width + box_spacing

    img.save(args.output)
    print(f"Saved {args.output}")

if __name__ == "__main__":
    main()
