import os
import html

def generate_info_card(output_path="info-card.svg", width=490, height=350):
    is_static = os.getenv("STATIC") == "1"

    lines = [
        ("user@github", "-----------------------------", "#58a6ff"),
        ("OS", "Ubuntu / macOS / Windows", "#8b949e"),
        ("Host", "Developer Workstation v2026", "#8b949e"),
        ("Shell", "zsh / bash 5.2", "#8b949e"),
        ("Role", "Full-Stack & Systems Engineer", "#58a6ff"),
        ("Stack", "Python, TypeScript, Rust, Docker", "#7ee787"),
        ("Now", "Building animated SVG profile generators", "#ffa657"),
        ("Highlights", "9,000+ Annual Contribs | Open Source Contributor", "#d2a8ff"),
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .card-bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('  .card-border { fill: none; stroke: #30363d; stroke-width: 1; rx: 10px; ry: 10px; }')
    svg.append('  .top-bar { fill: #161b22; rx: 10px; ry: 10px; }')
    svg.append('  .dot-red { fill: #ff5f56; }')
    svg.append('  .dot-yellow { fill: #ffbd2e; }')
    svg.append('  .dot-green { fill: #27c93f; }')
    svg.append('  .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; fill: #8b949e; font-weight: 600; }')
    svg.append('  .key-text { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; font-weight: bold; fill: #58a6ff; }')
    svg.append('  .val-text { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 13px; fill: #c9d1d9; }')
    
    if not is_static:
        svg.append('  @keyframes fadeIn {')
        svg.append('    from { opacity: 0; transform: translateY(6px); }')
        svg.append('    to { opacity: 1; transform: translateY(0); }')
        svg.append('  }')
        svg.append('  .animated-row { opacity: 0; animation: fadeIn 0.4s ease-out forwards; }')
    
    svg.append('</style>')

    # Base panel & top bar
    svg.append(f'<rect width="{width}" height="{height}" class="card-bg" />')
    svg.append(f'<rect width="{width}" height="32" class="top-bar" />')
    svg.append(f'<rect width="{width - 2}" height="{height - 2}" x="1" y="1" class="card-border" />')
    
    # Terminal Window Dots
    svg.append('<circle cx="18" cy="16" r="5" class="dot-red" />')
    svg.append('<circle cx="34" cy="16" r="5" class="dot-yellow" />')
    svg.append('<circle cx="50" cy="16" r="5" class="dot-green" />')
    svg.append(f'<text x="{width // 2}" y="20" text-anchor="middle" class="title-text">user@github ~ neofetch</text>')

    # Palette badges
    palette_colors = ["#161b22", "#ff5f56", "#27c93f", "#ffbd2e", "#58a6ff", "#bc8cff", "#39d353", "#e6edf3"]

    # Render info rows
    start_y = 65
    row_gap = 28

    for idx, (key, val, color) in enumerate(lines):
        y_pos = start_y + idx * row_gap
        delay = idx * 0.12
        anim_attr = f' class="animated-row" style="animation-delay: {delay:.2f}s;"' if not is_static else ''
        
        svg.append(f'<g{anim_attr}>')
        if key == "user@github":
            svg.append(f'  <text x="24" y="{y_pos}" class="key-text" style="fill: #58a6ff;">{html.escape(key)}</text>')
            svg.append(f'  <text x="140" y="{y_pos}" class="val-text" style="fill: #8b949e;">{html.escape(val)}</text>')
        else:
            svg.append(f'  <text x="24" y="{y_pos}" class="key-text" style="fill: {color};">{html.escape(key)}:</text>')
            svg.append(f'  <text x="130" y="{y_pos}" class="val-text">{html.escape(val)}</text>')
        svg.append('</g>')

    # Render palette blocks row at bottom
    palette_y = start_y + len(lines) * row_gap + 10
    anim_attr = f' class="animated-row" style="animation-delay: {(len(lines) * 0.12):.2f}s;"' if not is_static else ''
    svg.append(f'<g{anim_attr}>')
    for p_idx, p_col in enumerate(palette_colors):
        px = 24 + p_idx * 24
        svg.append(f'  <rect x="{px}" y="{palette_y}" width="20" height="12" rx="3" fill="{p_col}" />')
    svg.append('</g>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Successfully generated Neofetch info card SVG at {output_path}")

if __name__ == "__main__":
    generate_info_card("info-card.svg", width=490, height=350)
