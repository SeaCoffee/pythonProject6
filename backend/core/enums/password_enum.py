from enum import Enum


class PasswordRegexEnum(Enum):
    MIN_LENGTH = (
        r'.{8,}',
        'Password must be at least 8 characters long.'
    )
    UPPERCASE = (
        r'[A-Z]',
        'Password must contain at least one uppercase letter.'
    )
    LOWERCASE = (
        r'[a-z]',
        'Password must contain at least one lowercase letter.'
    )
    DIGIT = (
        r'\d',
        'Password must contain at least one digit.'
    )
    SPECIAL_CHAR = (
        r'[\W_]',
        'Password must contain at least one special character.'
    )

    def __init__(self, pattern: str, msg: str):
        self.pattern = pattern
        self.msg = msg
