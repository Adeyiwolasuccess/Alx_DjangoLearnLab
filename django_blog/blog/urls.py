# blog/urls.py
from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)


urlpatterns = [
    # Functional views
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Post CRUD views
    path('posts/', PostListView.as_view(), name='posts'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
