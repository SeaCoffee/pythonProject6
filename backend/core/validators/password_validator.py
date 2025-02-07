import re
from django.core.exceptions import ValidationError
from core.enums.password_enum import PasswordRegexEnum

def validate_password(value: str):

    for rule in PasswordRegexEnum:
        if not re.search(rule.pattern, value):
            raise ValidationError(rule.msg)
