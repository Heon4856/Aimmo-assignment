from flask import Blueprint, jsonify, make_response, request
from models.models import User
from service import auth_service

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=['POST'])
def signup():
    body = request.get_json()
    id = auth_service.signup(body['name'], body['password'])
    return make_response(jsonify(msg='success', status_code=201, id=str(id)), 201)


@bp.route('/login/', methods=['POST'])
def login():
    body = request.get_json()
    access_token = auth_service.login(body['name'], body['password'])
    if access_token:
        return jsonify(access_token=access_token, status_code=200)
    return make_response(jsonify(msg='잘못된 로그인 정보입니다.', status_code=404), 404)
