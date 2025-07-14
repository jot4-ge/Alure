import os
import json
import uuid
from typing import List, Dict, Optional
from app.models.usuario import UserAccount


class UserRecord:


    def __init__(self, filename: str):
        if not isinstance(filename, str):
            raise TypeError(f"Expected filename to be a string, but got {type(filename).__name__}")
        if not filename.strip():
            raise ValueError("Expected filename to be a non-empty string.")

        script_dir = os.path.dirname(__file__)
        self.db_dir = os.path.join(script_dir, 'db')
        os.makedirs(self.db_dir, exist_ok=True)
        self.file_path: str = os.path.join(self.db_dir, filename)

        self.__authenticated_users: Dict[str, UserAccount] = {}
        self.__clear_auth_users()
        self.__user_accounts: List[UserAccount] = []
        self.read()


    def read(self) -> None:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            print("ERRO read() UserRecord: Json não achado, lista de produtos vazia na memória.")
            with open(self.file_path, "w", encoding="utf-8") as arquivo_json:
                json.dump([], arquivo_json)
            return
        except json.JSONDecodeError:
            print("ERRO read() UserRecord: Erro ao decodificar JSON. O arquivo pode estar corrompido.")
            with open(self.file_path, "w", encoding="utf-8") as arquivo_json:
                json.dump([], arquivo_json)
            return

    def __clear_auth_users(self) -> None:
        auth_file_path: str = os.path.join(self.db_dir, "auth_users.json")
        with open(auth_file_path, "w", encoding="utf-8") as arquivo_json:
            json.dump({}, arquivo_json)

    def save_auth_user(self):
        auth_file_path: str = os.path.join(self.db_dir, "auth_users.json")
        serializable_users = {}
        for session_id, user_object in self.__authenticated_users.items():
            serializable_users[session_id] = user_object.to_dict()
        try:
            with open(auth_file_path, "w", encoding="utf-8") as arquivo_json:
                json.dump(serializable_users, arquivo_json, indent=4)
        except Exception as e:
            print(f"ERRO em save_auth_user: Não foi possível salvar o arquivo de autenticação. Erro: {e}")

    def _save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            user_data = [user.to_dict() for user in self.__user_accounts]
            json.dump(user_data, f, indent=4)

    def sign_in(self, username: str,email: str, telephone_num : str, password: str) -> Optional[UserAccount]:
        if any(user.username == username for user in self.__user_accounts):
            print(f"Erro: Usuário '{username}' já existe.")
            return None

        # Converte a senha para um tipo mutável (bytearray)
        password_bytes = bytearray(password.encode('utf-8'))

        try:
            # Passa o bytearray para a função de criação
            new_user = UserAccount.create_with_raw_password(username,email,telephone_num, password_bytes)
            self.__user_accounts.append(new_user)
            self._save()
            return True
        except ValueError as e:
            print(f"Erro ao criar usuário: {e}")
            return None
        finally:
            # Sobrescreve o bytearray com zeros, garantindo a remoção da memória.
            password_bytes[:] = b'\x00' * len(password_bytes)

    def get_current_user(self, session_id: str) -> Optional[UserAccount]:
        return self.__authenticated_users.get(session_id)

    def get_user_name(self, session_id: str) -> Optional[str]:
        user = self.get_current_user(session_id)
        return user.username if user else None

    def get_user_session_id(self, username: str) -> Optional[str]:
        for session_id, user in self.__authenticated_users.items():
            if user.username == username:
                return session_id
        return None


    def login(self, username: str, password: str) -> Optional[str]:
        password_bytes = bytearray(password.encode('utf-8'))

        try:
            user_to_check = next((user for user in self.__user_accounts if user.username == username), None)
            if user_to_check and user_to_check.verify_password(password_bytes):
                session_id = str(uuid.uuid4())
                self.__authenticated_users[session_id] = user_to_check
                self.save_auth_user()
                return session_id

            # Retorna None se o usuário não for encontrado ou a senha estiver incorreta
            return None
        finally:
            # 3. A limpeza agora é garantida, não importa o resultado
            password_bytes[:] = b'\x00' * len(password_bytes)


    def logout(self, session_id: str) -> bool:
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]
            self.save_auth_user()
            return True
        return False

    def delete_user(self, user_id: str) -> bool:

        len_before = len(self.__user_accounts)
        self.__user_accounts = [
            user for user in self.__user_accounts if user.id != user_id
        ]
        user_was_deleted = len(self.__user_accounts) < len_before

        if user_was_deleted:
            session_id_to_remove = None
            for session_id, authenticated_user in self.__authenticated_users.items():
                if authenticated_user.id == user_id:
                    session_id_to_remove = session_id
                    break

            if session_id_to_remove:
                del self.__authenticated_users[session_id_to_remove]
                self.save_auth_user()

            self._save()
        return user_was_deleted