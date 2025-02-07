from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status

from apps.posts.models import PostModel
from apps.posts.serializers import PostSerializer, PostPhotoSerializer
from apps.posts.filters import PostFilter

class PostListCreateView(ListCreateAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = [DjangoFilterBackend]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return self.queryset.filter(author=self.request.user)
        return self.queryset


class PostAddPhotoView(UpdateAPIView):
    serializer_class = PostPhotoSerializer
    queryset = PostModel.objects.all()
    http_method_names = ['patch']
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.photo:
            post.photo.delete()
        super().perform_update(serializer)










