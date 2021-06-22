from django.db.models.fields import CharField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    user = models.ForeignKey(
        'jwt_auth.User',
        related_name='posts',
        on_delete=models.CASCADE
    )
    liked_by = models.ManyToManyField(
        'jwt_auth.User',
        blank=True
    )

    def __str__(self):
        return f'{self.content}'


class Comment(models.Model):
    content = CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Comment {self.id} on {self.post}'


class Attachment(models.Model):
    url = models.CharField(max_length=250)
    post = models.ForeignKey(
        Post,
        related_name='attachments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        on_delete=models.CASCADE
    )
