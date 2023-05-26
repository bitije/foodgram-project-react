from django.contrib.auth import get_user_model
from django.db.models import (CASCADE, SET_NULL, CharField,
                              DateTimeField, ForeignKey, ImageField,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField)


User = get_user_model()


class Tag(Model):
    name = CharField(
        max_length=128,
        unique=True,
    )
    color = CharField(
        max_length=7,
        unique=True,
        db_index=False,
    )
    slug = CharField(
        max_length=64,
        unique=True,
        db_index=False,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} ({self.color})'


class Ingredient(Model):
    name = CharField(
        max_length=128,
    )
    measurement_unit = CharField(
        max_length=24,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Recipe(Model):
    name = CharField(
        max_length=128,
    )
    author = ForeignKey(
        related_name='recipes',
        to=User,
        on_delete=SET_NULL,
        null=True,
    )
    tags = ManyToManyField(
        related_name='recipes',
        to='Tag',
    )
    ingredients = ManyToManyField(
        related_name='recipes',
        to=Ingredient,
        through='recipes.AmountIngredient',
    )
    pub_date = DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    image = ImageField(
        upload_to='recipe_images/',
    )
    text = TextField(
        max_length=2048,
    )
    cooking_time = PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self) -> str:
        return f'{self.name}'


class AmountIngredient(Model):
    recipe = ForeignKey(
        related_name='ingredient',
        to=Recipe,
        on_delete=CASCADE,
    )
    ingredients = ForeignKey(
        related_name='recipe',
        to=Ingredient,
        on_delete=CASCADE,
    )
    amount = PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = ('recipe', )

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'


class Favorite(Model):
    recipe = ForeignKey(
        related_name='in_favorites',
        to=Recipe,
        on_delete=CASCADE,
    )
    user = ForeignKey(
        related_name='favorites',
        to=User,
        on_delete=CASCADE,
    )
    date_added = DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('user', )

    def __str__(self) -> str:
        return f'{self.user} : {self.recipe}'


class Cart(Model):
    recipe = ForeignKey(
        related_name='in_carts',
        to=Recipe,
        on_delete=CASCADE,
    )
    user = ForeignKey(
        related_name='carts',
        to=User,
        on_delete=CASCADE,
    )
    date_added = DateTimeField(
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('user', )

    def __str__(self) -> str:
        return f'{self.user} : {self.recipe}'
