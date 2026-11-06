import requests as rq

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

        respond = self.session.get(url, headers=self.headers)
        respond.raise_for_status()
        details = (respond.json())
        
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


#     def get_movie_credits(self, tmdb_id):
#         url = f"{self.BASE_URL}/movie/{tmdb_id}/credits"
#         respond = self.session.get(url, headers=self.headers)
#         respond.raise_for_status()
#         return respond.json()
