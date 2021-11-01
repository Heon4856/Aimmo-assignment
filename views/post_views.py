from flask import Blueprint, make_response, jsonify
import json
from flask import request, jsonify
from models.models import User, Post

bp = Blueprint('post', __name__, url_prefix='/')


@bp.route('/')
def hello_world():
    return 'Hello! blueprint'


@bp.route('/create', methods=['POST'])
def create():
    body = request.get_json()
    post = Post(**body).save()
    id = post.id
    return make_response(jsonify(msg='success', status_code=201, id=str(id)), 201)


@bp.route('/posts/<id>', methods=['GET'])
def read(id):
    post = Post.objects.get_or_404(id=id)
    return make_response(jsonify(post))


@bp.route('/posts/<id>', methods=['PUT', 'PATCH'])
def update(id):
    body = request.get_json()
    post = Post.objects.get_or_404(id=id)
    post.update(**body)
    return make_response(jsonify(msg='success', status_code=201, id=str(id)), 201)


@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
    post = Post.objects.get_or_404(id=id)
    post.delete()
    return make_response('', 204)
