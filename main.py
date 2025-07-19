import requests
import csv
from datetime import datetime, timedelta

BASE_URL = "https://lichess.org/api"

# Part 1 - Fetch top classical players
def print_top_50_classical_players():
    try:
        response = requests.get(f"{BASE_URL}/player/top/50/classical")
        response.raise_for_status()
        data = response.json()
        usernames = [player["username"] for player in data["users"][:50]]
        
        print("[Part 1] Top 50 Classical Players:")
        for username in usernames:
            print(username)
        return usernames
    except requests.exceptions.RequestException as e:
        print("Error fetching top players:", e)
        return []

# Part 2 - Fetch player's classical rating history
def get_player_classical_rating_history(username):
    try:
        response = requests.get(f"{BASE_URL}/user/{username}/rating-history")
        response.raise_for_status()
        data = response.json()

        classical_data = next((item for item in data if item["name"] == "Classical"), None)
        if not classical_data:
            return {}

        history = classical_data["points"]
        rating_by_date = {}

        for entry in history:
            year, month, day, rating = entry[:4]
            date = datetime(year, month + 1, day).date().isoformat()
            rating_by_date[date] = rating

        return rating_by_date
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rating history for {username}:", e)
        return {}

def print_last_30_day_rating_for_top_player():
    players = print_top_50_classical_players()
    if not players:
        return

    top_username = players[0]
    full_history = get_player_classical_rating_history(top_username)

    last_30_days = [(datetime.today().date() - timedelta(days=i)).isoformat() for i in reversed(range(30))]
    rating_by_day = {}
    last_known_rating = "N/A"

    for date in last_30_days:
        if date in full_history:
            last_known_rating = full_history[date]
        rating_by_day[date] = last_known_rating

    print(f"\n[Part 2] Last 30 days of ratings for {top_username}:")
    for date, rating in rating_by_day.items():
        print(f"{date}: {rating}")

# Part 3 - Save to CSV (last 30 days)
def get_last_30_days():
    today = datetime.today().date()
    return [(today - timedelta(days=i)).isoformat() for i in reversed(range(30))]

def save_ratings_to_csv(usernames):
    print("\n[Part 3] Saving all player ratings to ratings.csv...")
    with open("ratings.csv", "w", newline="") as csvfile:
        fieldnames = ["username"] + get_last_30_days()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for username in usernames:
            print(f"Fetching ratings for {username}...")
            history = get_player_classical_rating_history(username)
            row = {"username": username}
            last_known_rating = "N/A"

            for date in get_last_30_days():
                if date in history:
                    last_known_rating = history[date]
                row[date] = last_known_rating

            writer.writerow(row)

    print("Ratings successfully saved to ratings.csv")

# Main
def main():
    print("Starting Lichess Rating Fetcher...\n")

    # Part 1
    print_top_50_classical_players()

    # Part 2
    print_last_30_day_rating_for_top_player()

    # Part 3
    top_players = print_top_50_classical_players()
    if top_players:
        save_ratings_to_csv(top_players)

if __name__ == "__main__":
    main()
