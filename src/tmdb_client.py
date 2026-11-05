import os 
import requests as rq
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")
TMDB_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3/movie"
movieId = 550
url = f"{BASE_URL}/{movieId}"
headers = {
    "Authorization": f"Bearer {TMDB_TOKEN}"
}

respond = rq.get(url, headers=headers)

print(respond.status_code)
print(respond.json())