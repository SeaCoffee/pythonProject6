from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound



from apps.users.serializers import UserSerializer, ProfileSerializer
from apps.users.filters import UserFilter
from apps.auth.serializers import PasswordSerializer
from core.services.jwt_service import RecoveryToken

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
        password_changed = False
        validated_data = serializer.validated_data


        if "password" in self.request.data:
            password_serializer = PasswordSerializer(data={"password": self.request.data["password"]})
            password_serializer.is_valid(raise_exception=True)

            new_password = password_serializer.validated_data["password"]
            user.set_password(new_password)
            user.save()

            password_changed = True

            validated_data.pop("password", None)

        serializer.save()

        profile_data = self.request.data.get("profile")
        if profile_data:
            profile_serializer = ProfileSerializer(user.profile, data=profile_data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        if password_changed:
            try:
                token = self.request.auth
                if token:
                    token_instance = RecoveryToken(str(token))
                    token_instance.blacklist()
            except Exception as e:
                print(f"Token invalidation error: {e}")

            return Response(
                {"detail": "Password changed successfully. Please log in again."},
                status=200
            )



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
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter