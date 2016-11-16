from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Genre, Movie, Profile
from .tasks import update_profile

class SuggestServiceTestCase(APITestCase):

    def create_profile(self, min_rating, whitelist, blacklist):
        data = {
            "min_rating": min_rating,
            "whitelist": [{'genre': genre} for genre in whitelist],
            "blacklist": [{'genre': genre} for genre in blacklist]
        }
        self.client.post('/profiles/', data, format='json')
        profile = Profile.objects.all()[0]
        update_profile(profile.id)
        return profile.suggestion_set.all()


class SimpleApiTests(SuggestServiceTestCase):
    def setUp(self):
        action = Genre.objects.create(genre='Action')
        documentary = Genre.objects.create(genre='Documentary')
        batman = Movie.objects.create(title="Batman", rating=8)
        batman.genres.add(action)
        document = Movie.objects.create(title="Document about nothing", rating=3)
        document.genres.add(documentary)

    def test_list_movies(self):
        response = self.client.get('/movies/', {}, format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        genres = Genre.objects.all()
        self.assertEqual(len(genres), 2)

    def test_add_update_profile(self):
        data = {
            "min_rating": 49,
            "whitelist": [{"genre": "Action"}],
            "blacklist": []
        }
        response = self.client.post('/profiles/', data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'min_rating': ['Must be between 1 - 10']})

        data = {
            "min_rating": 4,
            "whitelist": [{"genre": "Action"}, {"genre": "New"}],
            "blacklist": []
        }
        response = self.client.post('/profiles/', data, format='json')
        self.assertEqual(response.status_code, 201)
        # new genre created automatically when is not created
        genres = Genre.objects.all()
        self.assertEqual(len(genres), 3)

        # update profile with new movies
        profile = Profile.objects.all()[0]
        self.assertEqual(len(profile.suggestion_set.all()), 0)
        update_profile(profile.id)
        suggestions = profile.suggestion_set.all()
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0].movie.title, 'Batman')

    def test_dismiss_and_like_option(self):
        data = {
            "min_rating": 4,
            "whitelist": [{"genre": "Action"}, {"genre": "New"}],
            "blacklist": []
        }
        self.client.post('/profiles/', data, format='json')
        profile = Profile.objects.all()[0]
        update_profile(profile.id)
        response = self.client.get(
            '/profiles/{}/'.format(profile.id),
            {},
            format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['suggestions']), 1)
        suggestion_url = data['suggestions'][0]['url']
        response = self.client.get(
            suggestion_url,
            {},
            format='json')
        self.assertEqual(response.status_code, 200)
        # try mark as like
        response = self.client.post(
            '{}like/'.format(suggestion_url),
            {},
            format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['is_like'], True)

        # try mark as dismissed
        response = self.client.post(
            '{}dismiss/'.format(suggestion_url),
            {},
            format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['is_dissmissed'], True)

        # check if dismissed recommendation is hidden in profile recommendation
        response = self.client.get(
            '/profiles/{}/'.format(profile.id),
            {},
            format='json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['suggestions']), 0)


class RecommendationTests(SuggestServiceTestCase):
    def setUp(self):
        action = Genre.objects.create(genre='Action')
        sfi = Genre.objects.create(genre='SFi')
        comedy = Genre.objects.create(genre='Comedy')
        category = Genre.objects.create(genre='Category')
        batman = Movie.objects.create(title="Batman", rating=8)
        batman.genres.add(action, sfi)
        bad_sfi_movie = Movie.objects.create(title="Bad SFi Movie", rating=2)
        bad_sfi_movie.genres.add(sfi, category)
        good_sfi_movie = Movie.objects.create(title="Good SFi Movie", rating=9)
        good_sfi_movie.genres.add(sfi, category)
        weird = Movie.objects.create(title="Weird", rating=9)
        weird.genres.add(action, sfi, comedy)

    def test_whitelist(self):
        suggestions = self.create_profile(3, ['Action'], [])
        self.assertEqual(len(suggestions), 2)  # batman, weird

    def test_whitelist_two_genres(self):
        suggestions = self.create_profile(1, ['Action', 'SFi'], [])
        self.assertEqual(len(suggestions), 4)  # all 4 movies

    def test_whitelist_min_rating(self):
        suggestions = self.create_profile(7, ['Category'], [])
        self.assertEqual(len(suggestions), 1)  # good sfi movie

    def test_whitelist_and_blacklist(self):
        suggestions = self.create_profile(1, ['Action'], ['Category'])
        self.assertEqual(len(suggestions), 2)  # batman, weird