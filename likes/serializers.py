from rest_framework import serializers
from .models import *


class LikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.ReadOnlyField(source="liked_by.username")
    disliked_by = serializers.ReadOnlyField(source="disliked_by.username")

    class Meta:
        model = Like
        fields = ("post", "liked_by", "disliked_by")