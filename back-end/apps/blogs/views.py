from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Blog
from .serializers import BlogSerializer
from apps.core.permissions import admin_or_user_required, user_required, admin_required

@api_view(['POST'])
@admin_or_user_required
async def create_blog(request):
    """
    Create a new blog post.
    
    Authentication required: Yes (Admin or User)
    
    Request body:
    - title (string): required
    - blog_content (string): required
    - published (boolean): optional, defaults to false
    
    Returns:
    - Complete blog object with author details
    """
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        blog = await serializer.save(author=request.user)
        return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
async def list_blogs(request):
    blogs = await Blog.objects.filter(published=True).select_related('author').all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@user_required
async def get_blog(request, blog_id):
    try:
        blog = await Blog.objects.select_related('author').get(blog_id=blog_id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
@admin_required
async def update_blog(request, blog_id):
    try:
        blog = await Blog.objects.get(blog_id=blog_id)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            updated_blog = await serializer.save()
            return Response(BlogSerializer(updated_blog).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@admin_required
async def delete_blog(request, blog_id):
    try:
        blog = await Blog.objects.get(blog_id=blog_id)
        await blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Blog.DoesNotExist:
        return Response({'error': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
