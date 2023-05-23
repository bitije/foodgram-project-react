from rest_framework.serializers import ModelSerializer
from .models import Tag, Ingredient, Recipe


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('__all__', )


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('__all__', )


class RecipeSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('__all__', )
