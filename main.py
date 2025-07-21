"""
Lichess Classical Chess Ratings Fetcher

This script fetches the top 50 classical chess players from Lichess, prints their usernames, displays the last 30 days of rating history for the top player, and generates a CSV file with the 30-day rating history for all top 50 players.
"""

import requests
import csv
from datetime import datetime, timedelta
import time

BASE_URL = "https://lichess.org/api"

# Part 1 - Fetch top classical players
def print_top_50_classical_players():
    """
    Fetch and print the usernames of the top 50 classical chess players from Lichess.

    Returns:
        list: List of usernames of the top 50 classical players.
    """
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
    """
    Fetch the classical rating history for a given player from Lichess.

    Args:
        username (str): The Lichess username.

    Returns:
        dict: Dictionary mapping ISO date strings to ratings for the classical variant.
    """
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
    """
    Print the last 30 days of classical ratings for the top player.
    If the player did not play on a given day, the rating remains the same as the previous day.
    Output format: username, {Sep 15: 990, Sep 14: 991, ..., Aug 17: 932, Aug 16: 1000}
    """
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

    formatted_ratings = ', '.join([
        f"{datetime.strptime(date, '%Y-%m-%d').strftime('%b %d')}: {rating_by_day[date]}" for date in last_30_days[::-1]
    ])
    print(f"\n[Part 2] Last 30 days of ratings for {top_username}:")
    print(f"{top_username}, {{{formatted_ratings}}}")

# Part 3 - Save to CSV (last 30 days)
def get_last_30_days():
    """
    Get a list of the last 30 days as ISO date strings (from 30 days ago to today).

    Returns:
        list: List of ISO date strings.
    """
    today = datetime.today().date()
    return [(today - timedelta(days=i)).isoformat() for i in reversed(range(30))]

def save_ratings_to_csv(usernames):
    """
    Save the last 30 days of classical ratings for each player in usernames to a CSV file.
    The first column is the username, followed by one column per day (oldest to newest).

    Args:
        usernames (list): List of Lichess usernames.
    """
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
            time.sleep(1)

    print("Ratings successfully saved to ratings.csv")

# Main
def main():
    """
    Main function to run all parts: print top 50 players, print last 30 days for top player, and save all ratings to CSV.
    """
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
