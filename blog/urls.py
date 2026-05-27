from django.urls import path
from . import views

urlpatterns = [
    path("", views.portfolio_view, name="portfolio"),
    path("blog/", views.post_list, name="post_list"),
    path("blog/post/<int:pk>/", views.post_detail, name="post_detail"),
    path("adminpage/", views.admin_login, name="admin_login"),
    path("adminpage/logout/", views.admin_logout, name="admin_logout"),
    path("adminpage/posts/new/", views.admin_post_create, name="admin_post_create"),
    path("adminpage/posts/<int:pk>/delete/", views.admin_post_delete, name="admin_post_delete"),
]
