from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AdminLoginForm, BlogPostForm
from .models import BlogPost


def portfolio_view(request):
    return render(request, "blog/portfolio.html")


def post_list(request):
    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("admin_post_create")

    form = AdminLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("admin_post_create")

    return render(request, "blog/admin_login.html", {"form": form})


def admin_logout(request):
    logout(request)
    return redirect("admin_login")


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required(login_url="admin_login")
@user_passes_test(is_staff_user, login_url="admin_login")
def admin_post_create(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        messages.success(request, "Blog post published successfully.")
        return redirect("post_detail", pk=post.pk)

    posts = BlogPost.objects.all().order_by("-created_at")
    return render(request, "blog/admin_post_create.html", {"form": form, "posts": posts})


@require_POST
@login_required(login_url="admin_login")
@user_passes_test(is_staff_user, login_url="admin_login")
def admin_post_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.success(request, "Blog post deleted successfully.")
    return redirect("admin_post_create")
