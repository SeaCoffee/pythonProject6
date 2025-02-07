from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.validators.password_validator import validate_password

UserModel = get_user_model()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'validators': [validate_password],
            }
        }