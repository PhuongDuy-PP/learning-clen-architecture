import re

class Email:
    def __init__(self, value: str):
        if not self._is_valid_email(value):
            raise ValueError(f"Invalid email address: {value}")
        self.value = value

    @property
    def value(self) -> str:
        return self.value

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self.value == other.value
        return False

    def __str__(self):
        return self.value