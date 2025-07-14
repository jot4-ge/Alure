import json
import traceback
from bottle import request, response
from app.controllers.UserRecord import UserRecord

class UsersAPI:
    """
    Encapsula toda a lógica de negócio para a API de usuários.
    """

    def __init__(self):
        """Inicializa a API e sua conexão com o 'banco de dados' de usuários."""
        self.user_db = UserRecord('users.json')

    @staticmethod
    def to_json(data: any) -> str:
        """Converte dados para uma resposta JSON com o header correto."""
        response.content_type = 'application/json'
        return json.dumps(
            data,
            default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else o.__dict__,
            indent=4
        )

    def sign_in(self):
        """
        Registra (cria) um novo usuário.
        Espera um JSON no corpo da requisição com 'username' e 'password'.
        """
        try:
            data = request.json
            if not data or 'username' not in data or 'password' not in data:
                response.status = 400
                return self.to_json({"error": "Campos 'username' e 'password' são obrigatórios."})

            username = data.get('username')
            password = data.get('password')

            if not (isinstance(username, str) and username.strip() and isinstance(password, str) and password):
                response.status = 400
                return self.to_json({"error": "Username e password devem ser strings não vazias."})

            new_user_created = self.user_db.sign_in(username, password)

            if new_user_created:
                response.status = 201
                return self.to_json({"message": f"Usuário '{username}' criado com sucesso."})
            else:
                response.status = 409
                return self.to_json({"error": f"Usuário '{username}' já existe."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def login(self):
        """
        Autentica um usuário e retorna um ID de sessão.
        Espera um JSON no corpo da requisição com 'username' e 'password'.
        """
        try:
            data = request.json
            if not data or 'username' not in data or 'password' not in data:
                response.status = 400
                return self.to_json({"error": "Campos 'username' e 'password' são obrigatórios."})

            username = data.get('username')
            password = data.get('password')

            if self.user_db.isUserLoggedIn(username):
                response.status = 409
                return self.to_json({"error": f"O usuário '{username}' já possui uma sessão ativa."})

            session_id = self.user_db.login(username, password)

            if session_id:
                response.status = 200
                return self.to_json({"message": "Login bem-sucedido.", "session_id": session_id})
            else:
                response.status = 401
                return self.to_json({"error": "Credenciais inválidas."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})

    def logout(self):
        """
        Desconecta um usuário, invalidando seu ID de sessão.
        Espera um JSON no corpo da requisição com 'session_id'.
        """
        try:
            data = request.json
            if not data or 'session_id' not in data:
                response.status = 400
                return self.to_json({"error": "Campo 'session_id' é obrigatório."})

            session_id = data.get('session_id')
            success = self.user_db.logout(session_id)

            if success:
                response.status = 200
                return self.to_json({"message": "Logout bem-sucedido."})
            else:
                response.status = 404
                return self.to_json({"error": "Sessão não encontrada ou já expirada."})

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
        Retorna informações do usuário logado a partir de um ID de sessão
        enviado no cabeçalho de autorização (Authorization: Bearer <session_id>).
        """
        try:
            # 1. Obter o cabeçalho de autorização
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                response.status = 401  # Unauthorized
                return self.to_json({"error": "Cabeçalho de autorização ausente."})

            # 2. Validar o formato "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                response.status = 401  # Unauthorized
                return self.to_json(
                    {"error": "Formato do cabeçalho de autorização inválido. Use 'Bearer <token>'."})

            session_id = parts[1]

            # 3. Buscar o usuário
            user = self.user_db.get_current_user(session_id)

            if user:
                response.status = 200
                return self.to_json(user)
            else:
                response.status = 404
                return self.to_json({"error": "Nenhum usuário autenticado com esta sessão ou sessão inválida."})

        except Exception as e:
            traceback.print_exc()
            response.status = 500
            return self.to_json({"error": f"Ocorreu um erro inesperado no servidor: {e}"})