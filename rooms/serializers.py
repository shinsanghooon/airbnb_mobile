
from rest_framework import serializers
from users.serializers import TinyUserSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):

    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = ["pk", "name", "price", "instant_book", "user"]


# 정말 귀찮다 
# class RoomSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=140)
#     price = serializers.IntegerField()
#     bedrooms = serializers.IntegerField()
#     instant_book = serializers.BooleanField()


class BigRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ()