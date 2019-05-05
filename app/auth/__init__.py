from flask import Blueprint

# Макет авторизации
auth = Blueprint('auth', __name__)

from . import views