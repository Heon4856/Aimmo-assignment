from flask import Blueprint, make_response, jsonify
from flask import request, jsonify
from models.models import Post
from service import post_service

bp = Blueprint('post', __name__, url_prefix='/')


@bp.route('/')
def hello_world():
    return 'Hello! blueprint'


@bp.route('/create', methods=['POST'])
def create():
    body = request.get_json()
    id = post_service.create_post(body["title"], body["content"])
    return make_response(jsonify(msg='success', status_code=201, id=str(id)), 201)


@bp.route('/posts/<id>', methods=['GET'])
def read(id):
    post=post_service.read_post_detail(id)
    return make_response(jsonify(post))


@bp.route('/posts/<id>', methods=['PUT', 'PATCH'])
def update(id):
    body = request.get_json()
    post_service.update_post(id, body["title"], body["content"] )
    return make_response(jsonify(msg='update_success', status_code=201, id=str(id)), 201)


@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
    post_service.delete_post_if_user_authorized(id, current_user)
    return make_response('', 204)
