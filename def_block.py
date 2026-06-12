#!/usr/bin/env python3
import argparse
from PIL import Image, ImageDraw, ImageFont

LABELS = ["SOAK VALUE", "WOUNDS", "STRAIN", "M/R DEFENSE"]

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
    parser = argparse.ArgumentParser(description="Generate header stat block.")
    parser.add_argument("soak", type=int)
    parser.add_argument("wounds", type=int)
    parser.add_argument("strain", type=int)
    parser.add_argument("mr_def", type=str)
    parser.add_argument("--theme", type=str, default="default",
                        help="Theme: blacksuns, default")
    parser.add_argument("--output", type=str, default="header_block.png")
    return parser.parse_args()

def get_theme(theme_name):
    theme_name = theme_name.lower()

    if theme_name == "blacksun":
        return {
            "label_text": (212, 175, 55),   # gold
            "value_text": (0, 0, 0),
            "label_box": (0, 0, 0),         # black
            "rect_bg": (255, 255, 255),     # white
            "border": (0, 0, 0),
        }

    # DEFAULT THEME (burgundy/red + white text)
    return {
        "label_text": (255, 255, 255),
        "value_text": (0, 0, 0),
        "label_box": (120, 0, 20),
        "rect_bg": (255, 255, 255),
        "border": (0, 0, 0),
    }

def draw_cut_rect(draw, x1, y1, x2, y2, cut, fill, outline=None, width=1):
    pts = [
        (x1 + cut, y1),
        (x2 - cut, y1),
        (x2, y1 + cut),
        (x2, y2 - cut),
        (x2 - cut, y2),
        (x1 + cut, y2),
        (x1, y2 - cut),
        (x1, y1 + cut),
    ]
    draw.polygon(pts, fill=fill)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=width)

def main():
    args = parse_args()
    values = [args.soak, args.wounds, args.strain, args.mr_def]
    theme = get_theme(args.theme)

    width = 730
    margin_x = 10
    margin_y = 10
    gap = 8

    rect_height = 90
    label_box_height = 28
    cut = 10
    border_width = 3

    rect_width = (width - 2 * margin_x - 3 * gap) // 4
    img_height = rect_height + 2 * margin_y

    img = Image.new("RGBA", (width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    label_font = load_font(16)
    value_font = load_font(32)

    x = margin_x

    for label, value in zip(LABELS, values):
        x1 = x
        y1 = margin_y
        x2 = x1 + rect_width
        y2 = y1 + rect_height

        # Main rectangle (white bg, black border)
        draw_cut_rect(
            draw, x1, y1, x2, y2, cut,
            fill=theme["rect_bg"],
            outline=theme["border"],
            width=border_width
        )

        # Label box (cut-cornered)
        lb_y2 = y1 + label_box_height
        draw_cut_rect(
            draw, x1, y1, x2, lb_y2, cut,
            fill=theme["label_box"],
            outline=theme["border"],
            width=border_width
        )

        # Label text
        lw, lh = text_size(draw, label, label_font)
        draw.text(
            (x1 + (rect_width - lw) // 2, y1 + (label_box_height - lh) // 2 - 2),
            label,
            fill=theme["label_text"],
            font=label_font
        )

        # Value text (centered in remaining space)
        value_str = str(value)
        vw, vh = text_size(draw, value_str, value_font)
        value_y = lb_y2 + (rect_height - label_box_height - vh) // 2 - 8
        draw.text(
            (x1 + (rect_width - vw) // 2, value_y),
            value_str,
            fill=theme["value_text"],
            font=value_font
        )

        x += rect_width + gap

    img.save(args.output)
    print(f"Saved {args.output}")

if __name__ == "__main__":
    main()
