from django.urls import path
from forum import views

app_name = 'forum'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),  # Главная страница с постами
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'), 
    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('rate/', views.PostRatingView.as_view(), name='post_rating'),
]