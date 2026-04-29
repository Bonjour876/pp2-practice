import psycopg2
from config import *

def get_connection():
    """
    Establishes a connection to the PostgreSQL database using 
    parameters defined in config.py.
    """
    return psycopg2.connect(
        dbname=DB_NAME, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        host=DB_HOST, 
        port=DB_PORT
    )

def get_or_create_player(username):
    """
    Task 3.1: Username entry & Personal Best.
    Checks if a player exists. If not, creates them.
    Returns the player's ID and their highest score ever recorded.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # 1. Insert player if they don't exist (ON CONFLICT prevents errors for existing names)
    cur.execute(
        "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", 
        (username,)
    )
    conn.commit()
    
    # 2. Get the player's ID
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player_id = cur.fetchone()[0]
    
    # 3. Fetch the Personal Best score for this specific player
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
    best_result = cur.fetchone()[0]
    personal_best = best_result if best_result is not None else 0
    
    cur.close()
    conn.close()
    return player_id, personal_best

def save_game_session(player_id, score, level):
    """
    Task 3.1: Save result.
    Automatically saves the player_id, final score, level reached, 
    and uses the DB default NOW() for the timestamp.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Insert new game session record
    cur.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
        (player_id, score, level)
    )
    
    conn.commit()
    cur.close()
    conn.close()

def get_leaderboard_data():
    """
    Task 3.1 & 3.6: Leaderboard screen.
    Fetches the Top 10 scores. 
    Improved: Uses GROUP BY to show only the BEST attempt per unique username.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # This query groups results by player, so one user doesn't take all 10 spots
    query = """
        SELECT p.username, MAX(s.score) as top_score, MAX(s.level_reached), MAX(s.played_at)
        FROM game_sessions s
        JOIN players p ON s.player_id = p.id
        GROUP BY p.username
        ORDER BY top_score DESC
        LIMIT 10;
    """
    
    cur.execute(query)
    data = cur.fetchall()
    
    cur.close()
    conn.close()
    return data