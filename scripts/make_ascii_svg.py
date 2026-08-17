import os
import html
import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)

def image_to_ascii(img_path, target_cols=90, aspect_ratio=0.55):
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Input prepped image not found at {img_path}. Run prep_photo.py first.")

    img = Image.open(img_path).convert("L")
    w, h = img.size
    target_rows = int((h / w) * target_cols * aspect_ratio)

    img_resized = img.resize((target_cols, target_rows), Image.Resampling.LANCZOS)
    pixels = np.array(img_resized)

    # Normalize pixels 0..255 to 0..len(RAMP)-1
    num_chars = len(RAMP)
    ascii_rows = []
    for row in pixels:
        row_str = ""
        for p in row:
            # Map dark pixels to dense chars, light pixels to space
            idx = int((255 - p) / 255.0 * (num_chars - 1))
            row_str += RAMP[idx]
        ascii_rows.append(row_str)

    return ascii_rows

def build_ascii_svg(ascii_rows, output_path="avi-ascii.svg", width=370):
    cols = len(ascii_rows[0])
    rows = len(ascii_rows)

    font_size = 9.5
    line_height = 11.2
    char_width = 5.7

    svg_width = width
    svg_height = int(rows * line_height + 40)

    # Calculate typing animation timing
    total_duration = 3.5  # seconds
    row_duration = total_duration / max(1, rows)

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('<style>')
    svg_lines.append('  .ascii-text { font-family: "Courier New", Courier, monospace; font-size: 9.5px; fill: #e6edf3; white-space: pre; font-weight: bold; }')
    svg_lines.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg_lines.append('  .border { fill: none; stroke: #30363d; stroke-width: 1; rx: 10px; ry: 10px; }')
    svg_lines.append('</style>')

    # Background card
    svg_lines.append(f'<rect width="{svg_width}" height="{svg_height}" class="bg" />')
    svg_lines.append(f'<rect width="{svg_width - 2}" height="{svg_height - 2}" x="1" y="1" class="border" />')

    # Define Clip Paths for row-by-row horizontal typing animation
    svg_lines.append('<defs>')
    for r in range(rows):
        start_time = r * row_duration
        svg_lines.append(f'  <clipPath id="row-clip-{r}">')
        svg_lines.append(f'    <rect x="20" y="{20 + r * line_height - 9}" width="0" height="{line_height + 2}">')
        svg_lines.append(f'      <animate attributeName="width" from="0" to="{cols * char_width + 10}" begin="{start_time:.2f}s" dur="{row_duration:.2f}s" fill="freeze" />')
        svg_lines.append('    </rect>')
        svg_lines.append('  </clipPath>')
    svg_lines.append('</defs>')

    # Render ASCII text with clip-paths
    for r, line in enumerate(ascii_rows):
        y_pos = 20 + r * line_height
        escaped_line = html.escape(line)
        svg_lines.append(f'  <text x="20" y="{y_pos:.1f}" class="ascii-text" clip-path="url(#row-clip-{r})">{escaped_line}</text>')

    # Add cursor effect riding the typewriter edge
    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Successfully generated animated ASCII SVG at {output_path}")

if __name__ == "__main__":
    prepped_img = "data/source-prepped.png"
    if not os.path.exists(prepped_img):
        print("Prepped photo missing. Running prep_photo.py first...")
        import prep_photo
        prep_photo.process_photo("source-photo.jpg")

    rows = image_to_ascii(prepped_img, target_cols=56)
    build_ascii_svg(rows, "avi-ascii.svg", width=370)
