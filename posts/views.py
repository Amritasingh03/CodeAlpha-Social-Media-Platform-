from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import models, transaction
from .models import Post, Like
from comments.models import Comment


def home(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        content = request.POST.get("content", "").strip()
        if content:
            Post.objects.create(author=request.user.username, content=content)
        return redirect("home")
    posts = Post.objects.order_by("-created_at")
    return render(request, "posts/home.html", {"posts": posts})


@login_required(login_url="login")
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    with transaction.atomic():
        _, created = Like.objects.get_or_create(post=post, username=request.user.username)
        if created:
            Post.objects.filter(id=post.id).update(likes=models.F("likes") + 1)
    return redirect("home")


@login_required(login_url="login")
@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user.username:
        return redirect("home")
    post.delete()
    return redirect("home")


@login_required(login_url="login")
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()
    if content:
        Comment.objects.create(post=post, author=request.user.username, content=content)
    return redirect("home")
