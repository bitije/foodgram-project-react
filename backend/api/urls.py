from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()

urlpatterns = (
    path('', include(router.urls)),
    path('users/', include('users.urls')),
    path('recipes/', include('recipes.urls')),
    path('tags/', include('recipes.urls')),
    path('ingredients/', include('recipes.urls')),
    path('auth/', include('djoser.urls.authtoken')),
)
