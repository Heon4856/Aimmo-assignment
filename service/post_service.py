from repository import post_repository
from datetime import datetime


def read_post_detail(id):
    return post_repository.read_post_detail(id)


def create_post(title, content, current_user_id):
    date = datetime.now()
    return post_repository.create(title, content, date, current_user_id)


def update_post(id, title, content, current_user_id):
    modify_date = datetime.now()
    return post_repository.modify(id, title, content, modify_date, current_user_id)


def delete_post_if_user_authorized(id, current_user_id):
    return post_repository.delete(id, current_user_id)
