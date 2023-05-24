from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .pagination import PageLimitPagination
from .models import Tag, Ingredient, Recipe, Favorite, Cart
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from django.db.models import F, Sum
from .permissions import AdminOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


class TagView(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientView(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)


class RecipeView(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageLimitPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['author', 'tags', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_favorited == '1':
            queryset = queryset.filter(in_favorites__user=self.request.user)
        if is_in_shopping_cart == '1':
            queryset = queryset.filter(in_carts__user=self.request.user)
        return queryset

    @action(
        methods=['post', 'delete', ],
        detail=True,
        url_name='favorite',
        url_path='favorite'
            )
    def favorite(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        fav_recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            con = Favorite.objects.filter(user=request.user).filter(
                recipe=fav_recipe)
            if con.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                Favorite.objects.create(recipe=fav_recipe, user=request.user)
                data = Recipe.objects.get(pk=pk)
                return Response(data=RecipeSerializer(data).data,
                                status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            try:
                recipe_del = Favorite.objects.get(recipe=fav_recipe,
                                                  user=request.user)
                recipe_del.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Recipe.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=['post', 'delete', ],
        detail=True,
        url_name='shopping_cart',
        url_path='shopping_cart'
    )
    def shopping_cart(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        to_buy = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            con = Cart.objects.filter(user=request.user).filter(
                recipe=to_buy)
            if con.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                Cart.objects.create(recipe=to_buy, user=request.user)
                data = Recipe.objects.get(pk=pk)
                return Response(data=RecipeSerializer(data).data,
                                status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            try:
                recipe_del = Cart.objects.get(recipe=to_buy,
                                              user=request.user)
                recipe_del.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Recipe.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

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
