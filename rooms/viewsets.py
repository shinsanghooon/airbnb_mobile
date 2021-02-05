from rest_framework import viewsets
from .models import Room
from .serializers import BigRoomSerializer

# url을 사용하지 않게 해준다. 
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer