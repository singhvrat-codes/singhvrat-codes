import os
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_NAMES = ["", "Mon", "", "Wed", "", "Fri", ""]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg", width=860, height=210):
    if not os.path.exists(json_path):
        print(f"Contributions JSON missing at {json_path}. Running fetch_contributions.py...")
        import fetch_contributions
        fetch_contributions.fetch_contributions()

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)

    # Grid parameters
    cell_size = 11
    cell_gap = 3.5
    step = cell_size + cell_gap

    start_x = 45
    start_y = 62  # Moved down so month labels (y=48) sit comfortably below header text (y=26)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('<style>')
    svg.append('  .bg { fill: #0d1117; rx: 10px; ry: 10px; }')
    svg.append('  .border { fill: none; stroke: #30363d; stroke-width: 1; rx: 10px; ry: 10px; }')
    svg.append('  .header-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 14px; font-weight: bold; fill: #e6edf3; }')
    svg.append('  .label-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #8b949e; }')
    svg.append('  .legend-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #8b949e; }')
    svg.append('  @keyframes slideDown {')
    svg.append('    from { opacity: 0; transform: translateY(-8px); }')
    svg.append('    to { opacity: 1; transform: translateY(0); }')
    svg.append('  }')
    svg.append('  .cell { opacity: 0; animation: slideDown 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; }')
    svg.append('</style>')

    # Background card
    svg.append(f'<rect width="{width}" height="{height}" class="bg" />')
    svg.append(f'<rect width="{width - 2}" height="{height - 2}" x="1" y="1" class="border" />')

    # Card Title / Summary Header
    svg.append(f'<text x="24" y="26" class="header-text">{total_contribs:,} contributions in the last year</text>')

    # Render Day Labels (Mon, Wed, Fri)
    for idx, dname in enumerate(DAY_NAMES):
        if dname:
            y_pos = start_y + idx * step + 9
            svg.append(f'<text x="22" y="{y_pos}" class="label-text">{dname}</text>')

    # Render 53 Weeks x 7 Days Grid
    num_weeks = 53
    week_idx = 0
    prev_month = -1

    for idx, d in enumerate(days):
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        w_day = (dt.weekday() + 1) % 7  # Sunday=0..Saturday=6

        if idx > 0 and w_day == 0:
            week_idx += 1

        if week_idx >= num_weeks:
            break

        x_pos = start_x + week_idx * step
        y_pos = start_y + w_day * step

        # Render Month Header if new month begins
        if dt.month != prev_month and w_day == 0:
            prev_month = dt.month
            svg.append(f'<text x="{x_pos}" y="{start_y - 12}" class="label-text">{MONTH_NAMES[dt.month - 1]}</text>')

        level = min(d.get("level", 0), len(PALETTE) - 1)
        color = PALETTE[level]

        # Diagonal stagger delay calculation
        delay = (week_idx * 0.015) + (w_day * 0.02)

        svg.append(
            f'<rect x="{x_pos:.1f}" y="{y_pos:.1f}" width="{cell_size}" height="{cell_size}" rx="2.5" '
            f'fill="{color}" class="cell" style="animation-delay: {delay:.2f}s;">'
            f'<title>{d["count"]} contributions on {d["date"]}</title></rect>'
        )

    # Footer Legend (Less -> More scale)
    legend_y = height - 20
    legend_start_x = width - 170

    svg.append(f'<text x="{legend_start_x - 30}" y="{legend_y + 9}" class="legend-text">Less</text>')
    for p_idx, p_col in enumerate(PALETTE):
        px = legend_start_x + p_idx * 14
        svg.append(f'<rect x="{px}" y="{legend_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{p_col}" />')
    svg.append(f'<text x="{legend_start_x + len(PALETTE) * 14 + 6}" y="{legend_y + 9}" class="legend-text">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Successfully generated clean contribution heatmap SVG at {output_path}")

if __name__ == "__main__":
    render_heatmap_svg("data/contributions.json", "contrib-heatmap.svg", width=860, height=210)
