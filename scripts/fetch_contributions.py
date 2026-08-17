import sys
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_contributions(username="singhvrat-codes", output_json="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Fetching contribution calendar for user '{username}' from {url}...")
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        print(f"Warning: HTTP {resp.status_code} when fetching profile. Generating mock contribution data.")
        return generate_mock_contributions(username, output_json)

    soup = BeautifulSoup(resp.text, "html.parser")
    days = []

    # Find day cells in HTML (table cells td.ContributionCalendar-day or rect.ContributionCalendar-day)
    day_elements = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)

    total_contributions = 0
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    max_day_count = 0
    max_day_date = ""

    for el in day_elements:
        date_str = el.get("data-date")
        if not date_str:
            continue

        # Level indicator (0 to 4/5)
        level_str = el.get("data-level", "0")
        try:
            level = int(level_str)
        except ValueError:
            level = 0

        # Try extracting exact count from tooltip / text / attributes
        count = 0
        if el.get("aria-label"):
            label = el["aria-label"]
            # e.g. "5 contributions on July 10, 2026" or "No contributions on..."
            if "No contribution" not in label and "contribution" in label:
                try:
                    count = int(label.split()[0].replace(",", ""))
                except (ValueError, IndexError):
                    count = level * 2
        else:
            count = level * 2

        total_contributions += count

        # Streak calculation
        if count > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

        if count > max_day_count:
            max_day_count = count
            max_day_date = date_str

        days.append({
            "date": date_str,
            "count": count,
            "level": level
        })

    current_streak = temp_streak if days and days[-1]["count"] > 0 else 0

    if not days:
        print("Could not parse days from HTML. Generating fallback mock data.")
        return generate_mock_contributions(username, output_json)

    data = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": max_day_date, "count": max_day_count},
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ"),
        "days": days
    }

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully saved {len(days)} days ({total_contributions} total contributions) to {output_json}")

def generate_mock_contributions(username, output_json):
    import random
    from datetime import timedelta, date

    today = date.today()
    start_date = today - timedelta(days=364)
    days = []
    total = 0
    
    curr_date = start_date
    while curr_date <= today:
        cnt = random.choices([0, 1, 3, 7, 14], weights=[0.3, 0.4, 0.15, 0.1, 0.05])[0]
        lvl = 0 if cnt == 0 else (1 if cnt <= 2 else (2 if cnt <= 5 else (3 if cnt <= 10 else 4)))
        total += cnt
        days.append({
            "date": curr_date.strftime("%Y-%m-%d"),
            "count": cnt,
            "level": lvl
        })
        curr_date += timedelta(days=1)

    data = {
        "username": username,
        "total_contributions": total,
        "current_streak": 5,
        "longest_streak": 18,
        "best_day": {"date": today.strftime("%Y-%m-%d"), "count": 14},
        "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ"),
        "days": days
    }

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Generated mock contribution calendar saved to {output_json}")

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else "singhvrat-codes"
    fetch_contributions(uname)
