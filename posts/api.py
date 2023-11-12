from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import viewsets, permissions, status
from user.permissions import *


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




