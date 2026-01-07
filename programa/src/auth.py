from .repository import Repository
from .models import Usuario

class AuthController:
    def __init__(self):
        self.repo = Repository("usuarios")

    def login(self, username, password):
        users = self.repo.load_all(Usuario.from_row)
        
        for user in users:
            # Note: Model order is now Name, User, Pass
            if user.username == username and user.password == password:
                return user
        return None
