from rest_framework import serializers
from .models import Blog
from apps.users.serializers import UserSerializer

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Blog
        fields = ('blog_id', 'title', 'blog_content', 'author', 'created_at', 'updated_at', 'published')
        read_only_fields = ('blog_id', 'author', 'created_at', 'updated_at')
