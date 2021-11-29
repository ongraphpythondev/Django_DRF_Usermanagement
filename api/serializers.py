from rest_framework import serializers

from .models import UserData

from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'email']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username' , 'email' , 'password']
    
    def save(self , validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        
        return user

class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'password']

"""
class UserDataSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style = {'input_type' : 'password'} , write_only = True)

    class Meta:
        model = UserData
        fields = ['email' , 'username' ,  'password' , 'password2']
        extra_kwargs = {
        'password' : {'write_only' : True}
        }
    
    def save(self):
        data = UserData(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
            password = self.validated_data['password']
        )
        password = self.validated_data['password'],
        password2 = self.validated_data['password2'],
        
        if password != password2:
            raise serializers.validationError({'password' : 'Passwords must match.'})
        data.save()
        return data
"""


