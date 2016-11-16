Service that consumes movie_info_downloader package (https://pypi.python.org/pypi/movie-info-downloader/0.0.4).
Technology: Django Rest Framework, PostgreSQL, Redis, Celery, RabbitMQ and Docker.

Installation:
-------------
1. Pull the repo
2. Make sure that docker-compose.yml reflects settings you want
3. Make sure that there is right chmod to run
4. Install docker and docker-compose if you don't have
5. Run by command: docker-compose up

Usage:
-------------
1. POST /movies/download/ - force download new movies
```
{
    "status": "download movies started"
}
```
2. GET /movies/ - list stored movies
```
[
    {
        "url": "http://localhost:8000/movies/12/",
        "genres": [
            {
                "genre": "Music"
            }
        ],
        "title": "World Happiness 2011",
        "rating": 0
    },
    {
        "url": "http://localhost:8000/movies/13/",
        "genres": [
            {
                "genre": "Sci-Fi"
            },
            {
                "genre": "Horror"
            },
            {
                "genre": "Short"
            }
        ],
        "title": "Re-Animator: 1942",
        "rating": 4.5
    }
]
```
3. GET /profiles/ - list profiles
```
[
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
]
```
4. POST /profile/ - create new profile. Body parameters:
```
{
"min_rating": 2,
"whitelist": [{"genre": "horror"}],
"blacklist": []
}
```
5. GET /profile/{profile_id}/ - get detailed profile with recommendations
```
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
```
6. POST /suggestions/{suggestion_id}/like/ - set that you like that recommendation (it was good)
```
{
    "url": "http://localhost:8000/suggestions/1/",
    "movie": {
        "url": "http://localhost:8000/movies/1/",
        "genres": [
            {
                "genre": "Comedy"
            },
            {
                "genre": "Romance"
            }
        ],
        "title": "Eedo Rakam Aado Rakam",
        "rating": 7.4
    },
    "is_dissmissed": false,
    "is_like": true,
    "created_at": "2016-11-16T09:50:56.366376Z",
    "profile": "http://localhost:8000/profiles/2/"
}
```
7. POST /suggestions/{suggestion_id}/dismiss/ - dismiss recommendation (it will hide from recommendation in profile)
```
{
    "url": "http://localhost:8000/suggestions/5/",
    "movie": {
        "url": "http://localhost:8000/movies/19/",
        "genres": [
            {
                "genre": "Comedy"
            },
            {
                "genre": "Thriller"
            }
        ],
        "title": "Damaal Dumeel",
        "rating": 5.3
    },
    "is_dissmissed": true,
    "is_like": false,
    "created_at": "2016-11-16T09:50:56.453982Z",
    "profile": "http://localhost:8000/profiles/2/"
}
```

Details:
-------------
- download movies and update profiles is done via Celery
- download movies task is run every 12 hours vie Celery beat

