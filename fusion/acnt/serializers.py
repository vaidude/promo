from rest_framework import serializers
from .models import User, Freelancer, Client
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError




class ClientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    password2 = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','password2',]

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError('passwords do not match ')
            
        return attrs
    
    def create(self, validated_data):

        validated_data['is_client'] = True


        # Create a new user
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password = validated_data.get('password'),
            is_client = True
        )

        if validated_data['is_client']:
            client_data = {'user': user}
            client = Client.objects.create(**client_data)


        return user





class FreelancerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    password2 = serializers.CharField(max_length = 68, min_length = 6, write_only = True)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError('passwords do not match ')
            
        return attrs
    
    def create(self, validated_data):
        validated_data['is_freelancer'] = True


        # Create a new user
        user = User.objects.create_user(

            email=validated_data['email'],
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password=validated_data.get('password'),
            is_freelancer = True 
        )

        if validated_data['is_freelancer']:
            # If the user is a freelancer, create a freelance profile
            freelancer_data = {'user': user}
            freelancer = Freelancer.objects.create(**freelancer_data)



        return user


class ClientLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255, min_length = 6)
    password = serializers.CharField(max_length = 68, write_only = True)
    full_name = serializers.CharField(max_length = 255, read_only = True)
    access_token = serializers.CharField(max_length = 255, read_only = True)
    refresh_token = serializers.CharField(max_length = 255, read_only = True)
    
    class Meta:
        model = User
        fields = ['email','password','full_name','access_token','refresh_token']
        
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email = email, password = password)
        
        if not user:
            raise AuthenticationFailed("Invalid credintials try again")
        user_tokens = user.tokens()
            
        return {
            'email' : user.email,
            'full_name' : user.get_full_name,
            'access_token' : user_tokens.get('access'),
            'refresh_token' : user_tokens.get('refresh')
        }


class FreelancerLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255, min_length = 6)
    password = serializers.CharField(max_length = 68, write_only = True)
    full_name = serializers.CharField(max_length = 255, read_only = True)
    access_token = serializers.CharField(max_length = 255, read_only = True)
    refresh_token = serializers.CharField(max_length = 255, read_only = True)
    user_type = serializers.CharField(max_length=20, read_only=True)
    
    class Meta:
        model = User
        fields = ['email','password','full_name','access_token','refresh_token','user_type']
        
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email = email, password = password)

        if not user or not hasattr(user, 'freelancer'):
            raise AuthenticationFailed('Invalid credentials. Please try again.')
        
        user_tokens = user.tokens()
            
        return {
            'email' : user.email,
            'full_name' : user.get_full_name,
            'access_token' : user_tokens.get('access'),
            'refresh_token' : user_tokens.get('refresh'),
            'user_type': 'freelancer',

        }