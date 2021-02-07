from rest_framework import viewsets
from .models import Room
from .serializers import RoomSerializer

# url을 사용하지 않게 해준다. 
# 모든 기능을 제공해준다. 
# 하지만 너무 많이 공개되어잇고, 대부분의 기능엔 로직이 들어가기 때문에 대단하지만 ... 
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer