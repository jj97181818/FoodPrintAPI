from flask_login import LoginManager, UserMixin

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, username):
        super().__init__()

        self.id = username

@login_manager.user_loader
def user_loader(username):
    return User(username)