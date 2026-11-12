import requests as rq
import time

class TMDBClient:
    def __init__(self, token, base_url):
        self.token = token 
        self.BASE_URL = base_url
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }
        self.session = rq.Session()


    def get_movie_details(self, tmdb_id):
        url = f"{self.BASE_URL}/movie/{tmdb_id}"

        for attempt in range(3):
            try:
                response = self.session.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()
                details = (response.json())
                break

            except rq.exceptions.Timeout:
                print(f"Request timed out: {tmdb_id}")
                if attempt == 2:
                    return None
                time.sleep(2 ** attempt)

            except rq.exceptions.HTTPError as e:
                print(f"HTTP error for {tmdb_id}: {e}")
                return None

            except rq.exceptions.RequestException as e:
                print(f"Request failed for {tmdb_id}: {e}")
                return None

        movie_data = [
                details['id'],
                details['title'],
                details['release_date'],
                details['runtime'],
                details['budget'],
                details['revenue'],
                details['vote_average'],
                details['vote_count']
        ]

        genres = details['genres']

        return movie_data, genres


    def get_movie_credits(self, tmdb_id):
        url = f"{self.BASE_URL}/movie/{tmdb_id}/credits"

        for attempt in range(3):
            try:
                response = self.session.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()
                credits = (response.json())
                break

            except rq.exceptions.Timeout:
                print(f"Request timed out: {tmdb_id}")
                if attempt == 2:
                    return None
                time.sleep(2 ** attempt)

            except rq.exceptions.HTTPError as e:
                print(f"HTTP error for {tmdb_id}: {e}")
                return None

            except rq.exceptions.RequestException as e:
                print(f"Request failed for {tmdb_id}: {e}")
                return None
        
        movie_cast = []

        for person in credits['crew']:
            if person['job'] == 'Director':
                movie_cast.append({
                    'id': person['id'],
                    'name': person['name'],
                    'role': person['job'],
                    'character': None 
                })
                break

        for actor in credits['cast'][:5]:
            movie_cast.append({
                'id': actor['id'],
                'name': actor['name'],
                'role': 'Actor',
                'character': actor['character'],
        })
 
        return movie_cast
