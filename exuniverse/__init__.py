from .app import *
from .api import *
from .login_manager import *


if __name__ == "__main__":
    app.run('0.0.0.0', debug=True, port = 5000)
