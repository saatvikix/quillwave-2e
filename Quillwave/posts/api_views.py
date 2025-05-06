from rest_framework import generics
from posts.models import Post
from posts.serializers import PostSerializer

class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_draft=False).order_by('-created_at')
    serializer_class = PostSerializer

class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
