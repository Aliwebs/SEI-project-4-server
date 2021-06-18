from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Post
from .serializers import PopulatedPostSerializer, PostSerializer


class PostListView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, _request):
        posts = Post.objects.all().order_by('-created_at')
        serialized_posts = PopulatedPostSerializer(posts, many=True)
        return Response(serialized_posts.data)

    def post(self, request):
        request.data['user'] = request.user.id
        serialized_post = PostSerializer(data=request.data)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response(data=serialized_post.data, status=200)
        return Response(data=serialized_post.errors, status=422)


class PostDetailView(APIView):

    permission_classes = (IsAuthenticated,)

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        post = self.get_post(pk)
        serialized_post = PopulatedPostSerializer(post)
        return Response(serialized_post.data)

    def put(self, request, pk):
        post = self.get_post(pk)
        if post.user != request.user:
            raise PermissionDenied()
        request.data['user'] = request.user.id
        serialized_post = PostSerializer(post, data=request.data)
        if serialized_post.is_valid():
            serialized_post.save()
            return Response(data=serialized_post.data, status=200)
        return Response(data=serialized_post.errors, status=422)

    def delete(self, request, pk):
        post = self.get_post(pk)
        if post.user != request.user:
            raise PermissionDenied()
        post.delete()
        return Response(data={'message': 'Success'}, status=status.HTTP_204_NO_CONTENT)
