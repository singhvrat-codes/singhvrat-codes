import os
import html

# User's exact Ferrari F40 Braille / ASCII art
USER_ASCII_ART = """⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠏⠁⠀⠠⠤⠤⢤⣤⣤⠄⠀⣀⣀⡉⠉⠛⠻⢿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⣉⣭⣽⣿⣶⣶⣶⡶⠶⡆⣠⡬⠭⣤⠄⠀⡀⠀⠀⠀⠯⠭⠍⠓⠒⠂⠀⣠⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⡿⠟⠋⣁⣠⣴⠤⠄⠈⠉⠉⠉⠛⠛⠻⠿⠖⠋⠙⠀⠀⠈⠀⠀⠀⠉⢉⡓⠶⠆⣀⣤⣶⣶⣶⣭⢻⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠴⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠔⠁⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⠿⣛⣭⣷⣿⡿⠛⠛⠁⣾⣿
⣿⣿⣿⣿⣿⠿⣋⣥⣄⣐⣄⠀⠀⠀⠐⠀⠂⠀⠀⠄⠀⢄⡀⢤⡴⢒⠀⢠⠊⠀⠀⢀⣤⡀⠀⣤⣾⠿⢛⡍⢰⡶⣶⡄⠈⠙⠀⠀⠀⢹⣿⣿
⣿⣿⣿⡿⠁⣮⣾⣿⣿⣿⣿⣿⣶⣤⣤⣤⣄⣀⣀⣀⣀⠀⠀⠀⠀⣀⣀⣀⣀⡀⡀⠀⢤⠴⠚⢭⣶⣿⣿⡏⣰⣿⣿⡿⠀⠀⠀⠀⠀⠀⣿⣿
⣿⣿⠟⠀⢀⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠋⢉⣽⠿⣛⣯⣴⣿⣿⣿⠿⠛⠛⢿⢑⡥⠒⠁⠀⣸⠿⠛⢙⡀⠹⠟⠛⣡⠀⠀⠀⠀⠀⠀⣾⣿
⣿⡏⣴⢂⠳⠬⣛⣻⡿⠿⢿⣷⣶⣶⣶⠾⠟⡏⣀⡭⣠⣼⣿⣿⡿⠁⠀⠀⠀⠀⣸⠁⠀⠀⡠⠔⠠⠔⠊⠁⠀⠀⠀⣀⡴⣷⣶⣶⣿⣷⣿⣿
⣿⡿⠀⠿⣷⣶⣏⡽⣁⣉⣁⣒⣲⣶⣶⣄⣀⣇⣴⣾⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⡻⠦⠀⠀⠀⠀⠀⠀⣀⣠⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⡟⠁⠀⠀⠀⠉⠛⠛⠛⠛⠻⠿⠿⠛⠛⠛⠛⠛⠻⢿⣿⠟⠉⠁⠀⠀⠀⠀⠀⠀⠠⠀⣀⡤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣤⠤⠀⠀⠀⠀⠀⠀⠴⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣶⣦⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢶⣤⣀⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""

def build_braille_ascii_svg(ascii_str, output_path="avi-ascii.svg", width=370):
    ascii_rows = [line for line in ascii_str.strip("\n").split("\n")]
    cols = max(len(line) for line in ascii_rows)
    rows = len(ascii_rows)

    # Typography and grid sizing
    font_size = 9.8
    line_height = 14.5
    char_width = 4.7

    svg_width = width
    content_width = cols * char_width
    padding_x = max(14, (svg_width - content_width) / 2)
    svg_height = int(rows * line_height + 65)

    # Calculate typing animation timing
    total_duration = 3.5  # seconds
    row_duration = total_duration / max(1, rows)

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('<style>')
    svg_lines.append('  .ascii-text { font-family: "Cascadia Code", "Fira Code", "Courier New", Consolas, monospace; font-size: 9.8px; fill: #e6edf3; white-space: pre; font-weight: bold; }')
    svg_lines.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg_lines.append('  .border { fill: none; stroke: #30363d; stroke-width: 1; rx: 10px; ry: 10px; }')
    svg_lines.append('  .header-badge { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 11px; font-weight: bold; fill: #ff4d4d; }')
    svg_lines.append('</style>')

    # Background card
    svg_lines.append(f'<rect width="{svg_width}" height="{svg_height}" class="bg" />')
    svg_lines.append(f'<rect width="{svg_width - 2}" height="{svg_height - 2}" x="1" y="1" class="border" />')

    # Card Title
    svg_lines.append('<text x="20" y="24" class="header-badge">🏎️ FERRARI F40</text>')

    # Define Clip Paths for row-by-row horizontal typing animation
    start_y = 44
    svg_lines.append('<defs>')
    for r in range(rows):
        start_time = r * row_duration
        svg_lines.append(f'  <clipPath id="row-clip-{r}">')
        svg_lines.append(f'    <rect x="{padding_x:.1f}" y="{start_y + r * line_height - 11:.1f}" width="0" height="{line_height + 4}">')
        svg_lines.append(f'      <animate attributeName="width" from="0" to="{cols * char_width + 30}" begin="{start_time:.2f}s" dur="{row_duration:.2f}s" fill="freeze" />')
        svg_lines.append('    </rect>')
        svg_lines.append('  </clipPath>')
    svg_lines.append('</defs>')

    # Render ASCII text with clip-paths
    for r, line in enumerate(ascii_rows):
        y_pos = start_y + r * line_height
        escaped_line = html.escape(line)
        svg_lines.append(f'  <text x="{padding_x:.1f}" y="{y_pos:.1f}" class="ascii-text" clip-path="url(#row-clip-{r})">{escaped_line}</text>')

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Successfully generated Ferrari F40 Braille ASCII SVG at {output_path}")

if __name__ == "__main__":
    build_braille_ascii_svg(USER_ASCII_ART, "avi-ascii.svg", width=370)
