from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from apps.users.models import ProfileModel
from core.services.email_service import EmailService
from core.validators.password_validator import validate_password

UserModel = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = (
            'id',
            'name',
            'surname',
            'age',
            'created_at',
            'updated_at',
        )

class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'last_logout',
            'created_at',
            'updated_at',
            'profile',
        )
        read_only_fields = (
            'id',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'last_logout',
            'created_at',
            'updated_at',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'validators': [validate_password],
            }

        }
    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        profile = ProfileModel.objects.create(**profile, user=user)
        EmailService.register(user)
        return user
