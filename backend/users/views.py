from rest_framework.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED,
                                   HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT,
                                   HTTP_404_NOT_FOUND)
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from recipes.serializers import SubscriptionSerializer
from djoser.views import UserViewSet
from .pagination import PageLimitPagination
from .models import Subscription
from django.shortcuts import get_object_or_404


User = get_user_model()


class UserView(UserViewSet):
    pagination_class = PageLimitPagination

    def auth_check(self):
        if self.request.user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

    @action(methods=['post', 'delete', ],
            detail=True,
            url_name='subscribe',
            url_path='subscribe')
    def subscribe(self, request, id=None) -> Response:
        self.auth_check()
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            con = Subscription.objects.filter(follower=request.user).filter(
                author=author)
            if con.exists():
                return Response(status=HTTP_400_BAD_REQUEST)
            else:
                Subscription.objects.create(author=author,
                                            follower=request.user)
                data = SubscriptionSerializer(author).data
                return Response(data=data, status=HTTP_200_OK)

        elif request.method == 'DELETE':
            try:
                sub = Subscription.objects.get(author=author,
                                               follower=request.user)
                sub.delete()
                data = SubscriptionSerializer(author).data
                return Response(data=data, status=HTTP_204_NO_CONTENT)
            except Subscription.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)

    @action(["get", ], detail=False)
    def subscriptions(self, request) -> Response:
        self.auth_check()
        pages = self.paginate_queryset(
            User.objects.filter(subscribers__follower=self.request.user)
        )
        serializer = SubscriptionSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)
