from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .pagination import PageLimitPagination
from .models import Tag, Ingredient, Recipe, Favorite, Cart
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer)
from django.db.models import F, Sum
from rest_framework.status import HTTP_401_UNAUTHORIZED
from .permissions import AuthorOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend


class TagView(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientView(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeView(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', ]
    filter_class = RecipeFilter

    def auth_check(self):
        if self.request.user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.query_params.getlist('tags')
        author = self.request.query_params.get('author')
        is_favorited = self.request.query_params.get('is_favorited', '0')
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart', '0')

        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if author:
            queryset = queryset.filter(author=author)

        if not self.request.user.is_anonymous:
            is_favorited = is_favorited == '1'
            is_in_shopping_cart = is_in_shopping_cart == '1'

            if is_favorited:
                queryset = queryset.filter(in_favorites__user=self.request.user)
            if is_in_shopping_cart:
                queryset = queryset.filter(in_carts__user=self.request.user)

        return queryset

    @action(
        methods=['post', 'delete', ],
        detail=True,
        url_name='favorite',
        url_path='favorite'
            )
    def favorite(self, request, pk=None):
        self.auth_check()
        fav_recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            return self.favorite_post(request, fav_recipe)
        elif request.method == 'DELETE':
            return self.favorite_delete(request=request, fav_recipe=fav_recipe)

    @action(
        methods=['post', 'delete', ],
        detail=True,
        url_name='shopping_cart',
        url_path='shopping_cart'
    )
    def shopping_cart(self, request, pk=None):
        self.auth_check()
        to_buy = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            return self.shopping_post(request, to_buy)
        elif request.method == 'DELETE':
            return self.shopping_delete(request=request, to_buy=to_buy)

    @action(
        methods=['get', ],
        detail=False,
        url_name='download_shopping_cart',
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        ingredients = Ingredient.objects.filter(
            recipe__recipe__in_carts__user=request.user
        ).values(
            'name',
            measurement=F('measurement_unit')
        ).annotate(amount=Sum('recipe__amount'))
        lines = [f"{ingredients}\n" for obj in ingredients]
        response = HttpResponse(lines, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="to_buy.txt"'
        return response

    def shopping_post(self, request, to_buy):
        con = Cart.objects.filter(user=request.user).filter(
            recipe=to_buy)
        if con.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            Cart.objects.create(recipe=to_buy, user=request.user)
            serializer = ShortRecipeSerializer(to_buy, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def shopping_delete(self, request, to_buy):
        try:
            recipe_del = Cart.objects.get(recipe=to_buy, user=request.user)
            recipe_del.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def favorite_post(self, request, fav_recipe):
        con = Favorite.objects.filter(user=request.user).filter(
            recipe=fav_recipe)
        if con.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            Favorite.objects.create(recipe=fav_recipe, user=request.user)
            serializer = ShortRecipeSerializer(fav_recipe, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def favorite_delete(self, request, fav_recipe):
        try:
            recipe_del = Favorite.objects.get(recipe=fav_recipe,
                                              user=request.user)
            recipe_del.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
