from django.conf.urls import url, include  
from rest_framework import routers

from suggest_service import views


router = routers.DefaultRouter()  
router.register(r'movies', views.MovieViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'suggestions', views.SuggestionViewSet)

urlpatterns = [  
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]