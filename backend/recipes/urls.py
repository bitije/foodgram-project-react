from .views import RecipeView, TagView, IngredientView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('', RecipeView, 'recipes')
router.register('', TagView, 'tags')
router.register('', IngredientView, 'ingredients')

urlpatterns = (
    path('', include(router.urls)),
)
