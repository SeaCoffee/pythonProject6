from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound



from apps.users.serializers import UserSerializer, ProfileSerializer
from apps.users.filters import UserFilter

UserModel = get_user_model()

class UserCreateView(CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserListView(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

class BlockUserView(GenericAPIView):
    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

class UnBlockUserView(GenericAPIView):
    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserToAdminView(GenericAPIView):
    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_staff:
            user.is_active = True
            user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UpdateSelfView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    http_method_names = ['patch']
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        if not user:
            raise NotFound("User not found")
        return user
    def perform_update(self, serializer):
        user = self.get_object()

        if "password" in self.request.data:
            user.set_password(self.request.data["password"])
            user.save(update_fields=["password"])

        serializer.save()

        profile_data = self.request.data.get("profile")
        if profile_data:
            profile_serializer = ProfileSerializer(user.profile, data=profile_data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        serializer.save()


class DeleteSelfView(DestroyAPIView):
    queryset = UserModel.objects.all()
    http_method_names = ['delete']
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.delete()

class UserRetrieveView(RetrieveAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        lookup_value = self.kwargs.get("lookup_value")

        if lookup_value.isdigit():
            user = UserModel.objects.filter(pk=lookup_value).first()
        else:
            user = UserModel.objects.filter(email=lookup_value).first()

        if not user:
            raise NotFound("User not found")

        return user


class UserFilteredListView(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)  # Или IsAdminUser
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter