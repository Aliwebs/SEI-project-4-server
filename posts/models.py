from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    user = models.ForeignKey(
        'jwt_auth.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.title}'


class Like(models.Model):
    user = models.ForeignKey(
        'jwt_auth.User',
        related_name='likes',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE
    )
