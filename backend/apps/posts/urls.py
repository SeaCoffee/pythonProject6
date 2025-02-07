from django.urls import path

from apps.posts.views import PostListCreateView, PostAddPhotoView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path("", PostListCreateView.as_view(), name='post_list_create'),
    path("<int:pk>", PostRetrieveUpdateDestroyView.as_view(), name='post_update_delete'),
    path("<int:pk>/photo", PostAddPhotoView.as_view(), name='post_add_photo'),
]
