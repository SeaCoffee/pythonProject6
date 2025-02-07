from rest_framework import serializers

from apps.posts.models import PostModel

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
        read_only_fields = ('author', 'created_at', 'updated_at')


class PostPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('photo',)



