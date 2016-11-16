from rest_framework import serializers

from .models import Movie, Genre, Profile, Suggestion
from .tasks import update_profile

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields =('genre',) 


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('created_at', 'updated_at')

    def create(self, validated_data):
        genres = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        movie.save()
        for genre in genres:
            (genre_obj, created) = Genre.objects.get_or_create(genre=genre['genre'])
            movie.genres.add(genre_obj)
        return movie


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Suggestion
        read_only_fields = ('id', 'profile', 'movie',)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    whitelist = GenreSerializer(many=True)
    blacklist = GenreSerializer(many=True)
    suggestions = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ('movies',)

    def validate_min_rating(self, value):
        if value <= 0 or value > 10:
            raise serializers.ValidationError("Must be between 1 - 10")
        return value

    def create(self, validated_data):
        whitelist = validated_data.pop('whitelist')
        blacklist = validated_data.pop('blacklist')
        profile = Profile(**validated_data)
        profile.save()
        for genre in whitelist:
            (genre_obj, created) = Genre.objects.get_or_create(genre=genre['genre'])
            profile.whitelist.add(genre_obj)
        for genre in blacklist:
            (genre_obj, created) = Genre.objects.get_or_create(genre=genre['genre'])
            profile.blacklist.add(genre_obj)
        update_profile.delay(profile.id)
        return profile

    def get_suggestions(self, obj):
        request = self.context['request']
        suggestions = Suggestion.objects.filter(is_dissmissed=False, profile=obj)
        return SuggestionSerializer(suggestions, many=True, context={'request': request}).data
