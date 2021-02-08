from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User 
from .serializers import UserSerializer
from rooms.serializers import RoomSerializer
from rooms.models import Room
import jwt
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsSelf


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        print(self.action)
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create' or self.action=='retrieve': #retrieve는 user하나만 보는거
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]   
    
    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            # jwt에는 식별이 가능한 최소 정보만 포함한다. 예를 들면 pk 같은거
            # jwt를 쓰는 이유는 누구도 우리 토큰을 건드리지 않았는지 확인 하기 위함
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True) 
    # detail=True 이 메소드가 /users/에선 유효하지 않지만 user, id 같이 있을 땐 유효
    # 이 때는 ViewSet이 자동으로 너한테 여기 이 user/id/ id를 argument로 보내줌
    # 그래서 pk를 적어줘야해
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    @favs.mapping.put  #favs.mapping.post, #fav.mapping.delete 다 가능 
    # favs.action이 detail=True이면 mapping도 true
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None) # pk or None 
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(UserSerializer(request.user).data)
    
#     def put(self, request):
#         serializer = UserSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response()
#         else:
#             return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)

    
# class FavsView(APIView):
#     permission_classes = [IsAuthenticated]

#     # post? put? 여기선 업데이트 상황이기 때문에 put
#     def put(self, request):
#         pk = request.data.get("pk", None) # pk or None 
#         user = request.user
#         if pk is not None:
#             try:
#                 room = Room.objects.get(pk=pk)
#                 if room in user.favs.all():
#                     user.favs.remove(room)
#                 else:
#                     user.favs.add(room)
#                 return Response()
#             except Room.DoesNotExist:
#                 pass
        
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def user_detail(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#         return Response(UserSerializer(user).data)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)




# 로그인 할 때 username, password 맞을 때는 JWT를 encode한다. 
# 토큰에는 pk만 들어있다. 헤더에 있는 토큰을 이용해 인증을 할 수 있음 
# HTTP_AUTHORUZATION 값을 받아온다. 토큰을 헤더로부터 받아서 
# 토큰으 파트를 split 한다. 두번째 파트가 실제 토큰이고 
# 토큰을 decode하는데 decode 과정을 통해서 pk를 알 수 있고 user를 return 해준다.