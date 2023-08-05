from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User
'''
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

    class Meta :
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if User.objects.filter(username = username).exists():
            user = User.objects.get(username = username)

            if not user.check_password(password):
                raise serializers.ValidationError("wrong password")

        else:
            raise serializers.ValidationError("user accounts not exist")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token) 

        data = {
            'user' : user,
            'refresh_token' : refresh_token,
            'access_token' : access_token
        }  

        return data
        '''