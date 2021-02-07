from rest_framework import serializers
from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "email",
            "avatar",
            "superhost"
        ]

class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        exclude = (
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
        )

class WriteUserSerializer(serializers.ModelSerializer):
    # ModelSerializer를 쓰면 Room Serializer에서 했던 것처럼 다 안해도됨
    # view는 custome이 필요한 경우가 많지만 serializer에서는 자동이 좋음
    class Meta:
        model = User
        fields = [
            "username", 
            "first_name", 
            "last_name", 
            "email"
        ]

    def validate_frist_name(self, value):
        print(value)
        return value.upper()