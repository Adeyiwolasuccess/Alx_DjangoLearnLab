# blog/urls.py
from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostByTagListView,
)

urlpatterns = [
    # Functional views
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Post CRUD views
    path('posts/', PostListView.as_view(), name='posts'),  # list view stays plural
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # detail view stays plural
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # Comment
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='add-comment'),
    path('posts/<int:pk>/comment/', views.comment_new, name='comment_new'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='edit-comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),

    # Search
    path('search/', views.search_view, name='search'),
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),

    # Tag filtering
    
    # 🔥 Tag filter
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts_by_tag"),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
