import traceback
from flask import Blueprint, jsonify
from marshmallow import ValidationError
from dataclasses import dataclass


error_bp = Blueprint("erros", __name__)


@dataclass
class Error:
    message: str

    def to_json(): ...


@error_bp.app_errorhandler(ValidationError)
def handle_invalid_data(error):
    print(traceback.format_exc())
    return jsonify({"Message": "Некорректный формат данных"}), 400
