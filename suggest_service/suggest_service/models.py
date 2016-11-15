from django.db import models


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=200)

    def __repr__(self):
        return self.genre

    def __str__(self):
        return self.genre


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    rating = models.FloatField()
    genres = models.ManyToManyField(Genre, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return u'{} {}'.format(self.id, self.title)

    def __str__(self):
        return u'{} {}'.format(self.id, self.title)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    min_rating = models.FloatField()
    whitelist = models.ManyToManyField(Genre, blank=True, related_name='whitelist')
    blacklist = models.ManyToManyField(Genre, blank=True, related_name='blacklist')
    movies = models.ManyToManyField(Movie, blank=True, through='Suggestion')

    def __repr__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class Suggestion(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    is_dissmissed = models.BooleanField(default=False)
    is_like = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
