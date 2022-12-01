from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework.views import APIView


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
