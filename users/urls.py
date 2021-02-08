from django.urls import path
from . import  views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register("", views.UserViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     path("", views.UsersView.as_view()),
#     path("token/", views.login),
#     path("me/", views.MeView.as_view()),
#     path("me/favs/", views.FavsView.as_view()),
#     path("<int:pk>/", views.user_detail),
# ]
