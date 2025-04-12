import sqlite3
import sys

def create_tables():
    conn = sqlite3.connect('soccer.db')
    cursor = conn.cursor()
    
    # Player table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES player (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def register_player(name):
    conn = sqlite3.connect('soccer.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO player (name) VALUES (?)', (name,))
    
    conn.commit()
    conn.close()
    print(f"Player '{name}' successfully registered")

def register_goals(player_id, quantity):
    conn = sqlite3.connect('soccer.db')
    cursor = conn.cursor()
    
    # Check if player exists
    cursor.execute('SELECT id FROM player WHERE id = ?', (player_id,))
    if not cursor.fetchone():
        print(f"Error: No player exists with ID {player_id}")
        conn.close()
        return False
    
    cursor.execute('INSERT INTO goals (player_id, quantity) VALUES (?, ?)', 
                  (player_id, quantity))
    
    conn.commit()
    conn.close()
    print(f"Recorded {quantity} goals for player ID {player_id}")
    return True

def list_players():
    conn = sqlite3.connect('soccer.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT p.id, p.name, COALESCE(SUM(g.quantity), 0) as total_goals
        FROM player p
        LEFT JOIN goals g ON p.id = g.player_id
        GROUP BY p.id, p.name
    ''')
    players = cursor.fetchall()
    
    for player in players:
        print(f"ID: {player[0]}, Name: {player[1]}, Total goals: {player[2]}")
    
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python registroFutbol.py <command> [arguments]")
        print("Available commands:")
        print("  register <player_name>      - Register a new player")
        print("  goals <player_id> <quantity> - Record goals for a player")
        print("  list                        - Show all players and their goals")
        sys.exit(1)
        
    create_tables()
    command = sys.argv[1]
    
    match command:
        case "register":
            if len(sys.argv) != 3:
                print("Error: Must provide player name")
                sys.exit(1)
            player_name = sys.argv[2]
            register_player(player_name)
        case "goals":
            if len(sys.argv) != 4:
                print("Error: Must provide player ID and goal quantity")
                sys.exit(1)
            try:
                player_id = int(sys.argv[2])
                quantity = int(sys.argv[3])
                if quantity < 0:
                    raise ValueError("Goal quantity cannot be negative")
                register_goals(player_id, quantity)
            except ValueError as e:
                print(f"Error: {str(e)}")
                sys.exit(1)
        case "list":
            list_players()
        case _:
            print(f"Error: Unrecognized command '{command}'")
            sys.exit(1)