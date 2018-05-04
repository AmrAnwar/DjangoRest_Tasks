from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers import LoginSerializer


class LoginView(APIView):
    """
    ApiView for Login users
    """
    def post(self, request):
        """
        post data :
        {
        'usersname':
        'email':
        'password':
        }
        :param request:
        :return: 2 cases -:
            1- if serializer isn't valid return serializer.errors
            2- if serializer is valid return serializer.data
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data)