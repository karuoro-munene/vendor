from django.contrib.auth import login, logout, user_logged_out
from django.contrib.sites.shortcuts import get_current_site
from knox.auth import TokenAuthentication
from knox.views import LoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from machine.models import User
from machine.serializers import CreateUserSerializer

current_format = None


# Create your views here.
class APIRoot(APIView):
    """
    Vending Machine API Root
    """

    def get(self, request):
        current_site = get_current_site(request)
        if current_site.name == 'localhost':
            ext = ''
        else:
            ext = 's'
        data = {
            "Auth Endpoints": [
                {
                    "Users' Registration": f"http{ext}://{current_site}/users",
                    "Users' Login": f"http{ext}://{current_site}/login",
                    "Users' Logout": f"http{ext}://{current_site}/logout",
                    "Users' Logout All": f"http{ext}://{current_site}/logout/all",
                }
            ]
        }
        return Response(data)


class UserCreateView(generics.CreateAPIView):
    """
    Make a POST request with email, username, role, and password.
    :param request: {"email":"foo@bar.com", "username":"FooBar","password":"@#pa55w0rd", "role":"Buyer"}
    :return: a success message if user is created. Error, if data invalid.
    """
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class UserLoginView(LoginView):
    """
    an example post is ```{"username":"usr@user.com","password":"@#pa55w0rd"}```
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer

    def post(self, request, format=current_format):
        try:
            username = request.data["username"]
            password = request.data["password"]
            if User.objects.filter(username=username).exists():
                login_data = {
                    "username": username,
                    "password": password
                }
                # pass the data to Knox Auth to generate token
                serializer = AuthTokenSerializer(data=login_data)
                serializer.is_valid(raise_exception=True)
                account = serializer.validated_data["user"]
                login(request, account)
                json = super(UserLoginView, self).post(request, format=current_format)
                token = json.data["token"]

                return Response(
                    json.data,
                    status=status.HTTP_201_CREATED,
                    headers={"Authorization": "Token {0}".format(token)},
                )
            else:
                return Response(
                    {"error": "That account doesn't exist in our database"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            print("error is:", e.__str__())
            raise ValidationError(e.__str__(), code='authorization')


class LogoutView(APIView):
    """
    Log the user out of current session
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=current_format):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class LogoutAllView(APIView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=current_format):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST", "PUT", "DELETE"])
def product(request):
    return Response()
