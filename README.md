Service that consumes movie_info_downloader package (https://pypi.python.org/pypi/movie-info-downloader/0.0.4).
Technology: Django Rest Framework, PostgreSQL, Redis, Celery, RabbitMQ and Docker.

Installation:
1. Pull the repo
2. Make sure that docker-compose.yml reflects settings you want
3. Make sure that there is right chmod to run
4. Install docker and docker-compose if you don't have
5. Run by command: docker-compose up

Usage:
1. POST /movies/download/ - force download new movies
2. GET /movies/ - list stored movies
3. GET /profiles/ - list profile
4. POST /profile/ - create new profile. Body parameters:
{
"min_rating": 2,
"whitelist": [{"genre": "horror"}],
"blacklist": []
}
5. GET /profile/{profile_id}/ - get detailed profile with recommendations
Example:
{
    "url": "http://localhost:8000/profiles/2/",
    "whitelist": [
        {
            "genre": "Comedy"
        }
    ],
    "blacklist": [],
    "suggestions": [
        {
            "url": "http://localhost:8000/suggestions/6/",
            "movie": {
                "url": "http://localhost:8000/movies/22/",
                "genres": [
                    {
                        "genre": "Comedy"
                    },
                    {
                        "genre": "Adventure"
                    },
                    {
                        "genre": "Fantasy"
                    },
                    {
                        "genre": "Musical"
                    },
                    {
                        "genre": "Animation"
                    },
                    {
                        "genre": "Family"
                    }
                ],
                "title": "Pete's Dragon",
                "rating": 6.3
            },
            "is_dissmissed": false,
            "is_like": false,
            "created_at": "2016-11-16T09:50:56.469989Z",
            "profile": "http://localhost:8000/profiles/2/"
        }
    ],
    "min_rating": 1
}
6. POST /suggestions/{suggestion_id}/like/ - set that you like that recommendation (it was good)
7. POST /suggestions/{suggestion_id}/dismiss/ - dismiss recommendation (it will hide from recommendation in profile)

Details:
- download movies and update profiles is done via Celery
- download movies task is run every 12 hours vie Celery beat

