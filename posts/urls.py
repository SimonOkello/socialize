from django.urls import path

from .views import(
    post_create_comment_and_list_view,
    like_unlike_view,
)
app_name = 'posts'
urlpatterns = [
    path('', post_create_comment_and_list_view, name='post-list-view'),
    path('like/', like_unlike_view, name='like-post-view'),
]
