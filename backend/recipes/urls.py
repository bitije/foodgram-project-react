from .views import RecipeView, TagView, IngredientView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'recipes'

router = DefaultRouter()
router.register(r'recipes', RecipeView)
router.register(r'tags', TagView)
router.register(r'ingredients', IngredientView)

urlpatterns = (
    path('', include(router.urls)),
)
