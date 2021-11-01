from flask import Blueprint
import json
from flask import request, jsonify
from models.models import User

bp = Blueprint('post', __name__, url_prefix='/')


@bp.route('/')
def hello_world():
    return 'Hello! blueprint'


# @doc(tags=['post'], description='게시글을 저장한다.')
@bp.route('/create', methods=['POST'])
@use_kwargs(CreatePostRequestSchema)
@marshal_with(None, code=201)
def create(subject, content):
    post_service.create_post(subject, content, current_user)
    return make_response(jsonify(msg='success', status_code=201), 201)

