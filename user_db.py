import sqlite3

DB_NAME = 'users.db'

def create_users_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_games_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    fill_scores_table()


def fill_scores_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM games")
    result = cursor.fetchone()[0] == 0

    if result:
        cursor.execute('''INSERT INTO games (id, name) VALUES 
        (1, "Snake"),
        (2, "Tetris"),
        (3, "Flappy Bird")
        ''')
        conn.commit()
        conn.close()

def create_scores_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            user_id INTEGER,
            game_id INTEGER,
            score INTEGER,
            PRIMARY KEY (user_id, game_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (game_id) REFERENCES games(id)
        )
    ''')
    conn.commit()
    conn.close()


def register(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "User already exists!"


def login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()

    return user is not None, "Login successful!" if user else "Invalid username or password"


def get_user_id_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM users WHERE username=?''', (username,))
    user_id = cursor.fetchone()
    conn.close()

    if user_id:
        return user_id[0]


def get_score(user_id, game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT score FROM scores WHERE user_id=? AND game_id=?', (user_id, game_id))
    score = cursor.fetchone()

    if score:
        conn.close()
        return score[0]
    else:
        cursor.execute('''INSERT INTO scores VALUES (?, ?, ?)''', (user_id, game_id, 0))
        conn.commit()
        conn.close()
        return 0

def get_game_id_by_name(game_name: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM games WHERE LOWER(name)=?''', (game_name.lower(),))
    game_id = cursor.fetchone()
    conn.close()

    if game_id:
        return game_id[0]

def update_score(user_id, game_id, score):
    db_score = get_score(user_id, game_id)
    if score > db_score:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''UPDATE scores SET score=? WHERE user_id=? AND game_id=?''', (score, user_id, game_id))
        conn.commit()
        conn.close()

def get_top_5_highscores(game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT scores.user_id, scores.score, users.username, games.name
        FROM scores
        LEFT OUTER JOIN users ON scores.user_id = users.id
        LEFT OUTER JOIN games ON scores.game_id = games.id
        WHERE scores.game_id=?
        ORDER BY scores.score DESC
        LIMIT 5
    ''', (game_id,))
    res = cursor.fetchall()
    conn.close()

    if res:
        return res

def get_all_game_ids():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT id FROM games''')
    ids = cursor.fetchall()
    conn.close()

    if ids:
        return [x[0] for x in ids]


def create_tables():
    create_users_table()
    create_games_table()
    create_scores_table()
