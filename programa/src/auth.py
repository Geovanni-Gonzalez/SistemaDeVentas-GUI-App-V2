import hashlib

from .repository import Repository
from .models import Usuario


def hash_password(password):
    """Devuelve el hash SHA-256 (hex) de la contraseña en texto plano."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class AuthController:
    def __init__(self):
        self.repo = Repository("usuarios")

    def login(self, username, password):
        users = self.repo.load_all(Usuario.from_row)
        hashed = hash_password(password)
        for user in users:
            if user.username == username and user.password == hashed:
                return user
        return None
