from rest_framework_simplejwt.tokens import BlacklistMixin, Token
from typing import Type
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.timezone import now


from core.enums.action_token_enum import ActionTokenEnum
from core.exceptions.jwt_exceptions import JWTException, JWTBlacklistException, JWTExpiredException,JWTInvalidException

UserModel = get_user_model()

ActionTokenClassType = Type[BlacklistMixin | Token]

class ActionToken(BlacklistMixin, Token):
    pass

class ActivateToken(ActionToken):
    token_type = ActionTokenEnum.ACTIVATE.token_type
    lifetime = ActionTokenEnum.ACTIVATE.lifetime

class RecoveryToken(ActionToken):
    token_type = ActionTokenEnum.RECOVERY.token_type
    lifetime = ActionTokenEnum.RECOVERY.lifetime

class JWTService:
    @staticmethod
    def create_token(user, token_class: ActionTokenClassType):
        user.last_login = now()
        user.save(update_fields=['last_login'])
        return token_class.for_user(user)

    @staticmethod
    def verify_token(token, token_class: ActionTokenClassType):
        try:
            token_res = token_class(token)
            token_res.check_blacklist()
        except token_class.BlacklistError:
            raise JWTBlacklistException()
        except token_class.TokenError:
            raise JWTInvalidException()
        except Exception as e:
            raise JWTException(f"Unexpected JWT error: {e}")

        user_id = token_res.payload.get('user_id')
        user = get_object_or_404(UserModel, pk=user_id)

        user.last_login = now()
        user.save(update_fields=['last_login'])


        if token_class == RecoveryToken:
            try:
                token_res.check_blacklist()
            except token_class.BlacklistError:
                pass

            token_res.blacklist()

        return user