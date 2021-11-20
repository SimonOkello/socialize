from django.urls import path

from .views import(
    post_create_comment_and_list_view,
    like_unlike_view,
    edit_post_view,
    delete_post_view,
)
app_name = 'posts'
urlpatterns = [
    path('', post_create_comment_and_list_view, name='post-list-view'),
    path('like/', like_unlike_view, name='like-post-view'),
    path('<pk>/edit/', edit_post_view, name='edit-post'),
    path('<pk>/delete', delete_post_view, name='delete-post'),
]
