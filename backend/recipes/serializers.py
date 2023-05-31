from .models import Tag, Ingredient, Recipe
from rest_framework.serializers import (ModelSerializer, SerializerMethodField)
from users.serializers import UserSerializer
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model


User = get_user_model()


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeSerializer(ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe: Recipe) -> bool:
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe: Recipe) -> bool:
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return user.carts.filter(recipe=recipe).exists()

    def get_ingredients(self, recipe: Recipe):
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )
        return ingredients


class ShortRecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj) -> bool:
        return True

    def get_recipes_count(self, obj) -> int:
        return obj.recipes.count()
