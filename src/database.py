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

    connection.commit()
    connection.close()



def save_movie(details, genres):
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

    result = cursor.fetchall()
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