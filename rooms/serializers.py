from django.utils.timezone import now
from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room

class RoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer(read_only=True)
    is_fav = serializers.SerializerMethodField()
    # years_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ["modified",]
        # room을 get하거나 update할 때 user를 validate 하지 말라고 알려줘야함.
        read_only_fields = ["user", "id", "created", "updated"]

    def validate(self, data):
        if self.instance: # update 
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else: # create
            checkin = data.get('check_in')
            check_out = data.get('check_out')
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
    
    def get_is_fav(self, obj):
        request = self.context.get("request")
        # print(request.user)
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False
    
    def create(self, validated_data):
        request = self.context.get('request')
        room = Room.objects.create(**validated_data, user=request.user)
        return room

    # def get_years_since_joined(self, obj):
    #     return round((now() - obj.created).days/365,1)

    # 유저들이 전송할 수 있는 것들 
    # name = serializers.CharField(max_length=140)
    # address = serializers.CharField(max_length=140)
    # price = serializers.IntegerField(help_text="USD per night")
    # beds = serializers.IntegerField(default=1)
    # lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    # lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    # bedrooms = serializers.IntegerField(default=1)
    # bathrooms = serializers.IntegerField(default=1)
    # check_in = serializers.TimeField(default="00:00:00")
    # check_out = serializers.TimeField(default="00:00:00")
    # instant_book = serializers.BooleanField(default=False)

    # def create(self, validated_data):
    #     return Room.objects.create(**validated_data)

    # def validate_beds(self, beds):
    #     if beds < 5:
    #         raise serializers.ValidationError("Your house is too small")
    #     else:
    #         return beds;
    


        # if not self.instance: #instance가 있으면 create instance가 없으면 update   
        #     checkin = data.get('check_in')
        #     check_out = data.get('check_out')
        #     if check_in == check_out:
        #         raise serializer.ValidationError('Not enough time between changes')
        #     else:
        #         return data
                
    # def update(self, instance, validated_data):
    #     # instance 때문에 장고가 create인지 update 인지 안다. 
    #     print(instance, validated_data)
    #     # validated_data에서 값을 가져오고, 없으면 instance.name 값으로 세팅한다
    #     # 여기서 instance는 serializer에 넘겨준 instance 
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.address = validated_data.get("address", instance.address)
    #     instance.price = validated_data.get("price", instance.price)
    #     instance.beds = validated_data.get("beds", instance.beds)
    #     instance.lat = validated_data.get("lat", instance.lat)
    #     instance.lng = validated_data.get("lng", instance.lng)
    #     instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
    #     instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
    #     instance.check_in = validated_data.get("check_in", instance.check_in)
    #     instance.check_out = validated_data.get("check_out", instance.check_out)
    #     instance.instant_book = validated_data.get("instant_book", instance.instant_book)

    #     instance.save()
    #     return instance


# 정말 귀찮다 
# class RoomSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=140)
#     price = serializers.IntegerField()
#     bedrooms = serializers.IntegerField()
#     instant_book = serializers.BooleanField()


