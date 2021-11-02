from flask import Blueprint, make_response, jsonify
from flask import request, jsonify
from flask_jwt_extended.utils import get_jwt
from service import post_service
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('post', __name__, url_prefix='/')


@bp.route('/')
def hello_world():
    return 'Hello! blueprint'


@bp.route('/create', methods=['POST'])
@jwt_required()
def create_post():
    current_user_id = get_jwt_identity()
    body = request.get_json()
    id = post_service.create_post(body["title"], body["content"], current_user_id, body["tags"])
    return make_response(jsonify(msg='success', status_code=201, id=str(id)), 201)


@bp.route('/posts', methods=['GET'])
def read_post_list():
    page = request.args.get('page', type=int, default=1)
    tags = request.args.get('tags')
    post_list = post_service.read_post_list(page, tags)
    return make_response(jsonify(post_list))


@bp.route('/posts/<post_id>', methods=['GET'])
def read_detail(post_id):
    cookie_value, max_age = post_service.count_hit_post(post_id, request)
    post = post_service.read_post_detail(post_id)
    response = make_response(post)
    response.set_cookie('hitboard', value=cookie_value, max_age=max_age, httponly=True)
    return response


@bp.route('/posts/<post_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post(post_id):
    current_user_id = get_jwt_identity()
    body = request.get_json()
    if post_service.update_post(post_id, body["title"], body["content"], current_user_id):
        return make_response(jsonify(msg='update_success', status_code=200, id=str(id)), 200)
    return make_response(jsonify(msg="권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요", status_code=401), 401)


@bp.route('/posts/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    current_user_id = get_jwt_identity()
    if post_service.delete_post_if_user_authorized(post_id, current_user_id):
        return make_response('', 204)
    return make_response(jsonify(msg="권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요.", status_code=401), 401)


@bp.route('/lists', methods=['GET'])
def search_post():
    keyword = request.args.get('keyword')
    tags = request.args.get('tags')
    posts = post_service.search_keyword(keyword, tags).to_json()
    return make_response(posts, 200)


@bp.route('/posts/<post_id>/comment_create', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    body = request.get_json()
    user_id = get_jwt_identity()
    create_comment_info = {
        'user_id' : user_id,
        'post_id' : post_id,
        'content' : body['content'],
    }
    if 'oid' in body:
        create_comment_info['oid'] = body['oid']
    post_service.create_comment_service(create_comment_info)
    return make_response(jsonify(msg='create_comment_success', status_code=201, id=str(id)), 201)


@bp.route('/post/<post_id>')
@jwt_required()
def delete_comment():
    user_id = get_jwt_identity()
    post_id = request.args.get('post_id')
    comment_id = request.args.get('comment_id')
    delete_comment_info = {
        'user_id' : user_id,
        'post_id' : post_id,
        'oid' : comment_id
    }
    post_service.delete_comment_service(delete_comment_info)
    return make_response(jsonify(msg='delete_comment_success', status_code=201, id=str(id)), 201)