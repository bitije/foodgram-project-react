from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


User = get_user_model()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            # 'is_subscribed',
            'first_name',
            'last_name',
        )
