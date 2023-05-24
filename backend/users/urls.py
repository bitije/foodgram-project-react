from .views import UserView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'users'

router = DefaultRouter()
router.register('', UserView)

urlpatterns = (
    path('', include(router.urls)),
)
