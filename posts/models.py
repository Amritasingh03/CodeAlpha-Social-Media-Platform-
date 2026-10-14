from django.db import models


class Post(models.Model):
    author = models.CharField(max_length=100, default="Community Member")
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.author}: {self.content[:40]}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="user_likes")
    username = models.CharField(max_length=150)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["post", "username"], name="unique_like_per_user_post")]

    def __str__(self):
        return f"{self.username} liked post {self.post_id}"
