from django.urls import path
from . import views
from . import viewsets 
from rest_framework.routers import DefaultRouter

app_name = "rooms"

router = DefaultRouter()
router.register("", viewsets.RoomViewSet, basename="room")

urlpatterns = [
    # path("list/", views.ListRoomsView.as_view()),
    # path("<int:pk>/", views.SeeRoomView.as_view()),
]

urlpatterns = router.urls