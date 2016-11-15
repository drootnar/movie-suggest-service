from datetime import timedelta
from movie_info_downloader import get_latest_movies
from celery.decorators import task, periodic_task

from .celeryconf import app
from .models import Movie, Genre, Profile, Suggestion

# every 12 h
@periodic_task(run_every=timedelta(seconds=60))
def periodic_grab_movies():
    grab_movies.delay()

@app.task()
def grab_movies():
    movies = get_latest_movies()
    for movie in movies.values():
        title = movie['title']
        genres = movie.get('genres', [])
        rating = movie.get('rating', 0)
        new_movies = []
        (movie_obj, created) = Movie.objects.get_or_create(title=title, rating=rating)
        if created:
            new_movies.append(title)
            for genre in genres:
                (genre_obj, genre_created) = Genre.objects.get_or_create(genre=genre)
                movie_obj.genres.add(genre_obj)
        movie_obj.save()

    profiles = Profile.objects.all()
    if new_movies:
        for profile in profiles:
            update_profile.delay(profile.id, new_movies)


@app.task()
def update_profile(profile_id, new_titles=None):
    profile = Profile.objects.get(id=profile_id)
    if new_titles:
        movies = Movie.objects.filter(title__in=new_titles)
    else:
        movies = Movie.objects.all()
    profile_whitelist = set(profile.whitelist.all())
    profile_blacklist = set(profile.blacklist.all())
    for movie_obj in movies:
        movie_genres = set(movie_obj.genres.all())
        if movie_obj.rating < profile.min_rating or (profile_blacklist & movie_genres):
            continue
        elif profile_whitelist & movie_genres:
            suggestion = Suggestion(profile=profile, movie=movie_obj)
            suggestion.save()

