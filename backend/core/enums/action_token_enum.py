from datetime import timedelta
from enum import Enum

class ActionTokenEnum(Enum):
    ACTIVATE = (
        'activate',
        timedelta(days=30),
    )
    RECOVERY = (
        'recovery',
        timedelta(days=60),
    )

    def __init__(self, token_type, lifetime):
        self.token_type = token_type
        self.lifetime = lifetime
