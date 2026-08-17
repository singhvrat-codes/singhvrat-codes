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

def build_braille_ascii_svg(ascii_str, output_path="avi-ascii.svg", width=370, height=360):
    ascii_rows = [line for line in ascii_str.strip("\n").split("\n")]
    cols = max(len(line) for line in ascii_rows)
    rows = len(ascii_rows)

    padding_x = 14
    target_text_width = width - (padding_x * 2)

    # Top terminal bar offset
    top_bar_height = 32
    start_y = top_bar_height + 12
    available_height = height - start_y - 12
    line_height = available_height / rows
    font_size = line_height * 0.76

    total_duration = 3.5  # seconds
    row_duration = total_duration / max(1, rows)

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_lines.append('<style>')
    svg_lines.append(f'  .ascii-text {{ font-family: "Cascadia Code", "Fira Code", "Courier New", Consolas, monospace; font-size: {font_size:.2f}px; fill: #e6edf3; white-space: pre; font-weight: bold; }}')
    svg_lines.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg_lines.append('  .border { fill: none; stroke: #30363d; stroke-width: 1; rx: 10px; ry: 10px; }')
    svg_lines.append('  .top-bar { fill: #161b22; rx: 10px; ry: 10px; }')
    svg_lines.append('  .dot-red { fill: #ff5f56; }')
    svg_lines.append('  .dot-yellow { fill: #ffbd2e; }')
    svg_lines.append('  .dot-green { fill: #27c93f; }')
    svg_lines.append('  .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: #8b949e; font-weight: 600; }')
    svg_lines.append('</style>')

    # Base panel & top bar matching Neofetch card style
    svg_lines.append(f'<rect width="{width}" height="{height}" class="bg" />')
    svg_lines.append(f'<rect width="{width}" height="{top_bar_height}" class="top-bar" />')
    svg_lines.append(f'<rect width="{width - 2}" height="{height - 2}" x="1" y="1" class="border" />')

    # Terminal Window Control Dots
    svg_lines.append('<circle cx="18" cy="16" r="5" class="dot-red" />')
    svg_lines.append('<circle cx="34" cy="16" r="5" class="dot-yellow" />')
    svg_lines.append('<circle cx="50" cy="16" r="5" class="dot-green" />')
    svg_lines.append(f'<text x="{width // 2}" y="20" text-anchor="middle" class="title-text">singhvrat-codes@github ~ ascii</text>')

    # Define Clip Paths for row-by-row horizontal typing animation
    svg_lines.append('<defs>')
    for r in range(rows):
        start_time = r * row_duration
        clip_y = start_y + r * line_height
        svg_lines.append(f'  <clipPath id="row-clip-{r}">')
        svg_lines.append(f'    <rect x="{padding_x}" y="{clip_y - 2:.1f}" width="0" height="{line_height + 4:.1f}">')
        svg_lines.append(f'      <animate attributeName="width" from="0" to="{target_text_width + 20}" begin="{start_time:.2f}s" dur="{row_duration:.2f}s" fill="freeze" />')
        svg_lines.append('    </rect>')
        svg_lines.append('  </clipPath>')
    svg_lines.append('</defs>')

    # Render ASCII text with textLength to stretch edge-to-edge seamlessly
    for r, line in enumerate(ascii_rows):
        y_pos = start_y + (r + 0.8) * line_height
        escaped_line = html.escape(line)
        svg_lines.append(
            f'  <text x="{padding_x}" y="{y_pos:.1f}" textLength="{target_text_width}" lengthAdjust="spacingAndGlyphs" '
            f'class="ascii-text" clip-path="url(#row-clip-{r})">{escaped_line}</text>'
        )

    svg_lines.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"Successfully generated Full-Card Terminal Braille ASCII SVG at {output_path}")

if __name__ == "__main__":
    build_braille_ascii_svg(USER_ASCII_ART, "avi-ascii.svg", width=370, height=360)
