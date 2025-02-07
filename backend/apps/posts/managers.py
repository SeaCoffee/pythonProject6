from django.db import models

class PostQuerySet(models.QuerySet):
    def by_author(self, user):
        return self.filter(author=user)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model)

    def author_posts(self, user):
        return self.get_queryset().by_author(user)
