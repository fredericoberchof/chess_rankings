import requests
import csv
from datetime import datetime, timedelta

BASE_URL = "https://lichess.org/api"

# Part 1 - Fetch top classical players
def get_top_classical_players(limit=50):
    try:
        response = requests.get(f"{BASE_URL}/player/top/{limit}/classical")
        response.raise_for_status()
        data = response.json()
        usernames = [player["username"] for player in data["users"][:limit]]

        # print("[Part 1] Top Classical Players:")
        # print(usernames)

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
            year = entry[0]
            month = entry[1] + 1
            day = entry[2]
            rating = entry[3]
            date = datetime(year, month, day).date().isoformat()
            rating_by_date[date] = rating

        # print(f"[Part 2] Rating history for {username}:")
        # print(rating_by_date)

        return rating_by_date
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rating history for {username}:", e)
        return {}

# Part 3 - Save to CSV (last 30 days)
def get_last_30_days():
    today = datetime.today().date()
    return [(today - timedelta(days=i)).isoformat() for i in reversed(range(30))]

def save_ratings_to_csv(usernames):
    print("Fetching and writing player ratings to CSV...")
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

            # print(f"[Part 3] {username} row:", row)

            writer.writerow(row)

    print("Ratings successfully saved to ratings.csv")

# Main
def main():
    print("Starting Lichess rating fetcher...")

    # Part 1
    top_players = get_top_classical_players()
    if not top_players:
        print("No players found.")
        return

    # Part 2 & 3
    save_ratings_to_csv(top_players)

if __name__ == "__main__":
    main()
