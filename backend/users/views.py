from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from .pagination import PageLimitPagination
from ..recipes.models import Ingredient
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

User = get_user_model()


class UserView(UserViewSet):
    pagination_class = PageLimitPagination
    permission_classes = (DjangoModelPermissions,)


class IngredientView(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
