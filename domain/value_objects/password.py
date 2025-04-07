from dataclasses import dataclass
import hashlib

@dataclass(frozen=True)
class Password:
    value: str
    
    def __post_init__(self):
        if not self._is_valid():
            raise ValueError("Password must be at least 8 characters long")
        # Hash the password
        object.__setattr__(self, 'value', self._hash_password(self.value))
    
    def _is_valid(self) -> bool:
        return len(self.value) >= 8
    
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify(self, plain_password: str) -> bool:
        return self.value == self._hash_password(plain_password)
    
    def __str__(self) -> str:
        return self.value 