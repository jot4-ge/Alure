import os
import json
import uuid
from typing import List, Dict, Optional, Tuple
from app.models.usuario import UserAccount
from app.models.roupa import Roupa
from enum import Enum, auto


class SignInResult(Enum):
    SUCCESS = auto()
    USERNAME_EXISTS = auto()
    VALIDATION_ERROR = auto()


class UserRecord:

    def __init__(self, filename: str):
        # ... (código do __init__ sem alterações) ...
        script_dir = os.path.dirname(__file__)
        self.db_dir = os.path.join(script_dir, 'db')
        os.makedirs(self.db_dir, exist_ok=True)
        self.file_path: str = os.path.join(self.db_dir, filename)

        self.__authenticated_users: Dict[str, UserAccount] = {}
        self.__session_carts: Dict[str, List[Dict]] = {}

        self.__clear_auth_users()
        self.__clear_carts()

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
    def __clear_carts(self) -> None:
        cart_file_path: str = os.path.join(self.db_dir, "users_carts.json")
        with open(cart_file_path, "w", encoding="utf-8") as arquivo_json:
            json.dump({}, arquivo_json)

    def save_auth_user(self):
        auth_file_path: str = os.path.join(self.db_dir, "auth_users.json")
        serializable_users = {}
        for session_id, user_object in self.__authenticated_users.items():
            serializable_users[session_id] = user_object.to_dict_no_password()
        try:
            with open(auth_file_path, "w", encoding="utf-8") as arquivo_json:
                json.dump(serializable_users, arquivo_json, indent=4)
        except Exception as e:
            print(f"ERRO em save_auth_user: Não foi possível salvar o arquivo de autenticação. Erro: {e}")

    def save_session_carts(self):
        """
        Salva o dicionário de carrinhos de sessão em um arquivo JSON.
        Ideal para fins de depuração e visualização.
        """
        carts_file_path: str = os.path.join(self.db_dir, "users_carts.json")
        try:
            with open(carts_file_path, "w", encoding="utf-8") as f:
                # O dicionário __session_carts já está em um formato serializável
                json.dump(self.__session_carts, f, indent=4)
        except Exception as e:
            print(f"ERRO em save_session_carts: Não foi possível salvar os carrinhos. Erro: {e}")


    def _save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            user_data = [user.to_dict() for user in self.__user_accounts]
            json.dump(user_data, f, indent=4)

    def sign_in(self, username: str, email: str, telephone_num: str, password: str) -> Tuple[
        SignInResult, Optional[UserAccount]]:
        if any(user.username == username for user in self.__user_accounts):
            print(f"Erro: Usuário '{username}' já existe.")
            return SignInResult.USERNAME_EXISTS, None

        password_bytes = bytearray(password.encode('utf-8'))

        try:
            new_user = UserAccount.create_with_raw_password(username, email, telephone_num, password_bytes)
            self.__user_accounts.append(new_user)
            self._save()
            return SignInResult.SUCCESS, new_user
        except ValueError as e:
            print(f"Erro ao criar usuário: {e}")
            return SignInResult.VALIDATION_ERROR, None
        finally:
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

                self.__session_carts[session_id] = []

                self.save_auth_user()
                self.save_session_carts()
                return session_id

            return None
        finally:
            password_bytes[:] = b'\x00' * len(password_bytes)

    def logout(self, session_id: str) -> bool:
        cart_removed = False
        if session_id in self.__session_carts:
            del self.__session_carts[session_id]
            cart_removed = True

        user_removed = False
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]
            self.save_auth_user()
            user_removed = True

        if cart_removed or user_removed:
            self.save_session_carts()

        return user_removed

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
                if session_id_to_remove in self.__session_carts:
                    del self.__session_carts[session_id_to_remove]
                del self.__authenticated_users[session_id_to_remove]
                self.save_auth_user()
                self.save_session_carts()

            self._save()
        return user_was_deleted

    def get_cart_by_session(self, session_id: str) -> Optional[List[Dict]]:
        """Retorna o carrinho associado a um session_id."""
        return self.__session_carts.get(session_id)

    def add_product_to_cart(self, session_id: str, product_id: str, quantity: int = 1) -> bool:
        """
        Adiciona um produto (usando seu ID) com uma quantidade específica ao carrinho de uma sessão.
        Retorna True se a operação for bem-sucedida, False caso contrário.
        """
        if session_id not in self.__session_carts:
            return False

        cart = self.__session_carts[session_id]

        # Procura por um item com o mesmo product_id
        for item in cart:
            if item.get('product_id') == product_id:
                item['quantity'] += quantity
                self.save_session_carts()
                return True

        cart.append({
            'product_id': product_id,
            'quantity': quantity
        })
        self.save_session_carts()
        return True

    def update_cart_by_session(self, session_id: str, new_cart: List[Dict]) -> bool:
        """Atualiza o carrinho de uma sessão e retorna True se a sessão existir."""
        if session_id in self.__session_carts:
            self.__session_carts[session_id] = new_cart
            self.save_session_carts()
            return True
        return False
    def remove_product_from_cart(self, session_id: str, product_id: str) -> bool:
        """
        Remove um único produto do carrinho de uma sessão específica.
        Retorna True se o produto foi encontrado e removido, False caso contrário.
        """
        # Verifica se a sessão existe e tem um carrinho associado
        if session_id not in self.__session_carts:
            return False

        cart = self.__session_carts[session_id]
        len_before = len(cart)

        # Cria uma nova lista de carrinho contendo todos os itens, exceto o que deve ser removido
        new_cart = [item for item in cart if item.get('product_id') != product_id]

        # Verifica se um item foi realmente removido comparando os tamanhos das listas
        if len(new_cart) < len_before:
            self.__session_carts[session_id] = new_cart
            self.save_session_carts()  # Salva a alteração no arquivo JSON
            return True

        # Retorna False se o product_id não foi encontrado no carrinho
        return False

    def clear_user_cart(self, session_id: str) -> bool:
        """
        Remove todos os produtos do carrinho de uma sessão (esvazia o carrinho).
        Retorna True se a sessão foi encontrada e o carrinho limpo, False caso contrário.
        """
        # Verifica se a sessão existe para que possamos limpar o carrinho
        if session_id in self.__session_carts:
            self.__session_carts[session_id] = []  # Substitui a lista de itens por uma lista vazia
            self.save_session_carts()  # Salva o estado do carrinho vazio no arquivo JSON
            return True

        # Retorna False se a sessão não foi encontrada
        return False