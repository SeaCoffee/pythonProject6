from django_filters import rest_framework as filters

from apps.posts.models import PostModel

class PostFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = filters.NumberFilter(field_name='author_id')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lt')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gt')
    order = filters.OrderingFilter(
        fields=[
            ('created_at', 'created_at'),
            ('updated_at', 'updated_at'),
            ('title', 'title'),
        ]
    )


    class Meta:
        model = PostModel
        fields = ['title', 'author', 'created_before', 'created_after']
