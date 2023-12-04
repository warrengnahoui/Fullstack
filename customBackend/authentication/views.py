from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from .renderers import UserRenderer
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    LogoutSerializer
)



# Create your views here.


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    #permission_classes=(permissions.IsAuthenticated,)
    renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)