import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import DO_NOTHING


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=50, unique=True)
    profile_pic = models.CharField(
        max_length=350, null=True, default='https://res.cloudinary.com/dnvstdsde/image/upload/v1623409738/user_yf5keh.png')
    # attribute author: <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
    background_pic = models.CharField(
        max_length=350, null=True, default='https://res.cloudinary.com/dnvstdsde/image/upload/v1623410114/index_s7iuv2.jpg')
    private = models.BooleanField(default=True)
    dob = models.DateField(null=True)


class Following(models.Model):
    user_id = models.ForeignKey(
        User,
        related_name='following',
        on_delete=DO_NOTHING
    )

    follower_id = models.ForeignKey(
        User,
        related_name='followed_by',
        on_delete=DO_NOTHING
    )
