from .models import Tag, Ingredient, Recipe, AmountIngredient
from rest_framework.serializers import (ModelSerializer, SerializerMethodField)
from users.serializers import UserSerializer
from django.core.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from django.db.transaction import atomic


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
    # tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time',)

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        return not user.is_anonymous and user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        return not user.is_anonymous and user.carts.filter(recipe=recipe).exists()

    def get_ingredients(self, recipe):
        ingredient_data = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', 'recipe__amount')
        ingredients = [
            {
                'id': data['id'],
                'name': data['name'],
                'measurement_unit': data['measurement_unit'],
                'amount': data['recipe__amount']
            }
            for data in ingredient_data
        ]
        return ingredients

    def validate(self, data):
        data['tags'] = self.initial_data.get('tags')
        data['ingredients'] = self.initial_data.get('ingredients')
        return data

    @atomic
    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        validated_data['author'] = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data)
        for tag_id in tags_data:
            tag = Tag.objects.get(id=tag_id)
            recipe.tags.add(tag)
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            ingredient = Ingredient.objects.get(id=ingredient_id)
            amount = ingredient_data.get('amount')
            AmountIngredient.objects.create(
                recipe=recipe,
                ingredients=ingredient,
                amount=amount
            )
        return recipe

    @atomic
    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe.__dict__.update(**validated_data)
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        if ingredients:
            recipe.ingredients.clear()
            for ingredient_data in ingredients:
                ingredient_id = ingredient_data.get('id')
                ingredient = Ingredient.objects.get(id=ingredient_id)
                amount = ingredient_data.get('amount')
                AmountIngredient.objects.create(
                    recipe=recipe, ingredients=ingredient, amount=amount)
        recipe.save()
        return recipe


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

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
