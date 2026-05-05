from flask import Blueprint

edit_bp = Blueprint(
    "edit_bp", __name__, template_folder="templates", static_folder="static"
)

from . import routes