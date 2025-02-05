from django.urls import path
from apps.users.views import UserCreateView, BlockUserView, \
    UnBlockUserView, UserToAdminView, UserListView, UserRetrieveView, UserFilteredListView, UpdateSelfView, DeleteSelfView

urlpatterns = [
    path('', UserCreateView.as_view(), name='user_create'),
    path('list', UserListView.as_view(), name='users_list'),
    path('<int:pk>/block', BlockUserView.as_view(), name='user_block'),
    path('<int:pk>/unblock', UnBlockUserView.as_view(), name='user_unblock'),
    path('<int:pk>/to_admin', UserToAdminView.as_view(), name='user_to_admin'),
    path('filtered/', UserFilteredListView.as_view(), name='users_filtered_list'),
    path('<str:lookup_value>', UserRetrieveView.as_view(), name='user_detail'),
    path('me/update', UpdateSelfView.as_view(), name='user_update_self'),
    path('me/delete', DeleteSelfView.as_view(), name='user_delete_self'),


]
