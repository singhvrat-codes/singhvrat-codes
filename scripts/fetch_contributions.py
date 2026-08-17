import sys
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def fetch_via_graphql(username, token):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": "GitHub-Profile-Art-Generator"
    }

    query = """
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
    """

    print(f"Fetching contribution calendar for user '{username}' via GitHub GraphQL API...")
    resp = requests.post(url, json={"query": query, "variables": {"username": username}}, headers=headers)
    
    if resp.status_code != 200:
        print(f"GraphQL request failed with status code {resp.status_code}")
        return None

    res_data = resp.json()
    if "errors" in res_data or "data" not in res_data or not res_data["data"]["user"]:
        print("GraphQL returned errors or empty user object:", res_data.get("errors"))
        return None

    calendar = res_data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    total_contributions = calendar["totalContributions"]

    level_map = {
        "NONE": 0,
        "FIRST_QUARTILE": 1,
        "SECOND_QUARTILE": 2,
        "THIRD_QUARTILE": 3,
        "FOURTH_QUARTILE": 4
    }

    days = []
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    max_day_count = 0
    max_day_date = ""

    for week in calendar["weeks"]:
        for d in week["contributionDays"]:
            date_str = d["date"]
            count = d["contributionCount"]
            level = level_map.get(d["contributionLevel"], 0)

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

    return {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": max_day_date, "count": max_day_count},
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "days": days
    }

def fetch_contributions(username="singhvrat-codes", output_json="data/contributions.json"):
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    
    # 1. Try official GraphQL API first if token is available
    if token:
        graphql_data = fetch_via_graphql(username, token)
        if graphql_data:
            save_contributions(graphql_data, output_json)
            return

    # 2. Fallback to public HTML endpoint
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Fetching contribution calendar for user '{username}' from {url}...")
    resp = requests.get(url, headers=headers)

    if resp.status_code != 200:
        print(f"Warning: HTTP {resp.status_code} when fetching profile.")
        if os.path.exists(output_json):
            print(f"Preserving existing local cache at {output_json} to prevent rate-limit data loss.")
            return
        else:
            return generate_mock_contributions(username, output_json)

    soup = BeautifulSoup(resp.text, "html.parser")
    days = []

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

        level_str = el.get("data-level", "0")
        try:
            level = int(level_str)
        except ValueError:
            level = 0

        count = 0
        if el.get("aria-label"):
            label = el["aria-label"]
            if "No contribution" not in label and "contribution" in label:
                try:
                    count = int(label.split()[0].replace(",", ""))
                except (ValueError, IndexError):
                    count = level * 2
        else:
            count = level * 2

        total_contributions += count

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
        print("Could not parse days from HTML.")
        if os.path.exists(output_json):
            print(f"Preserving existing local cache at {output_json}.")
            return
        else:
            return generate_mock_contributions(username, output_json)

    data = {
        "username": username,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": {"date": max_day_date, "count": max_day_count},
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "days": days
    }

    save_contributions(data, output_json)

def save_contributions(data, output_json):
    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Successfully saved {len(data['days'])} days ({data['total_contributions']} total contributions) to {output_json}")

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
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "days": days
    }

    save_contributions(data, output_json)

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else "singhvrat-codes"
    fetch_contributions(uname)
