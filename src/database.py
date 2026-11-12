import sqlite3



def create_tables():
    connection = sqlite3.connect("data/movies.db")
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            tmdb_id INTEGER PRIMARY KEY,
            title TEXT,
            release_date TEXT,
            runtime INTEGER,
            budget INTEGER,
            revenue INTEGER,
            vote_average REAL,
            vote_count INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genres(
            id INTEGER PRIMARY KEY,
            genre TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_genres (
            tmdb_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (tmdb_id, genre_id),
            FOREIGN KEY (tmdb_id) REFERENCES movies(tmdb_id),
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people(
            person_id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movie_credits(
            tmdb_id INTEGER,
            person_id INTEGER,
            role TEXT,
            character TEXT,
            PRIMARY KEY(tmdb_id, person_id),
            FOREIGN KEY (tmdb_id) REFERENCES movies(tmdb_id),
            FOREIGN KEY (person_id) REFERENCES people(person_id)
        )
    """)


    connection.commit()
    connection.close()



def save_movie(details, genres, cast):
    connection = sqlite3.connect("data/movies.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO movies
        VALUES (?,?,?,?,?,?,?,?)
    """, details)

    for genre in genres:
        cursor.execute("""
            INSERT OR IGNORE INTO genres
            VALUES (?,?)
        """, (genre['id'], genre['name']))

        cursor.execute("""
            INSERT OR IGNORE INTO movie_genres
            VALUES(?,?)
        """, (details[0], genre['id']))

    for person in cast:

        cursor.execute("""
            INSERT OR IGNORE INTO people
            VALUES(?,?)
        """, (person['id'], person['name']))
                
        cursor.execute("""
            INSERT OR IGNORE INTO movie_credits
            VALUES(?,?,?,?)
        """, (details[0], person['id'], person['role'], person['character']))


    connection.commit()
    connection.close()

def get_movie_info(tmdb_id):
    connection = sqlite3.connect("data/movies.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * 
        FROM movies 
        WHERE tmdb_id = ?
    """, (tmdb_id,))

    result = cursor.fetchone()
    connection.close()

    return result

def get_movie_genres(tmdb_id):
    connection = sqlite3.connect("data/movies.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT movies.title, genres.genre 
        FROM movies
        JOIN movie_genres
            ON movies.tmdb_id = movie_genres.tmdb_id
        JOIN genres
            ON movie_genres.genre_id = genres.id
        WHERE movies.tmdb_id = ?
    """, (tmdb_id,))

    result = cursor.fetchall()
    connection.close()

    return result

def get_movie_credits(tmdb_id):
    connection = sqlite3.connect("data/movies.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.person_id, p.name, m.role, m.character
        FROM movie_credits m
        JOIN people p 
            ON p.person_id = m.person_id
        WHERE m.tmdb_id = ?
    """, (tmdb_id,))

    result = cursor.fetchall()
    connection.close()

    return result
