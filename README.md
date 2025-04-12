# Soccer Player Registration System

A simple command-line application to manage soccer players and their goals.

## Features

- Register new players
- Record goals for players
- List all players with their total goals

## Database Structure

The application uses SQLite with two tables:
- `player`: Stores player information (id, name)
- `goals`: Records goals scored by players (id, player_id, quantity)

## Usage

```bash
# Register a new player
python registroFutbol.py register "Player Name"

# Record goals for a player
python registroFutbol.py goals <player_id> <quantity>

# List all players and their goals
python registroFutbol.py list
```

## Requirements

- Python 3.10 or higher
- SQLite3

## Installation

1. Clone this repository
2. No additional dependencies needed - uses Python standard library

## Error Handling

- Validates player existence when recording goals
- Prevents negative goal quantities
- Handles invalid input formats

## Disclaimer
This project is done by sessions and it is not planned | Entity Framework Code First Approach