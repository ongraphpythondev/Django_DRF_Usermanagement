from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, RegisterSerializer , ChangePasswordSerializer


# Create your views here.

# Register API
class RegisterAPI(GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self , request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save(request.data)
            return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self , username):
        try:
            return User.objects.get(username = username)
        except User.DoesNotExist :
            return None
    
    def patch(self , request):
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
            
        
        

    
    
"""
@api_view(['POST'])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = UserDataSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            u = serializer.save()
            data['response'] = "successfully resgistered a new user."
            data['email'] = u.email
            data['username'] = u.username
            username = request.data.get("username")
            password = request.data.get("password")
            email = request.data.get("email")
            user = User.objects.create_user(username, email=email, password=password)
            user.save()
            login(request , user)        
        else:
            data = serilizer.errors
        
        return Response(data)
       
{
"email":"max@gmail.com",
"username":"max",
"password":"abcd@1234",
"password2":"abcd@1234"
}    
"""