from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework  import status, permissions
from rest_framework.request import Request
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
   

    def post(self, request:Request):  
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message":"user created successfully",
                "data":serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST )

   
class LoginViewSet(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]

    
    def post(self, request:Request): 
        username= request.data.get('username')
        password = request.data.get('password')

        user=authenticate(username=username, password=password)

        if user is not None:

            token = Token.objects.create(user=user)
            response = {
                "message": "Login was successful",
                "tokens": token
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "invalid username and password"})

    def get(self, request:Request): 
        content = {
            "user":str(request.user),
            "auth":str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK )
    
class LogoutViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]  #Use the appropriate authentication method
  

    def post(self, request):
        # When a user logs out, you can simply delete their token (or perform other necessary actions).
        request.auth.delete()  # Delete the token
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        follower = self.request.user  # The user performing the follow action
        followee = self.get_object().user  # The user being followed

        if follower == followee:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        profile = self.get_object()
        profile.followers.add(follower)
        profile.save()

        return Response({"detail": f"You are now following {followee.username}."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        follower = self.request.user  # The user performing the unfollow action
        followee = self.get_object().user  # The user being unfollowed

        profile = self.get_object()
        profile.followers.remove(follower)
        profile.save()

        return Response({"detail": f"You have unfollowed {followee.username}."}, status=status.HTTP_200_OK)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    
    