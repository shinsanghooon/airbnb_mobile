from rest_framework.decorators import api_view
from .models import Room
from .serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status


class OwnPagination(PageNumberPagination):
    page_size = 20

class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True, context={"request": request})

        # 이렇게 해주면 count, next, prev 을 볼 수 있음
        return paginator.get_paginated_response(serializer.data)

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


@api_view(["GET"])
def room_search(request):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None) 
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)

    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    
    loc_range = 0.005
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - loc_range
        filter_kwargs["lat__lte"] = float(lat) + loc_range
        filter_kwargs["lng__gte"] = float(lng) - loc_range
        filter_kwargs["lng__lte"] = float(lng) + loc_range
    
    try:
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = Room.objects.all()

    paginator = OwnPagination()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)