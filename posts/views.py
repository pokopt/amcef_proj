from django.shortcuts import render

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer, PostUpdateSerializer
import requests
from drf_yasg.utils import swagger_auto_schema

class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Check if the post exists in the local database
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            # If the post doesn't exist, fetch it from the external API
            response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{pk}')
            if response.status_code == 200:
                post_data = response.json()
                # Create and save the post in the local database
                post = Post.objects.create(**post_data)
                serializer = PostSerializer(post)
                return Response(serializer.data)
            # If the post is not found in the external API, return a 404 error
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], url_path=r'by_user/(?P<userId>\d+)')
    def by_user(self, request, userId=None):
        posts = Post.objects.filter(userId=userId)
        if not posts:
            response = requests.get(f'https://jsonplaceholder.typicode.com/posts?userId={userId}')
            if response.status_code == 200:
                posts_data = response.json()
                for post_data in posts_data:
                    Post.objects.create(**post_data)
                posts = Post.objects.filter(userId=userId)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=PostSerializer,
        responses={201: PostSerializer}
    )
    def create(self, request):
        userId = request.data.get('userId')
        response = requests.get(f'https://jsonplaceholder.typicode.com/users/{userId}')
        if response.status_code != 200:
            return Response({'error': 'Invalid userId'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=PostUpdateSerializer,
        responses={200: PostSerializer}
    )
    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)