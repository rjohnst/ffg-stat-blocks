#!/usr/bin/env python3
import argparse
from PIL import Image, ImageDraw, ImageFont

WIDTH = 730
MARGIN = 20
ROW_HEIGHT = 34
COLUMN_GAP = 40
SHAPE_SIZE = 16
OUTLINE = (0, 0, 0)

def load_font(size):
    for name in ["Arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except:
            continue
    return ImageFont.load_default()

def draw_square(draw, cx, cy, size, fill):
    r = size // 2
    pts = [
        (cx - r, cy - r),
        (cx + r, cy - r),
        (cx + r, cy + r),
        (cx - r, cy + r)
    ]
    draw.polygon(pts, fill=fill, outline=OUTLINE)

def draw_hexagon(draw, cx, cy, size, fill):
    r = size // 2
    pts = [
        (cx - r, cy),
        (cx - r//2, cy - r),
        (cx + r//2, cy - r),
        (cx + r, cy),
        (cx + r//2, cy + r),
        (cx - r//2, cy + r),
    ]
    draw.polygon(pts, fill=fill, outline=OUTLINE)

def draw_diamond(draw, cx, cy, size, fill):
    r = size // 2
    pts = [
        (cx, cy - r),
        (cx + r, cy),
        (cx, cy + r),
        (cx - r, cy),
    ]
    draw.polygon(pts, fill=fill, outline=OUTLINE)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate a skills block image.")
    parser.add_argument("--output", type=str, default="skills_block.png",
                        help="Output filename")
    return parser.parse_args()

def main():
    args = parse_args()

    print("Enter skills in the format: SkillName yellow green (blue)")
    print("Press ENTER on an empty line to finish.\n")

    skills = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        parts = line.split()
        if len(parts) < 3 or len(parts) > 4:
            print("Format must be: SkillName yellow green (blue)")
            continue
        name = parts[0]
        try:
            yellow = int(parts[1])
            green = int(parts[2])
            blue = 0 if len(parts) <= 3 else int(parts[3])
        except:
            print("Yellow and green and must be integers. Blue must be an integer or omitted.")
            continue
        skills.append((name, yellow, green, blue))

    if not skills:
        print("No skills entered.")
        return

    # Split into two columns
    half = (len(skills) + 1) // 2
    col1 = skills[:half]
    col2 = skills[half:]

    rows = max(len(col1), len(col2))
    height = MARGIN * 2 + rows * ROW_HEIGHT

    img = Image.new("RGBA", (WIDTH, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    font = load_font(16)

    col_width = (WIDTH - MARGIN * 2 - COLUMN_GAP) // 2
    col_x = [MARGIN, MARGIN + col_width + COLUMN_GAP]

    for col_index, column in enumerate([col1, col2]):
        for row_index, (name, yellow, green, blue) in enumerate(column):
            y = MARGIN + row_index * ROW_HEIGHT
            x = col_x[col_index]

            # Skill name
            draw.text((x, y + 6), name, fill=(0, 0, 0), font=font)

            # Shapes start to the right of the skill name
            sx = x + 130
            sy = y + ROW_HEIGHT // 2

            # Yellow hexagons
            for i in range(yellow):
                draw_hexagon(draw, sx + i * (SHAPE_SIZE + 4), sy, SHAPE_SIZE, fill=(255, 215, 0))

            # Green diamonds (no spacing between groups)
            offset = yellow * (SHAPE_SIZE + 4)
            for i in range(green):
                draw_diamond(draw, sx + offset + i * (SHAPE_SIZE + 4), sy, SHAPE_SIZE, fill=(0, 180, 0))

            # Blue squares (no spacing between groups)
            offset = (yellow + green) * (SHAPE_SIZE + 4)
            for i in range(blue):
                draw_square(draw, sx + offset + i * (SHAPE_SIZE + 4), sy, SHAPE_SIZE, fill=(176, 224, 230))

    img.save(args.output)
    print(f"Saved {args.output}")

if __name__ == "__main__":
    main()
