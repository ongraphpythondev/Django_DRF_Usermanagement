from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication , SessionAuthentication

from .serializers import UserSerializer, RegisterSerializer , LoginSerializer , ChangePasswordSerializer


# Create your views here.

# Register API
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [SessionAuthentication]
    
    @csrf_exempt    
    def post(self , request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request , user)
            return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

            
# Login API
class Login(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = [SessionAuthentication]
    
    def get_object(self , username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist :
            return None
    
    @csrf_exempt    
    def post(self , request):
        user = self.get_object(request.data.get("username"))
        if not user :
            return Response({'Not Found' : 'User does not exist'} , status = status.HTTP_400_BAD_REQUEST)
        login(request , user)
        return Response({'Logged in' : 'User Logged in Successfully. '})

# Logout API
class Logout(GenericAPIView):
    serializer_class = LoginSerializer       
    authentication_classes = [SessionAuthentication]
    
    def get(self , request):
        logout(request)
        return Response({'Logging out' : 'User Logged out Successfully. '})

# Reset Password API
class ResetPasswordAPI(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get_object(self , username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist :
            return None
    @csrf_exempt        
    def put(self , request):
        if request.user.username == request.data.get("username") :
            user = self.get_object(request.data.get("username"))
            if not user :
                return Response({'Not Found' : 'User does not exist'} , status = status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(user , data = request.data , partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Invalid Username" : "For changing password logged in username should be use."})


class ChangePasswordAPI(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get_object(self , username ):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist :
            return None
    
    @csrf_exempt    
    def put(self , request):
        if request.user.username == request.data.get("username") :
            user = self.get_object(request.data.get("username"))
            if not user :
                return Response({'Not Found' : 'User does not exist'} , status = status.HTTP_400_BAD_REQUEST)
            user.set_password(make_password(request.data.get("new_password")))
            serializer = self.get_serializer(user , data = request.data , partial = True)
            if serializer.is_valid():
                user = serializer.save()
                return Response({"user": UserSerializer(user).data})
            return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Invalid Username" : "For changing password logged in username should be use."})






