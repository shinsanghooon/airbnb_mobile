from rest_framework.decorators import api_view
from .models import Room
from .serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# @api_view(["GET", "POST"])
# def room_views(request):
#     if request.method=="GET":
#         rooms = Room.objects.all()[:5]
#         serializer = ReadRoomSerializer(rooms, many=True).data
#         return Response(serializer)
#     elif request.method=="POST":
#         if not requestuser.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serializer = WriteRoomSerializer(data=request.data)
#         print(dir(serializer)) # serializer의 메소드 확인 가능
#         if serializer.is_valid():  # -> false, 내가 전송한 데이터로는 serializers가 invalid 
#             room = serializer.save(user=request.user)
#             room_serializer = ReadRoomSerializer(room).data
#             # serializer -> create, update를 직접 콜하면 안되고 항상 save메소드를 콜해야해 
#             # save 메소드가 -> create, update를 할 지 
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()[:5]
        serializer = RoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        print(dir(serializer)) # serializer의 메소드 확인 가능
        if serializer.is_valid():  # -> false, 내가 전송한 데이터로는 serializers가 invalid 
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            # serializer -> create, update를 직접 콜하면 안되고 항상 save메소드를 콜해야해 
            # save 메소드가 -> create, update를 할 지 
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RoomView(APIView):

    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)        

    def put(self, request, pk):
        room = self.get_room(pk) #room이 업데이트 하고 싶어하는 instance

        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            # serializer가 인스턴스를 가지고 초기화되면 update 
            # 인스턴스가 없는 상태로 초기화되면 create
            # partial=True는 바꾸고 싶은 데이터만 보내는 것이다. 
            if serializer.is_valid():
                room = serializer.save()
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# 많은 것을 커스터마이징 할 필요가 없을 때. 
# class ListRoomsView(ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

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
