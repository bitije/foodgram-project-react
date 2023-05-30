from django.contrib.auth import get_user_model
from rest_framework.serializers import (ModelSerializer, SerializerMethodField)


User = get_user_model()


class UserSerializer(ModelSerializer):

    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'is_subscribed',
            'first_name',
            'last_name',
        )

    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get('request').user

        if user.is_anonymous or (user == obj):
            return False

        return user.subscriptions.filter(author=obj).exists()
