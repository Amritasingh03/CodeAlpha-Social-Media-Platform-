from django.db import models


class Post(models.Model):
    author = models.CharField(max_length=100, default="Community Member")
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.author}: {self.content[:40]}"
