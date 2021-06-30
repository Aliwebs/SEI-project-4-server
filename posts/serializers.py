from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Attachment, Post, Comment

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_pic')


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'


class PopulatedAttachmentSerializer(AttachmentSerializer):
    owner = UserSerializer()


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class PopulatedCommentSerializer(CommentSerializer):
    owner = UserSerializer()


class PopulatedPostSerializer(PostSerializer):
    user = UserSerializer()
    comments = PopulatedCommentSerializer(many=True)
    attachments = PopulatedAttachmentSerializer(many=True)
