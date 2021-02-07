from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from users.models import User
import jwt

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # print(request.META)
        try:
            token = request.META.get("HTTP_AUTHORIZATION")
            if token is None:
                return None
            xjwt, jwt_token = token.split(" ")
            print(xjwt, jwt_token)
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded)
            pk = decoded.get("pk")
            user = User.objects.get(pk=pk)
            return (user, None)
        except ValueError:
            return None
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(detail="JWT Format Invalid")
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No Such User")


