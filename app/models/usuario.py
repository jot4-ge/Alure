import uuid
import bcrypt
from typing import Dict

class UserAccount:
    def __init__(self, username: str, password_hash: str, user_id: str = None):
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string.")
        if not password_hash or not isinstance(password_hash, str):
            raise ValueError("Password hash must be a non-empty string.")

        self.id: str = user_id or str(uuid.uuid4())
        self.username: str = username
        self.password_hash: str = password_hash


    @staticmethod
    def create_with_raw_password(username: str, raw_password_bytes: bytearray) -> 'UserAccount':
        if not raw_password_bytes or len(raw_password_bytes) < 5:
            raise ValueError("Password must be at least 5 characters long.")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(raw_password_bytes, salt).decode('utf-8')

        return UserAccount(username=username, password_hash=password_hash)

    def verify_password(self, raw_password_bytes: bytearray) -> bool:
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(raw_password_bytes, password_hash_bytes)

    def to_dict(self) -> Dict[str, str]:
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash
        }

    def __repr__(self) -> str:
        return f"UserAccount(id='{self.id}', username='{self.username}')"