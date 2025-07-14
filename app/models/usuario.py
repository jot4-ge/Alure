import uuid
import bcrypt
from typing import Dict

class UserAccount:
    def __init__(self, username: str,email : str, telephone_num : str, password_hash: str, id: str = None):
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string.")
        if not password_hash or not isinstance(password_hash, str):
            raise ValueError("Password hash must be a non-empty string.")

        self.id: str = id or str(uuid.uuid4())
        self.username: str = username
        self.email : str = email
        self.telephone_num : str = telephone_num
        self.password_hash: str = password_hash



    @staticmethod
    def create_with_raw_password(username: str,email : str, telephone_num : str, raw_password_bytes: bytearray) -> 'UserAccount':
        if not raw_password_bytes or len(raw_password_bytes) < 5:
            raise ValueError("Password must be at least 5 characters long.")
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(bytes(raw_password_bytes), salt).decode('utf-8')

        return UserAccount(username = username,email = email,telephone_num = telephone_num, password_hash = password_hash)

    def verify_password(self, raw_password_bytes: bytearray) -> bool:
        password_hash_bytes = self.password_hash.encode('utf-8')
        return bcrypt.checkpw(bytes(raw_password_bytes), bytes(password_hash_bytes))

    def to_dict(self) -> Dict[str, str]:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'telephone_num': self.telephone_num, #
            'password_hash': self.password_hash
        }

    def __repr__(self) -> str:
        return f"UserAccount(id='{self.id}', username='{self.username}')"