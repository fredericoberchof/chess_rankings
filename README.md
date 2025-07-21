# Chess Rankings - Lichess API Integration

A Python application that fetches and analyzes classical chess player rankings and rating histories from the Lichess API.

## Features

- **Top Players Fetching**: Retrieves the top 50 classical chess players from Lichess
- **Rating History Analysis**: Gets detailed rating history for individual players
- **CSV Export**: Generates a comprehensive CSV file with 30-day rating history for all top players

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fredericoberchof/chess_rankings.git
cd chess_rankings
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script to fetch top players and generate the CSV file:

```bash
python main.py
```

### What the script does:

1. **Fetches Top 50 Classical Players**: Gets the current top 50 classical chess players from Lichess
2. **Retrieves Rating Histories**: For each player, fetches their classical rating history
3. **Generates CSV Report**: Creates a `ratings.csv` file with 30-day rating history for all players

### Output

The script generates a `ratings.csv` file with the following structure:
- **Username**: Player's Lichess username
- **Date columns**: Last 30 days of ratings (YYYY-MM-DD format)
- **Rating values**: Classical rating for each date, or "N/A" if no rating change occurred

## API Endpoints Used

This project uses the following Lichess API endpoints:

- `GET /api/player/top/{limit}/classical` - Get top classical players
- `GET /api/user/{username}/rating-history` - Get player's rating history

## Dependencies

- `requests`: HTTP library for API calls
- `csv`: Built-in CSV handling
- `datetime`: Date and time utilities

## Error Handling

The application includes comprehensive error handling for:
- Network request failures
- API rate limiting
- Missing player data
- Invalid responses

## Author

Developed by [Frederico Berchof](https://github.com/fredericoberchof/chess_rankings)

