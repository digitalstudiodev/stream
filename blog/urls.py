from django.urls import path, include
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, TagPostListView, services, main, resume)

app_name = 'blog'

urlpatterns = [
    path('services/', services, name='services'),
    path('', main, name='main'),
    path('resume/', resume, name='resume'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('content/', PostListView.as_view(), name='content'),
    path('posts/<str:tag>/', TagPostListView.as_view(), name='posts-by-tag'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]