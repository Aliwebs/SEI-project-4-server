from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    date = models.DateField()
    user_id = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=CASCADE
    )


class Like(models.Model):
    user_id = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=CASCADE
    )
    post_id = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=CASCADE
    )
