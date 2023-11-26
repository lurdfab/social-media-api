from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields = ("id", "post", "comment", "commented_at", "comment_image", "commented_by")

class CommentLikesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ['id', 'user',]