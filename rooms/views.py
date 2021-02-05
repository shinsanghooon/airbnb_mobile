from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer, BigRoomSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView


# 많은 것을 커스터마이징 할 필요가 없을 때. 
class ListRoomsView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# Create your views here.
# @api_view(['GET', 'DELETE'])
# def list_rooms(request):
#     rooms = Room.objects.all()
#     serialized_rooms = RoomSerializer(rooms, many=True)
#     return Response(data=serialized_rooms.data)

# apiview 가장 일반적인 view
# class ListRoomsView(APIView):
#     def get(self, request):
#         rooms = Room.objects.all()
#         serializer = RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         pass

class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer
    pass
