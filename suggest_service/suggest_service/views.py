from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .models import Movie, Profile, Suggestion
from .serializers import MovieSerializer, ProfileSerializer, SuggestionSerializer
from .tasks import grab_movies


class MovieViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows profile to be viewed or created.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @list_route(methods=['post'])
    def download(self, request, pk=None):
        grab_movies.delay()
        return Response({'status': 'download movies started'})


class ProfileViewSet(mixins.CreateModelMixin,  
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows profile to be viewed or created.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SuggestionViewSet(mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    """
    API endpoint that allows profile to be viewed or created.
    """
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionSerializer

    @detail_route(methods=['post'])
    def dismiss(self, request, pk=None):
        suggestion = self.get_object()
        suggestion.is_dissmissed = True
        suggestion.save()
        return Response(SuggestionSerializer(suggestion, context={'request': request}).data)

    @detail_route(methods=['post'])
    def like(self, request, pk=None):
        suggestion = self.get_object()
        suggestion.is_like = True
        suggestion.save()
        return Response(SuggestionSerializer(suggestion, context={'request': request}).data)
