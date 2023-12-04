from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields=['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        email = attrs.get('email')
        if not email:
            email = ''
        if not username.isalnum() or not password.isalnum():
            raise serializers.ValidationError('Both username and password should only contain alphanumeric characters only')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields=['username', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = User.objects.filter(username=username)

        if not user.exists():
            raise AuthenticationFailed('This user does not exist, please try again!')
        if not user[0].is_verified:
            raise AuthenticationFailed('Your account is not verified. Check your email to verify your account')
        if not user[0].is_active:
            raise AuthenticationFailed('Your account is disabled. Contact an Admin at zarea.project.noreply@gmail.com')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, please try again!')
        return {
            'username': user.username,
            'tokens': user.tokens(),
        }



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')