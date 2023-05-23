from django.contrib.admin import ModelAdmin, register, TabularInline
from .models import Cart, Favorite, Ingredient, Recipe, Tag, AmountIngredient


class AmountIngredientInline(TabularInline):
    model = AmountIngredient
    extra = 2


@register(AmountIngredient)
class AmountIngredient(ModelAdmin):
    pass


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    save_on_top = True


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author',)
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    raw_id_fields = ('author',)
    inlines = (AmountIngredientInline,)
    search_fields = ('name', 'author__username', 'tags__name',)
    list_filter = ('name', 'author__username', 'tags__name')
    save_on_top = True


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'color')
    save_on_top = True


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe', 'date_added')
    search_fields = ('user__username', 'recipe__name')


@register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'recipe', 'date_added')
    search_fields = ('user__username', 'recipe__name')
