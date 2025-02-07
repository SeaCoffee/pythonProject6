from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel
from core.services.file_service import upload_post_photo
from apps.posts.managers import PostManager

User = get_user_model()

class PostModel(BaseModel):
    class Meta:
        db_table = 'posts'

    title = models.CharField(max_length=100, blank=False, null=False)
    content = models.TextField(max_length=5000, blank=False, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    photo = models.ImageField(upload_to=upload_post_photo, blank=True, null=True)

    objects = PostManager()