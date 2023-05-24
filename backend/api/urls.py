from django.urls import include, path

app_name = 'api'

urlpatterns = (
    path('', include('recipes.urls')),
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls.authtoken')),
)
