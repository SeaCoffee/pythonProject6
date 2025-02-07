from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated


from apps.users.serializers import UserSerializer
from core.services.jwt_service import JWTService, ActivateToken, RecoveryToken, ActionToken, JWTException
from apps.auth.serializers import EmailSerializer, PasswordSerializer
from core.services.email_service import EmailService
from core.services.jwt_service import RecoveryToken

UserModel = get_user_model()

class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            user = JWTService.verify_token(token, ActivateToken)

            if not user.is_active:
                user.is_active = True
                user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Exception as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RecoverRequestView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = EmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(UserModel, email=serializer.data['email'])
        if not user:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        print("Incoming email:", serializer.data['email'])
        print("Emails in DB:", list(UserModel.objects.values_list("email", flat=True)))
        EmailService.recovery(user)
        return Response({'details': 'link send to email'}, status.HTTP_200_OK)




class RecoveryPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = PasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        token = kwargs['token']
        user = JWTService.verify_token(token, RecoveryToken)

        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.save()


        try:
            token_instance = RecoveryToken(token)
            token_instance.blacklist()
        except Exception as e:
            print(f"Token invalidation error: {e}")

        return Response({'detail': 'Password successfully reset'}, status.HTTP_200_OK)

class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.last_logout = now()
        user.save(update_fields=['last_logout'])

        token = request.data.get("token")
        if token:
            try:
                JWTService.verify_token(token, ActionToken)
            except JWTException:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
