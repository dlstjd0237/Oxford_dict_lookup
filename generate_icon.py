"""Generate app icon for OxfordDictLookup - book + magnifying glass design."""
from PIL import Image, ImageDraw, ImageFont
import os

SIZES = [16, 24, 32, 48, 64, 128, 256]


def draw_icon(size):
    """Draw a dictionary icon at the given size."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    s = size  # shorthand

    # === Background: rounded rectangle (dark blue) ===
    pad = int(s * 0.06)
    radius = int(s * 0.15)
    draw.rounded_rectangle(
        [pad, pad, s - pad, s - pad],
        radius=radius,
        fill='#1565C0',
    )

    # === Book shape (white, slightly inset) ===
    bx1 = int(s * 0.15)
    by1 = int(s * 0.18)
    bx2 = int(s * 0.72)
    by2 = int(s * 0.82)
    book_radius = int(s * 0.06)
    draw.rounded_rectangle(
        [bx1, by1, bx2, by2],
        radius=book_radius,
        fill='#FFFFFF',
    )

    # === Book spine (darker stripe on left) ===
    spine_x = bx1 + int(s * 0.08)
    draw.rectangle(
        [bx1, by1, spine_x, by2],
        fill='#BBDEFB',
    )
    # Round the top-left and bottom-left
    draw.rounded_rectangle(
        [bx1, by1, spine_x + int(s * 0.02), by2],
        radius=book_radius,
        fill='#BBDEFB',
    )

    # === Lines on the book (text lines) ===
    line_color = '#90CAF9'
    line_x1 = bx1 + int(s * 0.16)
    line_x2 = bx2 - int(s * 0.06)
    line_h = max(1, int(s * 0.025))
    for i in range(3):
        ly = by1 + int(s * (0.15 + i * 0.12))
        lx2 = line_x2 - (i * int(s * 0.08))  # progressively shorter lines
        draw.rounded_rectangle(
            [line_x1, ly, lx2, ly + line_h],
            radius=max(1, line_h // 2),
            fill=line_color,
        )

    # === Magnifying glass (bottom-right) ===
    # Glass circle
    mg_cx = int(s * 0.68)
    mg_cy = int(s * 0.62)
    mg_r = int(s * 0.16)
    mg_thick = max(2, int(s * 0.04))

    # White fill for glass
    draw.ellipse(
        [mg_cx - mg_r, mg_cy - mg_r, mg_cx + mg_r, mg_cy + mg_r],
        fill='#E3F2FD',
        outline='#FFFFFF',
        width=mg_thick,
    )

    # Handle
    handle_len = int(s * 0.18)
    hx1 = mg_cx + int(mg_r * 0.65)
    hy1 = mg_cy + int(mg_r * 0.65)
    hx2 = hx1 + int(handle_len * 0.7)
    hy2 = hy1 + int(handle_len * 0.7)
    handle_w = max(2, int(s * 0.06))
    draw.line([hx1, hy1, hx2, hy2], fill='#FFFFFF', width=handle_w)
    # Handle cap
    draw.line(
        [hx2 - int(s * 0.02), hy2 - int(s * 0.02), hx2 + int(s * 0.02), hy2 + int(s * 0.02)],
        fill='#BBDEFB',
        width=handle_w + 1,
    )

    # "Abc" text inside magnifying glass
    if s >= 48:
        try:
            font_size = max(8, int(s * 0.11))
            font = ImageFont.truetype("segoeuib.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
        text = "Aa"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(
            (mg_cx - tw // 2, mg_cy - th // 2 - int(s * 0.02)),
            text,
            fill='#1565C0',
            font=font,
        )

    return img


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, 'assets')
    os.makedirs(assets_dir, exist_ok=True)

    # Generate individual sizes
    images = []
    for size in SIZES:
        img = draw_icon(size)
        images.append(img)

    # Save as .ico (multi-size)
    ico_path = os.path.join(assets_dir, 'icon.ico')
    images[0].save(
        ico_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in images],
        append_images=images[1:],
    )
    print(f"Icon saved: {ico_path}")

    # Also save a 256px PNG for reference
    png_path = os.path.join(assets_dir, 'icon.png')
    images[-1].save(png_path)
    print(f"PNG saved: {png_path}")


if __name__ == '__main__':
    main()
