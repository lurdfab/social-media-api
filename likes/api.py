from rest_framework import viewsets, status, permissions
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *
from .permissions import *
from posts.models import *
from rest_framework import serializers, viewsets, permissions
from rest_framework.generics import get_object_or_404
from .serializers import LikeSerializer
from .permissions import hasSelfVotedOrReadOnly  # Assuming you have defined this permission

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated, hasSelfVotedOrReadOnly]

    def perform_create(self, serializer):
        try:
            post_instance = get_object_or_404(Post, pk=self.request.data['post'])
        except Post.DoesNotExist:
            raise serializers.ValidationError({"message": "The specified post does not exist"})

        if self.request.data.get('liked_by', None):
            already_liked = Like.objects.filter(post=post_instance, liked_by=self.request.user).exists()
            if already_liked:
                raise serializers.ValidationError({"message": "You have liked this post before"})
            else:
                serializer.save(liked_by=self.request.user, post=post_instance)

        else:
            already_disliked = Like.objects.filter(post=post_instance, disliked_by=self.request.user).exists()
            if already_disliked:
                raise serializers.ValidationError({"message": "You have disliked this post before"})
            else:
                serializer.save(disliked_by=self.request.user, post=post_instance)





        