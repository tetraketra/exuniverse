from .app import *
from .api import *
from .login_manager import *


if __name__ == "__main__":
    app.run('192.168.1.177', debug=True, port = 8000)
