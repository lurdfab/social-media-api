from rest_framework import serializers
from .models import *
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from likes import services
from posts.models import Post
from posts.serializers import PostsLikesSerializer

class RegisterSerializer(serializers.ModelSerializer):
    #reason we do these below even after listing the fields in the class meta is to enforce certain parameters for the fields, we can do without it 
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=20, min_length=5)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True) #we used write only because we don't want it returned back to the server
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'token')

    def validate(self, attrs): #this method is used to validate our emails to avoid an email being used twice

        email_exists = User.objects.filter(email=attrs["email"]).first()
        if email_exists:
            raise ValidationError("Email already exists")
        return super().validate(attrs)
        
    def create(self, validated_data): #this method is used to hash password & generate token during registration.
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
    
        return user
    
    def get_token(self, obj):
        if obj:
            token, created = Token.objects.get_or_create(user=obj)
            return token.key
        return None

    

class LoginSerializer(serializers.ModelSerializer):
    #reason we do these below even after listing the fields in the class meta is to enforce certain parameters for the fields, we can do without it 

    username = serializers.CharField(max_length=20, min_length=5)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True) #we used write only because we don't want it returned back to the server

    class Meta:
        model = User
        fields = ('username', 'password')


class FollowersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username',]
class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    post_likes = serializers.SerializerMethodField() 
    class Meta:
        model = User
        fields = ['id', 'username', 'followers', 'post_likes']



    def get_followers(self, obj):
        followers = services.get_fans(obj)
        return FollowersSerializer(followers, many=True).data
    
    def get_post_likes(self, obj):
        likes = services.get_liked(obj.id, Post)
        return PostsLikesSerializer(likes, many=True).data