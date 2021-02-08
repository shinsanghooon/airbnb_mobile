from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Room
from .serializers import RoomSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework import status
from .permissions import IsOwner

class OwnPagination(PageNumberPagination):
    page_size = 20


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        # get /rooms or get/room/1
        if self.action == "list" or self.action =="retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]


    @action(detail=False)
    def search(self, request):
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