from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from djoser.views import UserViewSet
from .pagination import PageLimitPagination
from .models import Subscription
from django.shortcuts import get_object_or_404


User = get_user_model()


class UserView(UserViewSet):
    pagination_class = PageLimitPagination

    @action(["get", ], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['post', 'delete', ],
            detail=True,
            url_name='subscribe',
            url_path='subscribe')
    def subscribe(self, request, id=None) -> Response:
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        author = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            con = Subscription.objects.filter(follower=request.user).filter(
                author=author)
            if con.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                Subscription.objects.create(author=author,
                                            follower=request.user)
                data = User.objects.get(pk=id)
                return Response(data=UserSerializer(data).data,
                                status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            try:
                sub = Subscription.objects.get(author=author,
                                               follower=request.user)
                sub.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Subscription.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    @action(["get", ], detail=False)
    def subscriptions(self, request) -> Response:
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = User.objects.filter(subscribers__follower=request.user)
        return Response(data=UserSerializer(data, many=True).data,
                        status=status.HTTP_200_OK)
