from rest_framework import serializers
from .models import Post
from comments.serializers import *

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ("content", "created_at", "post_images", "category", "comments")
