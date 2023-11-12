from rest_framework import serializers
from .models import *

class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Comment
        fields = ("post", "comment", "commented_at", "comment_image", "commented_by")