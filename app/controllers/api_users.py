import json
import traceback
# A importação de 'requests' não é mais necessária
from bottle import request, response
from app.controllers.UserRecord import UserRecord, SignInResult
from typing import Optional

class UsersAPI:
    """
    Encapsula a lógica de negócio para a API de usuários, sessões e carrinhos.
    """

    def __init__(self):
        """Inicializa a API e sua conexão com o 'banco de dados' de usuários."""
        self.user_db = UserRecord('users.json')
        # A URL da API de produtos não é mais necessária aqui

    @staticmethod
    def to_json(data: any) -> str:
        """Converte dados para uma resposta JSON com o header correto."""
        response.content_type = 'application/json'
        return json.dumps(
            data,
            default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else o.__dict__,
            indent=4
        )

    # --- Métodos de Usuário (sign_in, login, logout, etc.) permanecem os mesmos ---
    # ... (código de sign_in, login, logout, etc. sem alterações) ...
    def sign_in(self):
        """
        Registra (cria) um novo usuário.
        Espera um JSON no corpo da requisição com 'username', 'email', 'telephone_num' e 'password'.
        """
        try:
            data = request.json
            if not data:
                response.status = 400
                return self.to_json({"error": "O corpo da requisição (JSON) está ausente."})

            required_fields = ['username', 'email', 'telephone_num', 'password']
            for field in required_fields:
                value = data.get(field)
                if value is None:
                    response.status = 400
                    return self.to_json({"error": f"O campo obrigatório '{field}' está ausente."})
                if not isinstance(value, str) or not value.strip():
                    response.status = 400
                    return self.to_json({"error": f"O campo '{field}' não pode ser um texto vazio."})

            username = data.get("username")
            email = data.get("email")
            telephone_num = data.get("telephone_num")
            password = data.get("password")

            # A função agora retorna uma tupla (status, dados)
            result, new_user = self.user_db.sign_in(username, email, telephone_num, password)

            if result == SignInResult.SUCCESS:
                # Usuário criado, agora faz o login automático para criar a sessão.
                session_id = self.user_db.login(username, password)

                if not session_id:
                    response.status = 500
                    return self.to_json({"error": "Usuário criado, mas falha ao gerar a sessão."})

                # Define o cookie seguro no navegador do usuário
                response.set_cookie(
                    "session_id",
                    session_id,
                    secret='uma-chave-secreta-muito-forte',
                    httponly=True,
                    path='/'
                )
                response.status = 201  # Created
                return self.to_json({"message": f"Usuário '{username}' criado e logado com sucesso."})
            elif result == SignInResult.USERNAME_EXISTS:
                response.status = 409
                return self.to_json({"error": f"Nome de usuário '{username}' ou e-mail '{email}' já existe."})
            elif result == SignInResult.VALIDATION_ERROR:
                response.status = 400
                return self.to_json({"error": "Dados inválidos. Verifique se a senha atende aos requisitos mínimos."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def login(self):
        """
        Autentica um usuário e retorna um ID de sessão.
        Espera um JSON no corpo da requisição com 'username' e 'password'.
        Se o usuário já estiver logado, invalida a sessão antiga e cria uma nova.
        """
        try:
            data = request.json
            if not data or 'username' not in data or 'password' not in data:
                response.status = 400  # Bad Request
                return self.to_json({"error": "Campos 'username' e 'password' são obrigatórios."})

            username = data.get('username')
            password = data.get('password')

            session_id = self.user_db.login(username, password)

            if session_id:
                response.status = 200  # OK
                # Define o cookie seguro no navegador do usuário
                response.set_cookie(
                    "session_id",
                    session_id,
                    secret='uma-chave-secreta-muito-forte',
                    httponly=True,
                    path='/'
                )
                return self.to_json({"message": "Login bem-sucedido.", "session_id": session_id})
            else:
                response.status = 401  # Unauthorized
                return self.to_json({"error": "Credenciais inválidas."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def logout(self):
        """
        Desconecta um usuário, invalidando sua sessão a partir do cookie.
        """
        try:
            session_id = request.get_cookie("session_id", secret='uma-chave-secreta-muito-forte')
            if not session_id:
                response.status = 401  # Unauthorized
                return self.to_json({"error": "Nenhum usuário logado para desconectar."})

            success = self.user_db.logout(session_id)

            # Deleta o cookie do navegador, independentemente de a sessão existir no DB.
            # Isso garante que o navegador não envie mais um cookie inválido.
            response.delete_cookie("session_id", path='/')

            if success:
                response.status = 200
                return self.to_json({"message": "Logout bem-sucedido."})
            else:
                # Mesmo que a sessão não exista no DB, o cookie foi removido do cliente.
                response.status = 200
                return self.to_json({"message": "Sessão já estava inválida, cookie removido."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def delete_user(self, user_id: str):
        """
        Deleta um usuário específico pelo seu ID.
        """
        try:
            success = self.user_db.delete_user(user_id)

            if success:
                response.status = 200
                return self.to_json({"message": f"Usuário com ID '{user_id}' deletado com sucesso."})
            else:
                response.status = 404
                return self.to_json({"error": f"Usuário com ID '{user_id}' não encontrado."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def get_current_user_info(self):
        """
        Retorna informações do usuário logado a partir do cookie de sessão.
        """
        try:
            session_id = request.get_cookie("session_id", secret='uma-chave-secreta-muito-forte')
            if not session_id:
                response.status = 401  # Unauthorized
                return self.to_json({"error": "Sessão inválida ou expirada. Faça o login novamente."})

            user = self.user_db.get_current_user(session_id)

            if user:
                response.status = 200
                return self.to_json(user)
            else:
                response.status = 404
                return self.to_json({"error": "Usuário não encontrado para esta sessão."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})


    # --- Métodos do Carrinho ---

    def get_cart(self):
        """
        Retorna dados básicos do carrinho (IDs e quantidades).
        """
        try:
            session_id = request.get_cookie("session_id", secret='uma-chave-secreta-muito-forte')
            if not session_id:
                return self.to_json([])

            cart = self.user_db.get_cart_by_session(session_id)

            if cart is None:
                return self.to_json([])

            return self.to_json(cart)

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Erro ao buscar carrinho: {e}"})

    def add_to_cart(self):
        """
        Adiciona um item ao carrinho, confiando que o ID do produto é válido.
        """
        try:
            session_id = request.get_cookie("session_id", secret='uma-chave-secreta-muito-forte')
            if not session_id:
                response.status = 401
                return self.to_json({"error": "Faça o login para adicionar itens ao carrinho."})

            data = request.json
            if not data or 'product_id' not in data or 'quantity' not in data:
                response.status = 400
                return self.to_json({"error": "Requisição inválida. 'product_id' e 'quantity' são obrigatórios."})

            product_id = data['product_id']
            quantity = int(data['quantity'])

            success = self.user_db.add_product_to_cart(session_id, product_id, quantity)

            if not success:
                response.status = 401
                return self.to_json({"error": "Sessão inválida. Faça o login novamente."})

            updated_cart = self.user_db.get_cart_by_session(session_id)
            new_cart_count = sum(item['quantity'] for item in updated_cart) if updated_cart else 0

            response.status = 200
            return self.to_json({
                "message": "Item adicionado ao carrinho com sucesso!",
                "new_cart_count": new_cart_count
            })

        except ValueError:
            response.status = 400
            return self.to_json({"error": "A quantidade deve ser um número inteiro."})
        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Erro ao adicionar ao carrinho: {e}"})