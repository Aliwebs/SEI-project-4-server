
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Attachment, Comment, Post
from .serializers import (
    AttachmentSerializer,
    CommentSerializer,
    PopulatedCommentSerializer,
    PopulatedPostSerializer,
    PostSerializer
)


class PostListView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, _request):
        posts = Post.objects.all().order_by('-created_at')
        serialized_posts = PopulatedPostSerializer(posts, many=True)
        return Response(serialized_posts.data)

    def post(self, request):
        request.data['user'] = request.user.id
        attachments = request.data.pop('attachments')
        serialized_post = PostSerializer(data=request.data)
        if serialized_post.is_valid():
            serialized_post.save()
            postId = serialized_post.data.get('id')
            post = Post.objects.get(pk=postId)
            attachments['owner'] = request.user.id
            attachments['post'] = serialized_post.data.get('id')
            serialized_attachment = AttachmentSerializer(data=attachments)
            if serialized_attachment.is_valid():
                serialized_attachment.save()
            serialized_post_after = PopulatedPostSerializer(post)
            return Response(data=serialized_post_after.data, status=200)
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
        # if post.user != request.user:
        #     raise PermissionDenied()
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


class PostFilterView(APIView):
    def get(self, _request, pk):
        posts = Post.objects.filter(user=pk).order_by('-created_at')
        serialized_posts = PopulatedPostSerializer(posts, many=True)
        return Response(serialized_posts.data)


class CommentListView(APIView):
    def get(self, _request, pk):
        comments = Comment.objects.filter(post=pk)
        serialized_comments = CommentSerializer(comments)
        return Response(serialized_comments.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        request.data['post'] = pk
        request.data['owner'] = request.user.id
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            comment = Comment.objects.get(pk=serialized_comment.data.get('id'))
            serialized_comment = PopulatedCommentSerializer(comment)
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CommentDetailView(APIView):

    def delete(self, request, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
            if comment.owner != request.user:
                raise PermissionDenied()
            comment.delete()
            return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound()
