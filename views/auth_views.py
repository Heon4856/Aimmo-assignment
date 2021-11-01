from flask import Blueprint, jsonify, make_response, request
from models.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=['POST'])
def signup():
    body = request.get_json()
    user = User(**body).save()
    id = user.id
    return make_response(jsonify(msg='success', status_code=201, id=str(id)), 201)


@bp.route('/login/', methods=['POST'])
def login():
    body = request.get_json()
    is_login_success = User.objects(name=body["name"]).first()
    if is_login_success:
        return jsonify(id=str(is_login_success.id), status_code=200)
