from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post
from comments.models import Comment


def home(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        author = request.POST.get("author", "Community Member").strip()

        if content:
            Post.objects.create(
                author=author or "Community Member",
                content=content
            )

        return redirect("home")

    posts = Post.objects.order_by("-created_at")
    return render(request, "posts/home.html", {"posts": posts})


@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save(update_fields=["likes"])
    return redirect("home")


@require_POST
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect("home")


@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()
    author = request.POST.get("author", "Community Member").strip()
    if content:
        Comment.objects.create(post=post, author=author or "Community Member", content=content)
    return redirect("home")


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
